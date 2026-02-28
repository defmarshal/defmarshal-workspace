#!/usr/bin/env bash
set -euo pipefail
# Clean up old log files in memory/ directory (keep recent for debugging)

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOG_DIR="$WORKSPACE/memory"
DAYS_TO_KEEP=7

echo "Old Log Cleanup (keep last $DAYS_TO_KEEP days)"
echo "----------------------------------------------"

if [ ! -d "$LOG_DIR" ]; then
  echo "❌ Log directory not found: $LOG_DIR"
  exit 1
fi

# Find log files older than $DAYS_TO_KEEP
OLD_LOGS=$(find "$LOG_DIR" -type f -name "*.log" -mtime +$DAYS_TO_KEEP 2>/dev/null)

if [ -z "$OLD_LOGS" ]; then
  echo "✅ No logs older than $DAYS_TO_KEEP days found."
  exit 0
fi

echo "Found $(echo "$OLD_LOGS" | wc -l) log file(s) older than $DAYS_TO_KEEP days:"
echo "$OLD_LOGS" | sed 's/^/  /'
echo
read -p "Delete these files? (yes/no): " CONFIRM
if [ "$CONFIRM" = "yes" ]; then
  echo "$OLD_LOGS" | xargs rm -f
  echo "🗑️  Deleted old logs."
else
  echo "Aborted."
fi
