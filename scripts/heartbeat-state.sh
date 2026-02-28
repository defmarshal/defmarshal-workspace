#!/usr/bin/env bash
set -euo pipefail
# Show heartbeat state (last check times per channel) in a readable format.
# Reads memory/heartbeat-state.json if present.

WORKSPACE="/home/ubuntu/.openclaw/workspace"
STATE_FILE="$WORKSPACE/memory/heartbeat-state.json"

if [ ! -f "$STATE_FILE" ]; then
  echo "No heartbeat state file found at $STATE_FILE"
  exit 0
fi

echo "Heartbeat State:"
echo "---------------"
if command -v jq &>/dev/null; then
  jq -r 'to_entries[] | "\(.key): \(.value | tostring)"' "$STATE_FILE" 2>/dev/null || cat "$STATE_FILE"
else
  cat "$STATE_FILE"
fi
