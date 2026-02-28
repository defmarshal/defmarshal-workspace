#!/usr/bin/env bash
# Restart meta-supervisor daemon
# Usage: ./scripts/meta-supervisor-restart.sh

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOG_FILE="$WORKSPACE/memory/meta-supervisor-restart.log"

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOG_FILE"
}

log "Restart requested"

# Kill existing meta-supervisor daemon if running
if pgrep -f "meta-supervisor-daemon.sh" > /dev/null; then
  log "Stopping existing meta-supervisor daemon..."
  pkill -f "meta-supervisor-daemon.sh" || true
  sleep 1
else
  log "No existing daemon found"
fi

# Start fresh daemon
log "Starting meta-supervisor daemon..."
nohup bash "$WORKSPACE/agents/meta-supervisor/meta-supervisor-daemon.sh" > /dev/null 2>&1 &
sleep 2

# Verify
if pgrep -f "meta-supervisor-daemon.sh" > /dev/null; then
  PID=$(pgrep -f "meta-supervisor-daemon.sh")
  log "Meta-supervisor daemon started successfully (PID $PID)"
  echo "✓ Meta-supervisor running (PID $PID)"
else
  log "⚠ Failed to start meta-supervisor daemon"
  echo "✗ Failed to start meta-supervisor daemon"
  exit 1
fi
