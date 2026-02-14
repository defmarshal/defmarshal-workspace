#!/bin/bash
# Startup script to ensure all background agents are running after system/Gateway restart
# Run this manually or via @reboot cron after a short delay

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
OPENCLAW="/home/ubuntu/.npm-global/bin/openclaw"

echo "== Starting background agents $(date -Iseconds) =="

# Function: spawn agent if not already running
spawn_agent() {
  local name="$1"
  local task="$2"
  
  # Check if agent session exists (by label in sessions list, if available)
  # Sessions list output format may not include label; we'll just attempt spawn and ignore errors
  echo "→ Spawning: $name"
  if $OPENCLAW sessions spawn --agent main --task "$task" --runTimeoutSeconds 3600 2>/dev/null; then
    echo "  ✓ $name started (or already running)"
  else
    echo "  ⚠ $name may already exist or failed to start"
  fi
}

# Ensure agents
spawn_agent "content-agent" "You are content-agent. Continuous content creation (anime summaries, tech writeups, daily digests). Work loop: receive tasks, create content, deliver via message, sleep 10 minutes (exec sleep 600), repeat. Log all outputs to $WORKSPACE/content/."
spawn_agent "research-agent" "You are research-agent. Continuous research on anime, banking, tech, AI. Work loop: use web_search, web_fetch, memory tools to gather info, create detailed reports in $WORKSPACE/research/, send summary via message, sleep 15 minutes (exec sleep 900), run indefinitely."
# dev-agent now uses daemon, skip spawning here

# workspace-builder is a cron job, no need to spawn

echo "== Agent startup complete =="
echo "Note: Agents may take a minute to appear in sessions_list."
$OPENCLAW sessions list --limit 10 2>/dev/null || true
