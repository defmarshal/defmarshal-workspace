#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOGFILE="memory/supervisor.log"
mkdir -p memory

ALERTS=()

# Helper: append alert
alert() {
  ALERTS+=("$1")
}

# 1. Cron job health (via openclaw cron list)
if command -v openclaw &>/dev/null; then
  if CRON_JSON=$(openclaw cron list --json 2>/dev/null); then
    # jq available? (should be)
    if command -v jq &>/dev/null; then
      PROBLEMS=$(echo "$CRON_JSON" | jq -r '.jobs[] | select(.lastStatus != "ok" or (.consecutiveErrors // 0) > 2) | "- \(.name): \(.lastStatus // "no status"), errors \(.consecutiveErrors // 0)"')
      if [ -n "$PROBLEMS" ]; then
        alert "Cron job issues:\n$PROBLEMS"
      fi
    else
      alert "jq missing; cannot parse cron health"
    fi
  else
    alert "Failed to fetch cron list"
  fi
else
  alert "openclaw CLI not found"
fi

# 2. Gateway health
if ! openclaw gateway status &>/dev/null; then
  alert "OpenClaw gateway appears down"
fi

# 3. Memory reindex needed
if ./quick memory-reindex-check &>/dev/null; then
  alert "Memory reindex recommended"
fi

# 4. Disk usage (threshold 90%)
USAGE=$(df -h . | awk 'NR==2 {gsub(/%/,""); print $5}')
if [ -n "$USAGE" ] && [ "$USAGE" -ge 90 ]; then
  alert "Disk usage ${USAGE}% >= 90%"
fi

# 5. APT updates threshold (optional: alert if >50)
if command -v apt-get &>/dev/null; then
  # dry-run to count upgradable packages
  COUNT=$(apt-get -s upgrade | grep -c '^Inst ')
  if [ "$COUNT" -gt 50 ]; then
    alert "APT updates pending: $COUNT"
  fi
fi

# Emit alerts only (cron will announce)
if [ ${#ALERTS[@]} -gt 0 ]; then
  printf "SUPERVISOR ALERT:\n%s\n" "${ALERTS[*]}"
fi

# Always log run status
STATUS="OK"
if [ ${#ALERTS[@]} -gt 0 ]; then STATUS="ALERT"; fi
printf "%s - %s\n" "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$STATUS" >> "$LOGFILE"
