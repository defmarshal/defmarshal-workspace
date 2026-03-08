#!/bin/bash
set -u
if [ -f "/home/ubuntu/.openclaw/workspace/.env" ]; then
  export $(cat /home/ubuntu/.openclaw/workspace/.env | grep -v '^#' | xargs)
fi
BATCH_SIZE=${BATCH_SIZE:-500}
PAGES_PER_RUN=${PAGES_PER_RUN:-4}
MAX_PARALLEL=${MAX_PARALLEL:-5}
API_KEY="${MATON_API_KEY:?MATON_API_KEY not set}"
STATE_FILE="/home/ubuntu/.openclaw/workspace/memory/email-categorizer.state"
LOG_FILE="/home/ubuntu/.openclaw/workspace/memory/email-categorizer.log"
log() { echo "[$(date -u)] $*" | tee -a "$LOG_FILE"; }
load_state() { if [ -f "$STATE_FILE" ]; then source "$STATE_FILE" 2>/dev/null || true; fi; : "${NEXT_PAGE_TOKEN:=}"; }
save_state() { echo "NEXT_PAGE_TOKEN=$NEXT_PAGE_TOKEN" > "$STATE_FILE"; }
categorize() {
  local from="$1" subj="$2"
  local lf="${from,,}" ls="${subj,,}"
  if echo "$lf" | grep -qE 'bca|bank|transaction|statement'; then echo "banking"
  elif echo "$ls" | grep -qE 'alert|error|cpu|disk|monitor'; then echo "alerts"
  elif echo "$ls" | grep -qE 'meeting|sprint|planning|standup|review'; then echo "work"
  elif echo "$ls" | grep -qE 'newsletter|digest|promo|marketing|subscribe'; then echo "newsletters"
  elif echo "$lf" | grep -qE '@company\.com|@org|@work'; then echo "work"
  elif echo "$ls" | grep -qE 'timesheet|hr|payroll|leave'; then echo "hr"
  else echo "personal"; fi
}
process_batch() {
  local page_token="$1"
  local url="https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?q=is:unread&maxResults=$BATCH_SIZE"
  [ -n "$page_token" ] && url="$url&pageToken=$page_token"
  log "Fetch: $url"
  resp=$(curl -s -f -H "Authorization: Bearer $API_KEY" "$url")
  if [ $? -ne 0 ] || [ -z "$resp" ]; then log "curl error"; echo "NO_MORE"; return; fi
  if command -v jq &>/dev/null; then
    msg_ids=$(echo "$resp" | jq -r '.messages[].id' 2>/dev/null | tr '\n' ' ')
    next_token=$(echo "$resp" | jq -r '.nextPageToken // empty' 2>/dev/null)
  else
    msg_ids=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(' '.join(m['id'] for m in d.get('messages',[])))" 2>/dev/null)
    next_token=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('nextPageToken',''))" 2>/dev/null)
  fi
  [ -n "$msg_ids" ] || { echo "NO_MORE"; return; }
  TMP=$(mktemp -d)
  for id in $msg_ids; do
    ( curl -s -f -H "Authorization: Bearer $API_KEY" "https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/$id?format=full" > "$TMP/$id.json" ) &
    if [ $(jobs -r | wc -l) -ge $MAX_PARALLEL ]; then wait -n 2>/dev/null || true; fi
  done; wait 2>/dev/null || true
  declare -A cnt; declare -A samp; local total=0
  for f in "$TMP"/*.json; do
    [ -f "$f" ] || continue
    id=$(basename "$f" .json)
    from=$(python3 -c "import json; d=json.load(open('$f')); h=[h for h in d.get('payload',{}).get('headers',[]) if h['name'].lower()=='from']; print(h[0]['value'] if h else '')" 2>/dev/null)
    subj=$(python3 -c "import json; d=json.load(open('$f')); h=[h for h in d.get('payload',{}).get('headers',[]) if h['name'].lower()=='subject']; print(h[0]['value'] if h else '')" 2>/dev/null)
    cat=$(categorize "$from" "$subj"); cnt["$cat"]=$(( ${cnt["$cat"]:-0} + 1 ))
    [ -z "${samp["$cat"]:-}" ] && samp["$cat"]="$subj|$from"; total=$((total+1))
  done; rm -rf "$TMP"
  local line="Batch $total:"; for cat in "${!cnt[@]}"; do line="$line $cat=${cnt[$cat]}"; done; log "$line"
  summary="📧 Email batch: $total unread"
  for cat in "${!cnt[@]}"; do summary="$summary\n  - $cat: ${cnt[$cat]}"; done
  openclaw message send --to last --text "$summary" 2>/dev/null || log "Failed to send Telegram"
  [ -z "$next_token" ] && echo "DONE" || echo "$next_token"
}
log "Starting sweep (batch=$BATCH_SIZE, pages=$PAGES_PER_RUN)"
load_state
pages=0
token="${NEXT_PAGE_TOKEN:-}"
while [ $pages -lt $PAGES_PER_RUN ]; do
  result=$(process_batch "$token"); log "Result: $result"
  if [ "$result" = "NO_MORE" ] || [ -z "$result" ]; then NEXT_PAGE_TOKEN=""; break
  elif [ "$result" = "DONE" ]; then NEXT_PAGE_TOKEN=""; break
  else token="$result"; pages=$((pages+1)); fi
done
NEXT_PAGE_TOKEN="${token:-}"; save_state
log "Finished: processed $pages pages. Next token: ${NEXT_PAGE_TOKEN:-none}"