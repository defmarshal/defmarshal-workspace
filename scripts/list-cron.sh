#!/usr/bin/env bash
# List OpenClaw cron jobs in a concise format

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "Cron Jobs (concise)"
echo "-------------------"

JSON=$(openclaw cron list --json 2>/dev/null | sed -n '/^{/,$p')

if ! echo "$JSON" | jq empty 2>/dev/null; then
  echo "⚠️  Failed to parse cron JSON"
  exit 1
fi

echo "$JSON" | jq -r '.jobs[] | "\(.name)\t\(.schedule.expr // "no-expr")\t\(.nextRunAtMs // 0)"' | while IFS=$'\t' read -r name expr nextRun; do
  next_human="never"
  if [ "$nextRun" -gt 1000000000000 2>/dev/null ]; then
    next_human=$(date -u -d @"$((nextRun/1000))" '+%m-%d %H:%M UTC' 2>/dev/null || echo "$nextRun")
  fi
  printf "%-35s %-20s %s\n" "$name" "$expr" "$next_human"
done

echo
echo "Use './quick show-cron' for detailed table with status icons."
