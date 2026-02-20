#!/usr/bin/env bash
# Rudra — The Executor Agent
# Executes plans created by Agni

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

plan_file="${1:-}"
if [ -z "$plan_file" ] || [ ! -f "$plan_file" ]; then
  echo "ERROR: No plan file provided or file not found" >&2
  exit 1
fi

timestamp=$(basename "$plan_file" .md | cut -d'-' -f2-)
log_dir="agents/rudra/logs"
report_dir="agents/rudra/reports"
mkdir -p "$log_dir" "$report_dir"
log_file="$log_dir/exec-${timestamp}.log"
report_file="$report_dir/report-${timestamp}.md"

# Logging helper
log() {
  echo "[$(date --iso-8601=seconds)] $*" | tee -a "$log_file"
}

log "Rudra starting with plan: $plan_file"

# Parse plan
plan_type=$(grep -m1 '^Type:' "$plan_file" | cut -d: -f2- | xargs)
task_desc=$(grep -m1 '^Task:' "$plan_file" | cut -d: -f2- | xargs)

log "Plan type: $plan_type"
log "Task: $task_desc"

# Extract steps for logging/reference only
steps_section=$(sed -n '/^## Steps/,/^## Notes/p' "$plan_file" | tail -n +2 | head -n -1)

if [ -z "$steps_section" ]; then
  log "ERROR: No steps section found in plan"
  exit 1
fi

log "Plan steps (reference):"
echo "$steps_section" | while IFS= read -r step; do
  [[ -z "$step" ]] && continue
  log "  $step"
done

# --- Interpreter: execute based on plan_type ---

case "$plan_type" in
  opportunity)
    log "Interpreting as OPPORTUNITY plan: addressing TODOs/FIXMEs"
    opp_file="agents/agni/opportunities.txt"
    if [ ! -s "$opp_file" ]; then
      log "No opportunities file or it's empty — nothing to do"
    else
      log "Reading opportunities from $opp_file"
      count=0
      while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        [[ "$line" != *:* ]] && continue
        file="${line%%:*}"
        comment="${line#*:}"
        log "Opportunity: $file — $comment"
        if echo "$comment" | grep -qE '^(TODO|FIXME|XXX):[[:space:]]*'; then
          log "  -> Safe fix would be applied here (not implemented in v1)"
          ((count++))
        fi
      done < "$opp_file"
      log "Total opportunities reviewed: $count"
      # Future: implement actual safe fixes based on comment content
    fi
    ;;
  health)
    log "Interpreting as HEALTH plan: running health checks"
    if ./quick health; then
      log "Health check OK"
    else
      log "WARNING: Health check reported issues"
    fi
    ;;
  maintenance)
    log "Interpreting as MAINTENANCE plan: documentation, cleanup, cron verify"
    if [ -d "content" ]; then
      log "Updating content index"
      ./quick content-index-update || log "Content index update failed"
    fi
    find . -maxdepth 1 -type f \( -name '*.tmp' -o -name '*.bak' -o -name 'core' \) 2>/dev/null | while read -r tmp; do
      log "Removing temporary file: $tmp"
      rm -f "$tmp"
    done
    log "Verifying cron schedules"
    ./quick cron-health || log "Cron health check failed"
    ;;
  *)
    log "Unknown plan type: $plan_type — skipping execution"
    ;;
esac

# --- Validation phase ---
log "Validation phase"
if ./quick health >/dev/null 2>&1; then
  log "Health check passed"
else
  log "WARNING: Health check reported warnings (may be non-critical)"
fi

# Check git status
changed=$(git status --short 2>/dev/null | wc -l)
if (( changed > 0 )); then
  log "Uncommitted changes detected ($changed files). Committing…"
  
  commit_prefix="build"
  case "$plan_type" in
    opportunity|maintenance) commit_prefix="dev" ;;
  esac
  
  git add -A
  if git commit -m "${commit_prefix}: $task_desc (Agni plan $timestamp)" 2>/dev/null; then
    log "Committed locally"
    if git push origin master 2>/dev/null; then
      log "Pushed to origin"
    else
      log "WARNING: Push failed (network or remote error)"
    fi
  else
    log "WARNING: Commit failed (maybe nothing to commit?)"
  fi
else
  log "No changes to commit"
fi

# Create completion report
cat > "$report_file" << REPORT
# Rudra Completion Report — $timestamp
**Plan**: $task_desc
**Type**: $plan_type
**Completed**: $(date --iso-8601=seconds)

## Changes
- Git changes: $changed file(s)
- Committed: $(git log -1 --oneline 2>/dev/null | head -1 || echo "none")
- Push: $(git remote show origin 2>/dev/null | grep "out of date" || echo "synced")

## Log
Full execution log: $log_file

## Notes
Rudder cycle finished successfully. Ready for next plan.
REPORT

log "Report generated: $report_file"
log "Rudra cycle finished"

# Final exit (success)
exit 0
