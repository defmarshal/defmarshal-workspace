#!/bin/bash
set -euo pipefail

# This is a long-running agent that continuously categorizes emails.
# The agent manager expects a loop that does work then sleeps.

# Load .env
if [ -f "/home/ubuntu/.openclaw/workspace/.env" ]; then
  export $(cat /home/ubuntu/.openclaw/workspace/.env | grep -v '^#' | xargs)
fi

# Configurable via env
INTERVAL_SECONDS=${EMAIL_CATEGORIZER_INTERVAL:-900}  # 15 min default
MAX_UNREAD=${MAX_UNREAD:-50}

API_KEY="${MATON_API_KEY:?MATON_API_KEY not set}"
CONN_ID="${CONNECTION_ID:?CONNECTION_ID not set}"

LOG_FILE="/home/ubuntu/.openclaw/workspace/memory/email-categorizer.log"

log() {
  echo "[$(date -u)] $*" | tee -a "$LOG_FILE"
}

categorize() {
  local from="$1" subject="$2" snippet="$3"
  local lfrom="${from,,}" lsubj="${subject,,}" lsnip="${snippet,,}"
  if echo "$lfrom" | grep -qE 'bca|bank|transaction|statement'; then echo "banking"
  elif echo "$lsubj" | grep -qE 'alert|error|cpu|disk|monitor'; then echo "alerts"
  elif echo "$lsubj" | grep -qE 'meeting|sprint|planning|standup|review'; then echo "work"
  elif echo "$lsubj" | grep -qE 'newsletter|digest|promo|marketing|subscribe'; then echo "newsletters"
  elif echo "$lfrom" | grep -qE '@company\.com|@org|@work'; then echo "work"
  elif echo "$lsubj" | grep -qE 'timesheet|hr|payroll|leave'; then echo "hr"
  else echo "personal"; fi
}

run_once() {
  log "Fetching up to $MAX_UNREAD unread..."
  list_url="https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?q=is:unread&maxResults=$MAX_UNREAD"
  msg_ids=$(curl -s -H "Authorization: Bearer $API_KEY" "$list_url" | python3 -c "import json,sys; d=json.load(sys.stdin); print(' '.join([m['id'] for m in d.get('messages',[])]))")
  if [ -z "$msg_ids" ]; then log "No unread emails"; return; fi

  TMPDIR=$(mktemp -d)
  trap 'rm -rf "$TMPDIR"' EXIT

  for id in $msg_ids; do
    (
      resp=$(curl -s -H "Authorization: Bearer $API_KEY" "https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/$id?format=full")
      from=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); h=[h for h in d.get('payload',{}).get('headers',[]) if h['name'].lower()=='from']; print(h[0]['value'] if h else '')")
      subject=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); h=[h for h in d.get('payload',{}).get('headers',[]) if h['name'].lower()=='subject']; print(h[0]['value'] if h else '')")
      snippet=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('snippet',''))")
      cat > "$TMPDIR/$id.json" <<EOF
{"messageId":"$id","from":$(python3 -c "import json; print(json.dumps('$from'))"),"subject":$(python3 -c "import json; print(json.dumps('$subject'))"),"snippet":$(python3 -c "import json; print(json.dumps('$snippet'))")}
EOF
    ) &
    pids+=($!)
    if [ ${#pids[@]} -ge 5 ]; then wait ${pids[0]} 2>/dev/null || true; unset pids[0]; pids=("${pids[@]}"); fi
  done
  wait 2>/dev/null || true

  declare -A counts; declare -A samples; total=0
  for id in $msg_ids; do
    if [ -f "$TMPDIR/$id.json" ]; then
      from=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('from',''))" < "$TMPDIR/$id.json")
      subject=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('subject',''))" < "$TMPDIR/$id.json")
      snippet=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('snippet',''))" < "$TMPDIR/$id.json")
      cat=$(categorize "$from" "$subject" "$snippet")
      counts["$cat"]=$(( ${counts["$cat"]} + 1 ))
      if [ -z "${samples[$cat]:-}" ]; then samples["$cat"]="$(printf '%s|%s' "$subject" "$from")"; fi
      total=$((total+1))
    fi
  done

  summary="📧 Email Categorizer ($(date -u)): $total unread"
  for cat in "${!counts[@]}"; do
    summary="$summary\n  - $cat: ${counts[$cat]}"
    if [ -n "${samples[$cat]:-}" ]; then
      IFS='|' read -r subj from <<< "${samples[$cat]}"
      summary="$summary (e.g., \"$subj\" from $from)"
    fi
  done

  log "$summary"
  openclaw message send --to last --text "$summary" 2>/dev/null || log "Failed to send Telegram"
}

log "Starting email categorizer agent (interval ${INTERVAL_SECONDS}s)"
while true; do
  run_once
  log "Sleeping ${INTERVAL_SECONDS}s"
  sleep "$INTERVAL_SECONDS"
done
