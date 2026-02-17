#!/usr/bin/env bash
# Gateway watchdog — ensure OpenClaw gateway stays running
# Runs via system crontab (outside OpenClaw) for reliability

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOG="$WORKSPACE/gateway-watchdog.log"

# Simple timestamped entry
echo "[$(date --iso-8601=seconds)] gateway watchdog check" >> "$LOG"

# Check gateway service
if systemctl --user is-active --quiet openclaw-gateway.service; then
  echo "  → Gateway active" >> "$LOG"
else
  echo "  → Gateway inactive — restarting" >> "$LOG"
  systemctl --user restart openclaw-gateway.service >> "$LOG" 2>&1 || echo "  → Restart failed" >> "$LOG"
fi