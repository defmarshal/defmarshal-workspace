#!/usr/bin/env bash
# Show OpenClaw cron jobs in a readable table (robust parsing)

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "OpenClaw Cron Jobs"
echo "------------------"

# Get cron list JSON, strip any non-JSON preamble (like warnings)
JSON=$(openclaw cron list --json 2>/dev/null | sed -n '/^{/,$p')

# Check if we got valid JSON
if ! echo "$JSON" | jq empty 2>/dev/null; then
  echo "⚠️  Failed to parse cron list JSON. Showing raw output:"
  openclaw cron list --json 2>/dev/null | head -20
  exit 1
fi

echo "$JSON" | jq -r '
  .jobs[]
  | "\(.name)\t\(.enabled // "?")\t\(.schedule.expr // "no-expr")\t\(.nextRunAtMs // 0)\t\(.lastStatus // "?")\t\(.lastRunAtMs // 0)"
' | sort -k1,1 | while IFS=$'\t' read -r name enabled expr nextRun lastStatus lastRun; do
  # Convert timestamps
  next_human="never"
  if [ "$nextRun" -gt 1000000000000 2>/dev/null ]; then
    next_human=$(date -u -d @"$((nextRun/1000))" '+%m-%d %H:%M UTC' 2>/dev/null || echo "$nextRun")
  fi
  last_human="never"
  if [ "$lastRun" -gt 1000000000000 2>/dev/null ]; then
    last_human=$(date -u -d @"$((lastRun/1000))" '+%m-%d %H:%M UTC' 2>/dev/null || echo "$lastRun")
  fi

  # Status icon
  case "$lastStatus" in
    "ok") status_icon="✅" ;;
    "failed") status_icon="❌" ;;
    *) status_icon="$lastStatus" ;;
  esac

  printf "%-35s %-8s %-20s %-15s %-8s %-15s\n" "$name" "$enabled" "$expr" "$next_human" "$status_icon" "$last_human"
done

echo
echo "Legend: enabled? next run (UTC) | status icon | last run (UTC)"
echo "Use 'openclaw cron <id> runs' for detailed history."
