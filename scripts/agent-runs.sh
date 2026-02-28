#!/usr/bin/env bash
set -euo pipefail
# Show recent agent runs from memory logs

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "Recent Agent Activity (last 20 entries)"
echo "---------------------------------------"

# Look for agent logs in memory/
if [ ! -d "$WORKSPACE/memory" ]; then
  echo "No memory directory found."
  exit 1
fi

# Grep common agent names and timestamps
grep -h -E 'Starting|cycle|completed|ERROR|WARN' memory/*.log 2>/dev/null | \
  grep -E 'research-agent|content-agent|dev-agent|linkedin-pa-agent|meta-agent|supervisor' | \
  tail -20 | \
  sed -E 's/^[^[]*\[//; s/\]$//' | \
  while IFS= read -r line; do
    # Try to extract timestamp and message
    if echo "$line" | grep -q '^[0-9]{4}-[0-9]{2}-[0-9]{2}'; then
      ts=$(echo "$line" | cut -d' ' -f1-2)
      msg=$(echo "$line" | cut -d' ' -f3-)
      printf "%-19s %s\n" "$ts" "$msg"
    else
      echo "$line"
    fi
  done

echo
echo "Full logs: memory/*.agent.log (if present)"
echo "Use ./quick agents-health for a summary."
