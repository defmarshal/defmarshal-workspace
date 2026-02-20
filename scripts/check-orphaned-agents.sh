#!/usr/bin/env bash
# Check for orphaned agents (sessions marked running but stale or dead)
# Usage: ./scripts/check-orphaned-agents.sh
# Exit: 0 if no issues, 1 if orphaned agents detected

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
OPENCLAW="/home/ubuntu/.openclaw"

echo "=== Orphaned Agent Check ==="
echo ""

# Get sessions list in JSON format
if ! SESSIONS_JSON=$(openclaw sessions list --json 2>/dev/null); then
  echo "⚠️  Could not retrieve sessions list (is gateway running?)"
  exit 1
fi

# Check if jq is available; if not, use grep/sed as fallback
if command -v jq &>/dev/null; then
  ORPHANED=$(echo "$SESSIONS_JSON" | jq -r '.sessions[] | select(.status=="running") | "\(.key) \(.lastActivityAt // "null") \(.createdAt)"')
else
  # Fallback: simple text parsing (less reliable)
  echo "Note: jq not installed; using basic parsing"
  ORPHANED=$(echo "$SESSIONS_JSON" | grep -o '"key":"[^"]*"' | cut -d'"' -f4)
fi

if [ -z "$ORPHANED" ]; then
  echo "✅ No running sessions found."
  echo ""
  echo "All agents are either stopped or managed via cron."
  exit 0
fi

echo "Found running sessions:"
echo "$ORPHANED" | while read -r KEY LA CREATED; do
  # For now, just list them; we can't easily determine if truly orphaned without lastActivityAt
  echo "  - $KEY (created: $CREATED, lastActivity: ${LA:-unknown})"
done

echo ""
echo "⚠️  Manual review recommended:"
echo "   Use 'openclaw sessions info --key <sessionKey>' to inspect."
echo "   Use 'openclaw sessions stop --key <sessionKey>' to terminate if needed."

# Future improvement: cross-reference with active-tasks.md and cron jobs

exit 0
