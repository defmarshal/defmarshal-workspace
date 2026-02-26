#!/usr/bin/env bash
# enhancement-bot-start.sh — start the daemon (if not running)

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

PID_FILE="$WORKSPACE/memory/enhancement-bot.pid"

if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Enhancement bot already running (PID $(cat "$PID_FILE"))."
  exit 0
fi

nohup "$WORKSPACE/scripts/enhancement-bot-daemon.sh" > /dev/null 2>&1 &
sleep 1
if [ -f "$PID_FILE" ]; then
  echo "Enhancement bot started (PID $(cat "$PID_FILE"))."
else
  echo "Failed to start enhancement bot."
  exit 1
fi
