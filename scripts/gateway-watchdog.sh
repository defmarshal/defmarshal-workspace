#!/usr/bin/env bash
# Gateway watchdog — ensure OpenClaw gateway stays listening on port 18789
# Runs via system crontab (*/5 * * * *). Does NOT use systemd, checks port directly.

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOG="$WORKSPACE/gateway-watchdog.log"
PORT=18789

echo "[$(date --iso-8601=seconds)] gateway watchdog check" >> "$LOG"

# Check if port is listening
if ss -tuln | grep -q ":$PORT "; then
  echo "  → Gateway listening on port $PORT" >> "$LOG"
else
  echo "  → Gateway NOT listening on port $PORT" >> "$LOG"
  # Try to start via openclaw CLI (bypasses systemd)
  echo "  → Attempting start via 'openclaw gateway start'..." >> "$LOG"
  if command -v openclaw >/dev/null 2>&1; then
    if openclaw gateway start >> "$LOG" 2>&1; then
      echo "  → Start command issued" >> "$LOG"
    else
      echo "  → Start command failed (check gateway config)" >> "$LOG"
    fi
  else
    echo "  → 'openclaw' CLI not found in PATH" >> "$LOG"
  fi
fi