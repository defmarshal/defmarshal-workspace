#!/bin/bash
# Startup script to ensure all background agents/daemons are running after system/Gateway restart
# Run this manually or via @reboot cron after a short delay

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "== Starting background agents/daemons $(date -Iseconds) =="

# Check and start daemons if not already running
start_if_missing() {
  local name="$1"
  local script="$2"
  
  if pgrep -f "$script" > /dev/null; then
    echo "  ✓ $name daemon already running"
  else
    echo "  → Starting $name daemon..."
    nohup bash "$WORKSPACE/$script" > /dev/null 2>&1 &
    sleep 1
    if pgrep -f "$script" > /dev/null; then
      echo "    ✓ $name daemon started (PID $(pgrep -f "$script"))"
    else
      echo "    ⚠ Failed to start $name daemon"
    fi
  fi
}

# Start daemons
start_if_missing "dev-agent" "dev-agent-loop.sh"
start_if_missing "content-agent" "content-agent-loop.sh"
start_if_missing "research-agent" "research-agent-loop.sh"

# workspace-builder is a cron job, no need to start

echo "== Agent startup complete =="
echo "Active processes:"
pgrep -af "agent-loop.sh" | grep -v grep || true
