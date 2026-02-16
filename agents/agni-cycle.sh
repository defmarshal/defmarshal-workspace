#!/usr/bin/env bash
# Agni — The Brainstormer Agent
# Spawns Rudra to execute plans

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOG="agents/agni/agni.log"
mkdir -p agents/agni
echo "[$(date --iso-8601=seconds)] Agni cycle starting" >> "$LOG"

# Respect quiet hours (23:00-08:00 Asia/Bangkok)
hour=$(date +%H)
if (( hour >= 23 || hour < 8 )); then
  echo "[$(date --iso-8601=seconds)] Quiet hours — exiting" >> "$LOG"
  exit 0
fi

# Avoid overlap: if another Agni is running, exit
if pgrep -f "agni-cycle.sh" > /dev/null; then
  echo "[$(date --iso-8601=seconds)] Another Agni running — exiting" >> "$LOG"
  exit 0
fi

# Do not spawn if a Rudra is already executing (avoid concurrent modifications)
if pgrep -f "rudra-executor.sh" > /dev/null; then
  echo "[$(date --iso-8601=seconds)] Rudra already running — skipping this cycle" >> "$LOG"
  exit 0
fi

# --- Brainstorming Phase ---
echo "[$(date --iso-8601=seconds)] Brainstorming phase…" >> "$LOG"

# 1. Scan for opportunities: TODO/FIXME comments, stale files, research gaps
grep -r "TODO\|FIXME\|XXX" agents/ quick/ research/ content/ 2>/dev/null | head -20 > agents/agni/opportunities.txt || true

# 2. Determine plan type
plan_type="health"
task_desc="Workspace health check and cleanup"

if [ -s agents/agni/opportunities.txt ]; then
  plan_type="opportunity"
  task_desc="Address found opportunities (TODOs/FIXMEs)"
fi

# 3. Create structured plan file
timestamp=$(date +%Y-%m-%d_%H%M)
plan_dir="agents/agni/plans"
mkdir -p "$plan_dir"
plan_file="$plan_dir/plan-${timestamp}.md"

cat > "$plan_file" << PLAN
# Agni Plan — $timestamp
**Type**: $plan_type
**Task**: $task_desc
**Generated**: $(date --iso-8601=seconds)

## Objective
$task_desc

## Context
- Workspace health: $(./quick status 2>/dev/null | head -1 || echo "unknown")
- Git state: $(git status --short 2>/dev/null | wc -l) files changed
- Active agents: $(cat active-tasks.md 2>/dev/null | grep -c '\[.*\]' || echo 0)

## Steps (for Rudra)
1. Review this plan and verify current workspace state.
2. Execute tasks appropriate to plan type:
   - if opportunity: read agents/agni/opportunities.txt and address them (safe fixes only)
   - if health: run quick health and fix any non-critical issues (e.g., stale logs, missing indexes)
   - if maintenance: update documentation, clean temporary files, verify cron jobs
3. Validation:
   - Run quick verify (if available)
   - Ensure no temporary or backup files left behind
4. Commit changes with prefix "dev:" (or "build:" for infrastructure changes)
5. Write completion report to agents/rudra/reports/report-${timestamp}.md
6. Exit.

## Notes
- Always respect quiet hours (already enforced by spawner)
- If uncertain about a step, skip it and note in report.
- Do not perform disruptive actions (e.g., mass deletions, system upgrades).
PLAN

echo "[$(date --iso-8601=seconds)] Plan created: $plan_file" >> "$LOG"

# --- Spawn Rudra ---
echo "[$(date --iso-8601=seconds)] Spawning Rudra…" >> "$LOG"

# Prepare spawn command
spawn_cmd="bash agents/rudra-executor.sh $plan_file"

# Use OpenClaw to spawn an isolated sub-agent (main agent)
# The agent will receive a message instructing it to exec the command
message="You are Rudra the Executor. Your job: run the following command using the exec tool: $spawn_cmd. After the command completes, write a brief completion report to agents/rudra/reports/report-${timestamp}.md and then exit. Do not ask for confirmation."

# Spawn the agent
output=$(./openclaw sessions spawn --agent main --label rudra-${timestamp} --task "$message" 2>&1)
echo "$output" >> "$LOG"

# Extract session key if possible (for logging)
session_key=$(echo "$output" | grep -o '"sessionKey":"[^"]*"' | cut -d'"' -f4 || echo "unknown")
echo "[$(date --iso-8601=seconds)] Rudra spawned (label: rudra-${timestamp}, session: $session_key)" >> "$LOG"

echo "[$(date --iso-8601=seconds)] Agni cycle complete" >> "$LOG"
