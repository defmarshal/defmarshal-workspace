#!/bin/bash
set -u
if [ -f "/home/ubuntu/.openclaw/workspace/.env" ]; then
  export $(cat /home/ubuntu/.openclaw/workspace/.env | grep -v '^#' | xargs)
fi
BATCH_SIZE=${BATCH_SIZE:-100}
PAGES_PER_RUN=${PAGES_PER_RUN:-4}
MAX_PARALLEL=${MAX_PARALLEL:-5}
DRY_RUN=${DRY_RUN:-0}
MARK_AS_READ=${MARK_AS_READ:-0}
API_KEY="${MATON_API_KEY:-}"
STATE_FILE="/home/ubuntu/.openclaw/workspace/memory/email-categorizer.state"
LOG_FILE="/home/ubuntu/.openclaw/workspace/memory/email-categorizer.log"
LABEL_CACHE_FILE="/home/ubuntu/.openclaw/workspace/memory/email-labels.cache"

# Category to label name mapping
declare -A CATEGORY_LABELS=(
  ["banking"]="Categorized/Banking"
  ["alerts"]="Categorized/Alerts"
  ["work"]="Categorized/Work"
  ["newsletters"]="Categorized/Newsletters"
  ["hr"]="Categorized/HR"
  ["personal"]="Categorized/Personal"
)

log() { echo "[$(date -u)] $*" | tee -a "$LOG_FILE" >&2; }

load_state() { if [ -f "$STATE_FILE" ]; then source "$STATE_FILE" 2>/dev/null || true; fi; : "${NEXT_PAGE_TOKEN:=}"; }
save_state() { echo "NEXT_PAGE_TOKEN=$NEXT_PAGE_TOKEN" > "$STATE_FILE"; }

# Load label cache into memory
declare -A LABEL_ID_CACHE
load_label_cache() {
  LABEL_ID_CACHE=()
  if [ -f "$LABEL_CACHE_FILE" ]; then
    while IFS='=' read -r name id; do
      [ -n "$name" ] && [ -n "$id" ] && LABEL_ID_CACHE["$name"]="$id"
    done < "$LABEL_CACHE_FILE"
  fi
}

# Save label cache to disk
save_label_cache() {
  mkdir -p "$(dirname "$LABEL_CACHE_FILE")"
  : > "$LABEL_CACHE_FILE"
  for name in "${!LABEL_ID_CACHE[@]}"; do
    echo "$name=${LABEL_ID_CACHE[$name]}" >> "$LABEL_CACHE_FILE"
  done
}

# Get cached label ID if available
get_cached_label_id() {
  local label_name="$1"
  echo "${LABEL_ID_CACHE[$label_name]:-}"
}

# Cache a label ID
cache_label_id() {
  local label_name="$1"
  local label_id="$2"
  LABEL_ID_CACHE["$label_name"]="$label_id"
  save_label_cache
}

