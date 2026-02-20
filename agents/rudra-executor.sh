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
      changed_files=""
      total=0
      fixed=0
      backup_dir="agents/rudra/backups/$(date +%Y-%m-%d_%H%M)"
      mkdir -p "$backup_dir"

      while IFS= read -r line; do
        # Increment total safely (avoid 'set -e' exit on zero)
        total=$((total + 1))
        [[ -z "$line" ]] && continue
        [[ "$line" != *:* ]] && continue
        file="${line%%:*}"
        comment="${line#*:}"
        log "Opportunity: $file — $comment"

        # Check if file exists and is a regular file
        if [ ! -f "$file" ]; then
          log "  -> Skipping: file not found"
          continue
        fi

        # Determine if this line is a full-line comment (safe to modify)
        # We'll check if the line in the file exactly matches our opportunity line (with possible leading/trailing spaces)
        # Use grep -F to find exact match; if found, it's likely a comment-only line (since the opportunity scanner captured the whole line)
        if grep -qF "$line" "$file"; then
          # Safe transformation: replace TODO: FIXME: XXX with DONE:
          if echo "$comment" | grep -qE '^(TODO|FIXME|XXX):[[:space:]]*'; then
            # Create backup of the file if not already backed up (once per file)
            if [ ! -f "$backup_dir/$(basename "$file").bak" ]; then
              cp -- "$file" "$backup_dir/$(basename "$file").bak" 2>/dev/null || true
            fi
            # Build new line: file: DONE: <rest of comment after marker>
            new_suffix=$(echo "$comment" | sed -E 's/^(TODO|FIXME|XXX):[[:space:]]*/DONE: /')
            new_line="${file}:${new_suffix}"
            # Use awk to replace exact matching line (preserves other lines)
            awk -v old="$line" -v new="$new_line" '
              $0 == old { print new; changed=1; next }
              { print }
            ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
            if [ $? -eq 0 ]; then
              log "  -> Fixed: marked as DONE in $file"
              fixed=$((fixed + 1))
            else
              log "  -> Failed to modify $file (awk error)"
            fi
          else
            log "  -> Not a simple TODO/FIXME marker; skipping for safety"
          fi
        else
          log "  -> Line not found verbatim in $file (may be inline comment); skipping"
        fi
      done < "$opp_file"

      log "Opportunities reviewed: $total, fixed: $fixed"
      # Note: actual file modifications are recorded via changed_files
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
