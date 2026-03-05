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

# 1. Cron job health (via openclaw)
if command -v openclaw &>/dev/null; then
  if CRON_JSON=$(timeout 15 openclaw cron list --json 2>/dev/null | sed -n '/^{/,$p'); then
    if command -v jq &>/dev/null; then
      PROBLEMS=$(echo "$CRON_JSON" | jq -r '.jobs[] | select((.state.lastStatus // "ok") != "ok" or (.state.consecutiveErrors // 0) > 2) | "- \(.name): \(.state.lastStatus // "no status"), errors \(.state.consecutiveErrors // 0)"')
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
if ! timeout 5 openclaw gateway status &>/dev/null; then
  alert "OpenClaw gateway appears down"
fi

# 3. Memory reindex needed
if ! timeout 10 ./quick memory-reindex-check &>/dev/null; then
  alert "Memory reindex recommended (auto-reindex disabled; run manually via quick memory-reindex)"
fi

# 4. Disk usage (threshold 90%)
USAGE=$(df -h . | awk 'NR==2 {gsub(/%/,""); print $5}')
if [ -n "$USAGE" ] && [ "$USAGE" -ge 90 ]; then
  alert "Disk usage ${USAGE}% >= 90%"
fi

# 5. APT updates threshold (optional: alert if >50)
if command -v apt-get &>/dev/null; then
  COUNT=$(apt-get -s upgrade 2>/dev/null | grep '^Inst ' | wc -l) || COUNT=0
  if [ "$COUNT" -gt 50 ]; then
    alert "APT updates pending: $COUNT"
  fi
fi

# Determine overall status
if [ ${#ALERTS[@]} -gt 0 ]; then
  STATUS="ALERT"
else
  STATUS="OK"
fi

# Update heartbeat-state.json
HEARTBEAT_STATE_FILE="memory/heartbeat-state.json"
NOW_EPOCH=$(date +%s)
jq -n --argjson now "$NOW_EPOCH" '{lastChecks: {email: $now, calendar: $now, weather: $now, health: $now}}' > "$HEARTBEAT_STATE_FILE.tmp" && mv "$HEARTBEAT_STATE_FILE.tmp" "$HEARTBEAT_STATE_FILE" 2>/dev/null || true

# Always log run status
printf "%s - %s\n" "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$STATUS" >> "$LOGFILE"

# If no alerts, exit silently (no Telegram message)
if [ "$STATUS" != "ALERT" ]; then
  exit 0
fi

# Build alert message
NOW_UTC="$(date -u '+%H:%M UTC')"
HEARTBEAT_DATE="$(date -u '+%b %d, %Y')"

DISK_USAGE="$(df -h . | awk 'NR==2 {gsub(/%/,""); print $5}')"
DISK_FREE="$(df -h . | awk 'NR==2 {print $4}')"

UPDATES_COUNT="$(apt-get -s upgrade 2>/dev/null | grep '^Inst ' | wc -l | tr -d ' ' || true)"
[ -z "$UPDATES_COUNT" ] && UPDATES_COUNT=0

GIT_STATUS="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo 0)"
if [ "$GIT_STATUS" -eq 0 ]; then
  GIT_TEXT="clean"
else
  GIT_TEXT="$GIT_STATUS changes"
fi

AGENT_TEXT="idle"
if timeout 5 openclaw sessions list --activeMinutes 5 --json 2>/dev/null | jq -e '.sessions[] | select(.agentId=="main")' >/dev/null 2>&1; then
  AGENT_COUNT=$(timeout 5 openclaw sessions list --activeMinutes 5 --json 2>/dev/null | jq -r '.sessions[] | select(.agentId=="main") | .agentId' | wc -l | tr -d ' ' || echo 0)
  AGENT_TEXT="$AGENT_COUNT active"
fi

# Weather
WEATHER_TEXT=""
if command -v curl &>/dev/null; then
  WEATHER_DATA=$(timeout 10 curl -s "wttr.in/Bangkok?format=%C+%t" 2>/dev/null || echo "")
  if [ -n "$WEATHER_DATA" ]; then
    if echo "$WEATHER_DATA" | grep -qi "rain\|storm\|snow" >/dev/null 2>&1; then
      WEATHER_TEXT="⚠️ Weather: $WEATHER_DATA"
    else
      WEATHER_TEXT="🌤️ Weather: $WEATHER_DATA"
    fi
  fi
fi

# Holiday
HOLIDAY_TEXT=""
if command -v ./quick &>/dev/null; then
  UPCOMING_HOLIDAY=$(./quick holidays 2>/dev/null | head -1 | sed 's/^/🎉 /')
  [ -n "$UPCOMING_HOLIDAY" ] && HOLIDAY_TEXT="$UPCOMING_HOLIDAY"
fi
if [ -z "$HOLIDAY_TEXT" ] && [ -f "HEARTBEAT.md" ] && grep -qi "holiday\|cuti" "HEARTBEAT.md" 2>/dev/null; then
  HOLIDAY_LINE=$(grep -m1 -i "holiday\|cuti" "HEARTBEAT.md" | sed 's/^/🎉 /')
  HOLIDAY_TEXT="$HOLIDAY_LINE"
fi

# Build alert message
HEADER="🔴 System Alert ($NOW_UTC, $HEARTBEAT_DATE)"
ALERT_SUMMARY=""
for a in "${ALERTS[@]}"; do
  a_one_line=$(echo "$a" | tr '\n' ' ' | sed 's/[[:space:]]*$//')
  ALERT_SUMMARY="$ALERT_SUMMARY⚠️ $a_one_line\n"
done

MSG="${HEADER}
─────────────
🖥️  System Overview
─────────────
• Gateway: checking...
• Disk: ${DISK_USAGE}% used (${DISK_FREE} free)
• Updates: ${UPDATES_COUNT} pending
• Git: ${GIT_TEXT}
• Agents: ${AGENT_TEXT}
${ALERT_SUMMARY}${WEATHER_TEXT}
${HOLIDAY_TEXT}

─────
Needs attention! (◕‿◕)♡"

# Log alerts
printf "%s - ALERT - Reasons:\n" "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$LOGFILE"
for alert in "${ALERTS[@]}"; do
  printf "  * %s\n" "$alert" >> "$LOGFILE"
done

# Send alert
timeout 10 /home/ubuntu/.npm-global/bin/openclaw message send -t 952170974 --channel telegram -m "$MSG" 2>/dev/null || true
