#!/bin/bash
set -euo pipefail

# Load .env if present
if [ -f "/home/ubuntu/.openclaw/workspace/.env" ]; then
  export $(cat /home/ubuntu/.openclaw/workspace/.env | grep -v '^#' | xargs)
fi

MAX=${1:-10}

API_KEY="${MATON_API_KEY:?MATON_API_KEY not set}"
CONN_ID="${CONNECTION_ID:?CONNECTION_ID not set}"

# 1. List IDs
list_url="https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=$MAX"
msg_ids=$(curl -s -H "Authorization: Bearer $API_KEY" "$list_url" | python3 -c "import json,sys; d=json.load(sys.stdin); print(' '.join([m['id'] for m in d.get('messages',[])]))")

if [ -z "$msg_ids" ]; then
  echo "[]"
  exit 0
fi

# 2. Fetch each message's headers in parallel (max 5 concurrent)
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

for id in $msg_ids; do
  (
    resp=$(curl -s -H "Authorization: Bearer $API_KEY" \
      "https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/$id?format=full")
    from=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); h=[h for h in d.get('payload',{}).get('headers',[]) if h['name'].lower()=='from']; print(h[0]['value'] if h else '')")
    subject=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); h=[h for h in d.get('payload',{}).get('headers',[]) if h['name'].lower()=='subject']; print(h[0]['value'] if h else '')")
    date=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); h=[h for h in d.get('payload',{}).get('headers',[]) if h['name'].lower()=='date']; print(h[0]['value'] if h else '')")
    snippet=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('snippet',''))")
    # Build JSON with jq for safety
    jq -n \
      --arg mid "$id" \
      --arg from "$from" \
      --arg subject "$subject" \
      --arg date "$date" \
      --arg snippet "$snippet" \
      '{messageId:$mid, from:$from, subject:$subject, date:$date, snippet:$snippet}' \
      > "$TMPDIR/$id.json"
  ) &
  pids+=($!)
  if [ ${#pids[@]} -ge 5 ]; then
    wait ${pids[0]}
    unset pids[0]
    pids=("${pids[@]}")
  fi
done
wait

# Collect all JSON objects into array
jq -s '.' "$TMPDIR"/*.json
