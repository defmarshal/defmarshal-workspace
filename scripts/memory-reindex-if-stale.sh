#!/usr/bin/env bash
# Reindex memory if the last reindex is older than a threshold (default: 7 days).
# Safe to run from cron; respects Voyage rate limits (skips if locked).

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

THRESHOLD_DAYS=${1:-7}
NOW=$(date +%s)
THRESHOLD_SECONDS=$((THRESHOLD_DAYS * 86400))

# Check rate lock file (if Voyage rate-limited, skip)
if [ -f "memory/.voyage-rate-lock" ]; then
  LOCK_AGE=$(( (NOW - $(stat -c %Y memory/.voyage-rate-lock)) / 3600 ))
  if [ $LOCK_AGE -lt 6 ]; then
    echo "⏸️  Voyage rate‑lock active (${LOCK_AGE}h old). Skipping reindex."
    exit 0
  fi
fi

# Check last reindex time from memory reindex log or index mtime
# Use the main store's index file modification time as proxy
INDEX_FILE="$HOME/.openclaw/memory/main.sqlite"
if [ ! -f "$INDEX_FILE" ]; then
  echo "❌ Memory index not found: $INDEX_FILE"
  exit 1
fi

INDEX_MTIME=$(stat -c %Y "$INDEX_FILE")
AGE_SECONDS=$((NOW - INDEX_MTIME))
AGE_DAYS=$((AGE_SECONDS / 86400))

if [ $AGE_SECONDS -lt $THRESHOLD_SECONDS ]; then
  echo "✅ Memory index recent ($AGE_DAYS days old). No reindex needed."
  exit 0
fi

echo "🔄 Memory index stale ($AGE_DAYS days old). Triggering reindex..."
# Use meta‑agent's memory reindex check (respects rate limits)
"$WORKSPACE/agents/meta-agent.sh" memory-reindex-check
echo "✅ Reindex triggered (or skipped due to rate lock)."