# Ensure label exists, create if missing, return label ID
# Uses Gmail API: users.labels
ensure_label_exists() {
  local category="$1"
  local label_name="${CATEGORY_LABELS[$category]:-}"
  
  if [ -z "$label_name" ]; then
    log "ERROR: Unknown category '$category'"
    return 1
  fi
  
  # Check cache first
  local cached_id
  cached_id=$(get_cached_label_id "$label_name")
  if [ -n "$cached_id" ]; then
    echo "$cached_id"
    return 0
  fi
  
  # Check if API key is available
  if [ -z "$API_KEY" ]; then
    log "WARN: No API key, cannot create label '$label_name'"
    return 1
  fi
  
  # Search for existing label
  log "Searching for label '$label_name'..."
  local list_resp
  list_resp=$(curl -s -f -H "Authorization: Bearer $API_KEY" \
    "https://gateway.maton.ai/google-mail/gmail/v1/users/me/labels" 2>/dev/null)
  
  if [ -n "$list_resp" ]; then
    # Try to find the label in the response
    local found_id
    found_id=$(echo "$list_resp" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for label in data.get('labels', []):
        if label.get('name') == '$label_name':
            print(label.get('id', ''))
            break
except:
    pass
" 2>/dev/null)
    
    if [ -n "$found_id" ]; then
      log "Found existing label '$label_name' (id: $found_id)"
      cache_label_id "$label_name" "$found_id"
      echo "$found_id"
      return 0
    fi
  fi
  
  # Create the label
  log "Creating label '$label_name'..."
  local create_resp
  create_resp=$(curl -s -f -X POST \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$label_name\", \"labelListVisibility\": \"labelShow\", \"messageListVisibility\": \"show\"}" \
    "https://gateway.maton.ai/google-mail/gmail/v1/users/me/labels" 2>/dev/null)
  
  if [ -n "$create_resp" ]; then
    local created_id
    created_id=$(echo "$create_resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id',''))" 2>/dev/null)
    if [ -n "$created_id" ]; then
      log "Created label '$label_name' (id: $created_id)"
      cache_label_id "$label_name" "$created_id"
      echo "$created_id"
      return 0
    fi
  fi
  
  log "ERROR: Failed to create/find label '$label_name'"
  return 1
}

# Apply label to a message using Gmail API: users.messages.modify
# Handles rate limits with simple retry logic
apply_label() {
  local message_id="$1"
  local category="$2"
  local label_name="${CATEGORY_LABELS[$category]:-}"
  
  if [ -z "$label_name" ]; then
    log "ERROR: Cannot apply label - unknown category '$category' for message $message_id"
    return 1
  fi
  
  # Check if API key is available
  if [ -z "$API_KEY" ]; then
    log "WARN: No API key, skipping label application for message $message_id"
    return 1
  fi
  
  # Dry run mode
  if [ "$DRY_RUN" = "1" ]; then
    log "DRY-RUN: Would label message $message_id as $category ($label_name)"
    return 0
  fi
  
  # Get label ID
  local label_id
  label_id=$(ensure_label_exists "$category")
  if [ -z "$label_id" ]; then
    log "ERROR: Could not get label ID for category '$category'"
    return 1
  fi
  
  # Build request body
  local add_labels="\"$label_id\""
  local remove_labels=""
  
  # Optionally mark as read
  if [ "$MARK_AS_READ" = "1" ]; then
    remove_labels="\"UNREAD\""
  fi
  
  # Retry logic for rate limits
  local max_retries=3
  local retry_delay=1
  local attempt=0
  
  while [ $attempt -lt $max_retries ]; do
    attempt=$((attempt + 1))
    
    # Call Gmail API: users.messages.modify (do not use -f; handle responses manually)
    local modify_resp
    modify_resp=$(curl -s -X POST \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"addLabelIds\": [$add_labels], \"removeLabelIds\": [$remove_labels]}" \
      "https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/$message_id/modify" 2>/dev/null) || true
    
    # Check for rate limit error (retryable)
    if echo "$modify_resp" | grep -qi "rateLimitExceeded\|429"; then
      log "WARN: Rate limit hit for message $message_id, retrying in ${retry_delay}s (attempt $attempt/$max_retries)"
      sleep $retry_delay
      retry_delay=$((retry_delay * 2))
      continue
    fi
    
    # Success: response contains id field
    if echo "$modify_resp" | grep -q '"id"'; then
      log "Labeled message $message_id as $category ($label_name)"
      return 0
    fi
    
    # Other error, don't retry
    log "ERROR: Failed to label message $message_id: $modify_resp"
    return 1
  done
  
  log "ERROR: Max retries exceeded for message $message_id"
  return 1
}

categorize() {
  local from="$1" subj="$2"
  local lf="${from,,}" ls="${subj,,}"
  if echo "$lf" | grep -qE 'bca|bank|transaction|statement'; then echo "banking"
  elif echo "$ls" | grep -qE 'alert|error|cpu|disk|monitor'; then echo "alerts"
  elif echo "$ls" | grep -qE 'meeting|sprint|planning|standup|review'; then echo "work"
  elif echo "$ls" | grep -qE 'newsletter|digest|promo|marketing|subscribe'; then echo "newsletters"
  elif echo "$ls" | grep -qE 'timesheet|hr|payroll|leave'; then echo "hr"
  elif echo "$lf" | grep -qE '@company\.com|@org|@work'; then echo "work"
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
  declare -A cnt; declare -A samp; declare -A labeled_cnt; local total=0
  for f in "$TMP"/*.json; do
    [ -f "$f" ] || continue
    id=$(basename "$f" .json)
    from=$(python3 -c "import json; d=json.load(open('$f')); h=[h for h in d.get('payload',{}).get('headers',[]) if h['name'].lower()=='from']; print(h[0]['value'] if h else '')" 2>/dev/null)
    subj=$(python3 -c "import json; d=json.load(open('$f')); h=[h for h in d.get('payload',{}).get('headers',[]) if h['name'].lower()=='subject']; print(h[0]['value'] if h else '')" 2>/dev/null)
    cat=$(categorize "$from" "$subj"); cnt["$cat"]=$(( ${cnt["$cat"]:-0} + 1 ))
    [ -z "${samp["$cat"]:-}" ] && samp["$cat"]="$subj|$from"
    
    # Apply label after categorization
    if apply_label "$id" "$cat"; then
      labeled_cnt["$cat"]=$(( ${labeled_cnt["$cat"]:-0} + 1 ))
    fi
    
    total=$((total+1))
  done; rm -rf "$TMP"
  
  # Build log line with labeling info
  local line="Batch $total:"
  for cat in "${!cnt[@]}"; do
    line="$line $cat=${cnt[$cat]}"
    if [ -n "${labeled_cnt[$cat]:-}" ]; then
      line="$line(labeled:${labeled_cnt[$cat]})"
    fi
  done
  log "$line"
  
  summary="📧 Email batch: $total unread"
  for cat in "${!cnt[@]}"; do
    summary="$summary\n  - $cat: ${cnt[$cat]}"
    if [ -n "${labeled_cnt[$cat]:-}" ]; then
      summary="$summary (labeled: ${labeled_cnt[$cat]})"
    fi
  done
  openclaw message send --to last --text "$summary" 2>/dev/null || log "Failed to send Telegram"
  [ -z "$next_token" ] && echo "DONE" || echo "$next_token"
}

log "Starting sweep (batch=$BATCH_SIZE, pages=$PAGES_PER_RUN, dry_run=$DRY_RUN, mark_as_read=$MARK_AS_READ)"
load_state
load_label_cache

# Pre-create all category labels if API key is available
if [ -n "$API_KEY" ] && [ "$DRY_RUN" != "1" ]; then
  log "Ensuring category labels exist..."
  for category in "${!CATEGORY_LABELS[@]}"; do
    ensure_label_exists "$category" >/dev/null 2>&1 || true
  done
fi

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
