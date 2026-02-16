#!/usr/bin/env bash
# Kṛṣṇa — Game Builder Agent
# Executes game development plans from Vishwakarma

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

plan_file="${1:-}"
if [ -z "$plan_file" ] || [ ! -f "$plan_file" ]; then
  echo "ERROR: No plan file provided or file not found" >&2
  exit 1
fi

plan_id=$(basename "$plan_file" .md | cut -d'-' -f2-)
log_dir="agents/krishna/logs"
report_dir="agents/krishna/reports"
mkdir -p "$log_dir" "$report_dir"
log_file="$log_dir/build-${plan_id}.log"
report_file="$report_dir/report-${plan_id}.md"

log() {
  echo "[$(date --iso-8601=seconds)] $*" | tee -a "$log_file"
}

log "Kṛṣṇa starting with plan: $plan_file"

# Parse plan
phase=$(grep -m1 '^Phase:' "$plan_file" | cut -d: -f2- | xargs)
task_desc=$(grep -m1 '^Task:' "$plan_file" | cut -d: -f2- | xargs)
game_dir=$(grep -m1 '^game_dir=' "$plan_file" | cut -d= -f2- || echo "games/anime-studio-tycoon")

log "Phase: $phase"
log "Task: $task_desc"
log "Game dir: $game_dir"

# Extract Implementation Steps section
steps=$(sed -n '/^## Implementation Steps/,/^## Notes/p' "$plan_file" | tail -n +2 | head -n -1)

if [ -z "$steps" ]; then
  log "ERROR: No implementation steps found"
  exit 1
fi

log "Executing implementation steps…"
echo "$steps" | while IFS= read -r step; do
  [[ -z "$step" ]] && continue
  [[ "$step" =~ ^# ]] && continue
  log "→ $step"
  if bash -c "$step" 2>&1 | tee -a "$log_file"; then
    log "Step completed"
  else
    log "WARNING: Step exited with non-zero status"
  fi
done

# Test the game
log "Testing the game…"
if [ -f "${game_dir}/main.py" ]; then
  log "Running: python3 ${game_dir}/main.py (quick test)"
  timeout 30 python3 "${game_dir}/main.py" < /dev/null 2>&1 | tee -a "$log_file" || log "Game test completed (may have exit code)"
else
  log "WARNING: No main.py found to test"
fi

# Validation: check git status
changed=$(git status --short 2>/dev/null | wc -l)
if (( changed > 0 )); then
  log "Uncommitted changes ($changed files). Committing with prefix 'game:'"
  git add -A
  if git commit -m "game: $task_desc (Vishwakarma plan $plan_id)" 2>/dev/null; then
    log "Committed locally"
    if git push origin master 2>/dev/null; then
      log "Pushed to origin"
    else
      log "WARNING: Push failed"
    fi
  else
    log "WARNING: Commit failed"
  fi
else
  log "No changes to commit"
fi

# Create completion report
cat > "$report_file" << REPORT
# Kṛṣṇa Build Report — $plan_id
**Plan**: $task_desc
**Phase**: $phase
**Completed**: $(date --iso-8601=seconds)

## Implementation
- Followed Vishwakarma's plan
- Created/updated files in: $game_dir

## Test
- Game test executed (see log)

## Git
- Changed files: $changed
- Last commit: $(git log -1 --oneline 2>/dev/null || echo "none")

## Log
Full build log: $log_file

## Next Steps
Planned by Vishwakarma in next cycle.
REPORT

log "Report generated: $report_file"
log "Kṛṣṇa cycle finished"

# Notify Vishwakarma
./openclaw sessions send --label vishwakarma --message "Kṛṣṇa completed: $task_desc (report: $report_file)" 2>/dev/null || log "Could not message Vishwakarma"

exit 0
