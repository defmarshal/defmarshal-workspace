#!/usr/bin/env bash
# Idea Executor — runs one pending idea per cycle
# Picks next unexecuted idea from agents/ideas/latest.json and executes steps via exec

set -uo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
IDEAS_DIR="$WORKSPACE/agents/ideas"
STATUS_FILE="$IDEAS_DIR/status.json"
IDEA_FILE="$IDEAS_DIR/latest.json"
LOG_FILE="$WORKSPACE/memory/idea-executor.log"
RUN_TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Ensure files exist
if [[ ! -f "$IDEA_FILE" ]]; then
  echo "[$RUN_TIMESTAMP] No latest ideas file found, skipping." >> "$LOG_FILE"
  # Set status idle
  echo "{\"status\":\"idle\",\"last_run\":\"$RUN_TIMESTAMP\",\"current_idea\":null}" > "$STATUS_FILE"
  exit 0
fi

# Read JSON array robustly (use jq if available, else fallback to grep)
if command -v jq &>/dev/null; then
  IDEAS_COUNT=$(jq 'length' "$IDEA_FILE")
else
  # Rough count
  IDEAS_COUNT=$(grep -o '"slug":' "$IDEA_FILE" | wc -l)
fi

if [[ $IDEAS_COUNT -eq 0 ]]; then
  echo "[$RUN_TIMESTAMP] No ideas to execute." >> "$LOG_FILE"
  echo "{\"status\":\"idle\",\"last_run\":\"$RUN_TIMESTAMP\",\"current_idea\":null}" > "$STATUS_FILE"
  exit 0
fi

# Find next pending idea (first where .executed != true or field missing)
NEXT_SLUG=""
if command -v jq &>/dev/null; then
  # Use jq to pick index of first not executed
  IDX=$(jq -r 'to_entries[] | select((.value.executed // false) == false) | .key' "$IDEA_FILE" | head -1)
  if [[ -n "$IDX" ]]; then
    NEXT_SLUG=$(jq -r ".[$IDX].slug" "$IDEA_FILE")
    NEXT_IDX=$IDX
  fi
else
  # Fallback: read the raw JSON and look for "executed":false or no executed field
  # This is a bit hacky but works for basic JSON
  MATCH=$(grep -n '"slug":' -m1 "$IDEA_FILE")
  # Actually easier: assume first non-executed; we'll need to grep for executed: false. Let's skip fallback complexity and require jq.
  echo "[$RUN_TIMESTAMP] jq not available; install jq for executor." >> "$LOG_FILE"
  exit 1
fi

if [[ -z "$NEXT_SLUG" ]]; then
  echo "[$RUN_TIMESTAMP] All ideas executed." >> "$LOG_FILE"
  echo "{\"status\":\"idle\",\"last_run\":\"$RUN_TIMESTAMP\",\"current_idea\":null}" > "$STATUS_FILE"
  exit 0
fi

# Update status to executing
RUN_ID="exec-$NEXT_SLUG-$(date -u +%s)"
echo "{\"status\":\"executing\",\"last_run\":\"$RUN_TIMESTAMP\",\"current_idea\":\"$NEXT_SLUG\",\"run_id\":\"$RUN_ID\"}" > "$STATUS_FILE"

log() {
  echo "[$(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)] $*" >> "$LOG_FILE"
}

log "Executor starting on idea: $NEXT_SLUG (index $NEXT_IDX)"

# Fetch the idea's details
TITLE=$(jq -r ".[$NEXT_IDX].title" "$IDEA_FILE")
DESCRIPTION=$(jq -r ".[$NEXT_IDX].description" "$IDEA_FILE")
STEPS=$(jq -r ".[$NEXT_IDX].steps[]" "$IDEA_FILE")
CATEGORY=$(jq -r ".[$NEXT_IDX].category // \"misc\"" "$IDEA_FILE")
FILES_TOUCH=$(jq -r ".[$NEXT_IDX].files_to_touch // [] | join(\",\")" "$IDEA_FILE")

log "Title: $TITLE"
log "Category: $CATEGORY"
log "Steps:"
while IFS= read -r step; do
  [[ -z "$step" ]] && continue
  log "  - $step"
done <<< "$STEPS"

# Execute each step in order, capturing output and exit status
EXEC_LOG="$WORKSPACE/agents/ideas/exec-$NEXT_SLUG-$(date -u +%Y%m%d_%H%M%S).log"
: > "$EXEC_LOG"

STEP_RESULTS=()
STEP_COUNT=$(jq ".[$NEXT_IDX].steps | length" "$IDEA_FILE")
for ((s=0; s<STEP_COUNT; s++)); do
  STEP_CMD=$(jq -r ".[$NEXT_IDX].steps[$s]" "$IDEA_FILE")
  log "Step $((s+1)): $STEP_CMD"
  echo "[$(date -u +%Y-%m-%d_%H:%M:%S UTC)] START: $STEP_CMD" >> "$EXEC_LOG"
  if eval "$STEP_CMD" >> "$EXEC_LOG" 2>&1; then
    STATUS="success"
  else
    STATUS="failed"
    log "Step $((s+1)) failed with exit code $?"
    # Continue to next steps? Or abort? Let's continue but record failure.
  fi
  echo "[$(date -u +%Y-%m-%d_%H:%M:%S UTC)] END: $STEP_CMD — $STATUS" >> "$EXEC_LOG"
  STEP_RESULTS+=("$STATUS")
done

# Determine overall result: all success => success, any failure => partial/failed
FAILED_COUNT=0
for r in "${STEP_RESULTS[@]}"; do
  [[ "$r" == "failed" ]] && ((FAILED_COUNT++))
done

if [[ $FAILED_COUNT -eq 0 ]]; then
  RESULT="success"
else
  if [[ $FAILED_COUNT -lt ${#STEP_RESULTS[@]} ]]; then
    RESULT="partial"
  else
    RESULT="failed"
  fi
fi

log "Idea execution completed: $RESULT ($FAILED_COUNT failures)"

# Mark idea as executed in latest.json
# We'll update the .executed field to true and add result and log path
TMP_JSON=$(mktemp)
jq ".[$NEXT_IDX].executed = true | .[$NEXT_IDX].execution_result = \"$RESULT\" | .[$NEXT_IDX].executed_at = \"$RUN_TIMESTAMP\" | .[$NEXT_IDX].execution_log = \"$EXEC_LOG\"" "$IDEA_FILE" > "$TMP_JSON" && mv "$TMP_JSON" "$IDEA_FILE"

# Update status back to idle (we keep current_idea for info)
echo "{\"status\":\"idle\",\"last_run\":\"$RUN_TIMESTAMP\",\"current_idea\":\"$NEXT_SLUG\",\"result\":\"$RESULT\",\"run_id\":\"$RUN_ID\"}" > "$STATUS_FILE"

log "Executor cycle complete."

exit 0
