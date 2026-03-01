#!/usr/bin/env bash
# Agni — The Brainstormer + Executor
# Creates a plan and directly runs rudra-executor.sh

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOG="agents/agni/agni.log"
mkdir -p agents/agni
echo "[$(date --iso-8601=seconds)] Agni cycle starting" >> "$LOG"

# Avoid overlap: use flock lockfile
LOCKFILE="agents/agni/agni.lock"
mkdir -p "$(dirname "$LOCKFILE")"
if [ -e "$LOCKFILE" ]; then
  lock_age=$(( $(date +%s) - $(stat -c %Y "$LOCKFILE" 2>/dev/null || echo 0) ))
  if [ "$lock_age" -gt 3600 ]; then
    echo "[$(date --iso-8601=seconds)] Removing stale Agni lock (age: $((lock_age/60)) min)" >> "$LOG"
    rm -f "$LOCKFILE"
  fi
fi
exec 200>"$LOCKFILE"
if ! flock -n 200; then
  echo "[$(date --iso-8601=seconds)] Another Agni running — exiting" >> "$LOG"
  exit 0
fi

# Do not spawn if a Rudra is already executing
if pgrep -f "rudra-executor.sh" > /dev/null; then
  echo "[$(date --iso-8601=seconds)] Rudra already running — skipping this cycle" >> "$LOG"
  exit 0
fi

# --- Brainstorming Phase ---
echo "[$(date --iso-8601=seconds)] Brainstorming phase…" >> "$LOG"

grep -r "TODO\|FIXME\|XXX" agents/ quick/ research/ content/ 2>/dev/null | head -20 > agents/agni/opportunities.txt || true

plan_type="health"
task_desc="Workspace health check and cleanup"
if [ -s agents/agni/opportunities.txt ]; then
  plan_type="opportunity"
  task_desc="Address found opportunities (TODOs/FIXMEs)"
fi

timestamp=$(date +%Y-%m-%d_%H%M)
plan_dir="agents/agni/plans"
mkdir -p "$plan_dir"
plan_file="$plan_dir/plan-${timestamp}.md"

cat > "$plan_file" << PLAN
# Agni Plan — $timestamp
Type: $plan_type
Task: $task_desc
Generated: $(date --iso-8601=seconds)

## Objective
$task_desc

## Context
- Workspace health: $(./quick status 2>/dev/null | head -1 || echo "unknown")
- Git state: $(git status --short 2>/dev/null | wc -l) files changed
- Active agents: $(grep -c '\[.*\]' active-tasks.md 2>/dev/null || echo 0)

## Steps (for Rudra)
1. Review this plan and verify current workspace state.
2. Execute tasks appropriate to plan type:
   - if opportunity: read agents/agni/opportunities.txt and address them (safe fixes only)
   - if health: run quick health and fix any non-critical issues (stale logs, missing indexes)
   - if maintenance: update documentation, clean temporary files, verify cron jobs
3. Run quick verify (if available)
4. Ensure no temporary or backup files left behind
5. Commit changes with prefix "dev:" or "build:"
6. Write completion report to agents/rudra/reports/report-${timestamp}.md

## Notes
- If uncertain about a step, skip it and note in report.
- Do not perform disruptive actions (mass deletions, system upgrades).
PLAN

echo "[$(date --iso-8601=seconds)] Plan created: $plan_file" >> "$LOG"

# --- Execute Rudra directly ---
echo "[$(date --iso-8601=seconds)] Running rudra-executor…" >> "$LOG"

if [ -f agents/rudra-executor.sh ]; then
  bash agents/rudra-executor.sh "$plan_file" >> "$LOG" 2>&1
  echo "[$(date --iso-8601=seconds)] Rudra completed" >> "$LOG"
else
  echo "[$(date --iso-8601=seconds)] WARNING: rudra-executor.sh not found — skipping execution" >> "$LOG"
fi

echo "[$(date --iso-8601=seconds)] Agni cycle complete" >> "$LOG"
