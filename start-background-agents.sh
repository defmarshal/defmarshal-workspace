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
# NOTE (2026-02-16): dev-agent, content-agent, research-agent have been migrated to OpenClaw cron jobs.
# The daemon loops are no longer needed. Keeping aria2 and torrent-bot (legacy) as daemons.
# start_if_missing "dev-agent" "dev-agent-loop.sh"
# start_if_missing "content-agent" "content-agent-loop.sh"
# start_if_missing "research-agent" "research-agent-loop.sh"
# start_if_missing "torrent-bot" "agents/torrent-bot/loop.sh"  # Deprecated: CLI API changed; disabled 2026-02-19
# cron-supervisor is now a cron-triggered agent (not a daemon loop).

# Start meta-supervisor daemon if not running (continuous agent outcome auditor)
if pgrep -f "meta-supervisor-daemon.sh" > /dev/null; then
  echo "  ✓ meta-supervisor daemon already running"
else
  echo "  → Starting meta-supervisor daemon..."
  nohup bash "$WORKSPACE/agents/meta-supervisor/meta-supervisor-daemon.sh" > /dev/null 2>&1 &
  sleep 1
  if pgrep -f "meta-supervisor-daemon.sh" > /dev/null; then
    echo "    ✓ meta-supervisor daemon started (PID $(pgrep -f "meta-supervisor-daemon.sh"))"
  else
    echo "    ⚠ Failed to start meta-supervisor daemon"
  fi
fi
if pgrep -f "aria2c.*--conf-path=/home/ubuntu/.openclaw/workspace/aria2.conf" > /dev/null; then
  echo "  ✓ aria2 daemon already running"
else
  echo "  → Starting aria2 daemon..."
  nohup aria2c --conf-path="$WORKSPACE/aria2.conf" --daemon=true > /dev/null 2>&1 &
  sleep 1
  if pgrep -f "aria2c.*--conf-path=$WORKSPACE/aria2.conf" > /dev/null; then
    echo "    ✓ aria2 daemon started (PID $(pgrep -f "aria2c.*--conf-path=$WORKSPACE/aria2.conf"))"
  else
    echo "    ⚠ Failed to start aria2 daemon"
  fi
fi

# workspace-builder is a cron job, no need to start

# Start RPG Dashboard (Node server) if not running
if pgrep -f "dashboard/server.js" > /dev/null; then
  echo "  ✓ RPG dashboard already running"
else
  echo "  → Starting RPG dashboard..."
  nohup node "$WORKSPACE/dashboard/server.js" > /dev/null 2>&1 &
  sleep 1
  if pgrep -f "dashboard/server.js" > /dev/null; then
    echo "    ✓ RPG dashboard started (PID $(pgrep -f "dashboard/server.js"))"
  else
    echo "    ⚠ Failed to start RPG dashboard"
  fi
fi

echo "== Agent startup complete =="
echo "Active processes:"
pgrep -af "agent-loop.sh" | grep -v grep || true
