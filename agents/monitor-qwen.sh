#!/bin/bash
# Qwen CLI Monitor — track usage, errors, and performance
set -u

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOG_DIR="$WORKSPACE/memory/qwen-monitor"
LOG_FILE="$LOG_DIR/qwen-usage.log"
mkdir -p "$LOG_DIR"

# Rotate if > 10MB
if [ -f "$LOG_FILE" ] && [ $(stat -c%s "$LOG_FILE") -gt 10485760 ]; then
  mv "$LOG_FILE" "$LOG_FILE.$(date -u +%Y%m%d-%H%M%S).gz"
  gzip -q "$LOG_FILE.$(date -u +%Y%m%d-%H%M%S).gz"
fi

# Count today's invocations
TODAY=$(date -u +%Y-%m-%d)
TODAY_COUNT=$(grep -c "\[$TODAY" "$LOG_FILE" 2>/dev/null || echo "0")

# Top models used
echo "=== Qwen CLI Monitor ==="
echo "Date (UTC): $(date -u)"
echo "Today's invocations: $TODAY_COUNT"
echo ""
echo "Top 5 models (last 100 lines):"
tail -100 "$LOG_FILE" 2>/dev/null | grep -oE 'model-[a-zA-Z0-9-]+' | sort | uniq -c | sort -rn | head -5 || echo "No data yet"
echo ""
echo "Recent errors (last 5):"
grep -i "error\|fail" "$LOG_FILE" 2>/dev/null | tail -5 || echo "No errors"
