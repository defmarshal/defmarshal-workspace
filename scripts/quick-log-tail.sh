#!/usr/bin/env bash
# Show recent log tail for a given agent or all
# Usage: quick log-tail [agent-name]

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOGS_DIR="$WORKSPACE/memory"

AGENT="${1:-all}"

if [ "$AGENT" = "all" ]; then
  echo "Recent log tails (last 10 lines) for all agents:"
  for log in "$LOGS_DIR"/*.log; do
    [ -f "$log" ] || continue
    name=$(basename "$log" .log)
    echo "=== $name ==="
    tail -n 10 "$log" 2>/dev/null || echo "(empty or unreadable)"
    echo ""
  done
else
  LOG="$LOGS_DIR/$AGENT.log"
  if [ ! -f "$LOG" ]; then
    echo "❌ Log not found: $LOG"
    exit 1
  fi
  tail -n 20 "$LOG"
fi
