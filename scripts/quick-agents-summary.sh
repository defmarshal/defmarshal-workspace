#!/usr/bin/env bash
# Quick agents summary — one line per agent with status and last run
# Usage: quick agents-summary

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
ACTIVE_TASKS="$WORKSPACE/active-tasks.md"

if [ ! -f "$ACTIVE_TASKS" ]; then
  echo "❌ active-tasks.md not found"
  exit 1
fi

echo "Agent Status Summary:"
grep -E '^- \[.+\] .+ - .+ \(started:' "$ACTIVE_TASKS" | sed -E 's/^- \[([^]]+)\] ([^ ]+) - .+ \(started: ([^,]+), status: ([^)]+)\)/\4 | \2 | \3 | \1/' | column -t -s '|' || true

echo ""
echo "Completed (recent):"
grep -E '^- \[.+\] .+ - .+ \(started:' "$ACTIVE_TASKS" | sed -E 's/^- \[([^]]+)\] ([^ ]+) - .+ \(started: ([^,]+), status: [^)]+, verification: .+\)/\3 | \2 | \1/' | sort -r | head -5 | column -t -s '|' || true
