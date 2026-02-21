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
  echo "[$(date -u +"%Y-%m-%d_%H:%M:%S UTC")] START: $STEP_CMD" >> "$EXEC_LOG"
  if eval "$STEP_CMD" >> "$EXEC_LOG" 2>&1; then
    STATUS="success"
  else
    STATUS="failed"
    log "Step $((s+1)) failed with exit code $?"
    # Continue to next steps? Or abort? Let's continue but record failure.
  fi
  echo "[$(date -u +"%Y-%m-%d_%H:%M:%S UTC")] END: $STEP_CMD — $STATUS" >> "$EXEC_LOG"
  STEP_RESULTS+=("$STATUS")
done

# ------------------------------------------------------------
# Quality validation: ensure idea produced meaningful changes
# Reject placeholder commits (only touched 'quick' or no changes)
# ------------------------------------------------------------
validate_idea_execution() {
  local slug="$1"
  local idx="$2"
  local log_ref="$EXEC_LOG"

  # Check if there's a recent commit on current branch matching this idea
  # We expect the last commit message to contain the idea title/slug
  local last_msg
  last_msg=$(git log -1 --oneline --decorate-refs-exclude="refs/heads/idea/*" 2>/dev/null || git log -1 --oneline)

  # Verify it's our commit by checking slug presence
  if [[ "$last_msg" != *"$slug"* ]] && [[ "$last_msg" != *"$TITLE"* ]]; then
    # No matching commit found; could be that steps didn't commit
    echo "VALIDATION: No matching commit found for idea '$slug'. Last: $last_msg" | tee -a "$log_ref"
    return 1  # reject
  fi

  # Get commit stats for the last commit
  local stats
  stats=$(git show --stat --pretty="" HEAD 2>/dev/null)
  if [[ -z "$stats" ]]; then
    echo "VALIDATION: Could not get stats for last commit" | tee -a "$log_ref"
    return 1
  fi

  # Count insertions/deletions excluding changes to 'quick'
  # git show --stat format: " file | N changes" but we can use --shortstat for numeric
  local shortstats
  shortstats=$(git show --shortstat HEAD 2>/dev/null)

  # Extract total insertions/deletions
  local ins del
  ins=$(echo "$shortstats" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
  del=$(echo "$shortstats" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo "0")
  # Ensure numeric
  ins=${ins:-0}
  del=${del:-0}

  # Check if all changes are to 'quick' only
  local changed_files
  changed_files=$(git diff --name-only HEAD~1 HEAD 2>/dev/null)

  local only_quick=true
  if [[ -n "$changed_files" ]]; then
    while IFS= read -r f; do
      [[ "$f" == "quick" ]] && continue
      # Also ignore empty lines
      [[ -z "$f" ]] && continue
      # Some file changed besides quick
      only_quick=false
      break
    done <<< "$changed_files"
  else
    # No changed files detected (maybe empty commit)
    only_quick=true
  fi

  if [[ "$only_quick" == "true" ]] && (( ins < 5 && del < 5 )); then
    echo "VALIDATION FAILED: Only 'quick' modified or no significant changes (ins=$ins, del=$del). Rejecting idea." | tee -a "$log_ref"
    return 1
  fi

  # Additional heuristic: at least one substantive file (extensions) should be changed
  local substantive_ext_regex='\.(sh|md|ts|js|json|yml|yaml|py|rb|go|rs|c|cpp|h|txt|html|css)$'
  local has_substantive=false
  if [[ -n "$changed_files" ]]; then
    while IFS= read -r f; do
      [[ "$f" == "quick" ]] && continue
      if echo "$f" | grep -qE "$substantive_ext_regex"; then
        has_substantive=true
        break
      fi
    done <<< "$changed_files"
  fi

  if [[ "$has_substantive" == "false" ]]; then
    echo "VALIDATION FAILED: No substantive source files modified (only quick or non-code files). Rejecting." | tee -a "$log_ref"
    return 1
  fi

  echo "VALIDATION PASSED: substantive changes detected (ins=$ins, del=$del, files=${#changed_files[@]})" | tee -a "$log_ref"
  return 0
}

# ------------------------------------------------------------
# Execution steps already completed. Now validate before marking executed.
# ------------------------------------------------------------
log "Execution steps finished. Validating outcome..."
VALIDATION_PASSED=0
if validate_idea_execution "$NEXT_SLUG" "$NEXT_IDX"; then
  VALIDATION_PASSED=1
else
  VALIDATION_PASSED=0
fi

# Determine overall result considering validation
if [[ $FAILED_COUNT -eq 0 && $VALIDATION_PASSED -eq 1 ]]; then
  FINAL_RESULT="success"
elif [[ $VALIDATION_PASSED -eq 0 ]]; then
  FINAL_RESULT="rejected"
  log "Idea rejected by quality validation."
  # Revert the commit(s) made by this idea
  # We'll revert the most recent commit if it matches our slug
  git revert --no-edit HEAD 2>/dev/null || true
  # Ensure we don't leave the branch in a weird state; stay on original branch
  # (We might be on a feature branch created by the idea)
else
  FINAL_RESULT="partial"
fi

# Mark idea as executed (or rejected) in latest.json with final result
TMP_JSON=$(mktemp)
jq ".[$NEXT_IDX].executed = true | .[$NEXT_IDX].execution_result = \"$FINAL_RESULT\" | .[$NEXT_IDX].executed_at = \"$RUN_TIMESTAMP\" | .[$NEXT_IDX].execution_log = \"$EXEC_LOG\" | .[$NEXT_IDX].validated = true" "$IDEA_FILE" > "$TMP_JSON" && mv "$TMP_JSON" "$IDEA_FILE"

# Update status back to idle (we keep current_idea for info)
echo "{\"status\":\"idle\",\"last_run\":\"$RUN_TIMESTAMP\",\"current_idea\":\"$NEXT_SLUG\",\"result\":\"$FINAL_RESULT\",\"run_id\":\"$RUN_ID\"}" > "$STATUS_FILE"

log "Executor cycle complete."

exit 0
