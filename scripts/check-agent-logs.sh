#!/usr/bin/env bash
# Check agent log freshness with awareness of typical schedules.
# Green: active within expected window; Yellow: stale but within quiet period; Red: missing or clearly stale.

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOGDIR="$WORKSPACE/memory"

# Agent definitions: name, expected active hours (24h = always), log file
declare -A AGENT_SCHEDULE
AGENT_SCHEDULE=(
  [linkedin-pa-agent]="0-23"     # runs hourly 24/7
  [research-agent]="8-22"        # 08:00-22:00 UTC
  [content-agent]="0-23"         # can run any time
  [dev-agent]="0-23"
  [supervisor]="0-23"
  [agent-manager]="0-23"
  [meta-agent]="0-23"
)

NOW_EPOCH=$(date -u +%s)
NOW_HOUR=$(date -u +%H)

echo "Agent Log Freshness (as of $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC))"
echo "-----------------------------------------------------------"

for agent in "${!AGENT_SCHEDULE[@]}"; do
  LOG="$LOGDIR/$agent.log"
  if [ ! -f "$LOG" ]; then
    echo "❌ $agent: log file missing"
    continue
  fi

  # Get last timestamp from log (ISO format expected)
  LAST_LINE=$(tail -1 "$LOG")
  if ! echo "$LAST_LINE" | grep -qE '[0-9]{4}-[0-9]{2}-[0-9]{2}'; then
    echo "⚠️  $agent: no parsable timestamp in log"
    continue
  fi

  TS=$(echo "$LAST_LINE" | awk '{print $1" "$2}')
  TS_EPOCH=$(date -d "$TS" +%s 2>/dev/null || echo 0)
  HOURS_AGO=$(( (NOW_EPOCH - TS_EPOCH) / 3600 ))

  SCHEDULE="${AGENT_SCHEDULE[$agent]}"
  if [[ "$SCHEDULE" == "0-23" ]]; then
    # Always-on agent: must have activity in last 2 hours
    if [ $HOURS_AGO -le 2 ]; then
      echo "✅ $agent: active ($HOURS_AGO hour(s) ago)"
    elif [ $HOURS_AGO -le 24 ]; then
      echo "🟡 $agent: stale ($HOURS_AGO hour(s) ago)"
    else
      echo "❌ $agent: stale ($HOURS_AGO hour(s) ago)"
    fi
  else
    # Scheduled agent: check if current hour is within active window
    START_HOUR="${SCHEDULE%%-*}"
    END_HOUR="${SCHEDULE##*-}"
    if [ "$NOW_HOUR" -ge "$START_HOUR" ] && [ "$NOW_HOUR" -lt "$END_HOUR" ]; then
      # Within active hours; expect activity in last 2 hours
      if [ $HOURS_AGO -le 2 ]; then
        echo "✅ $agent: active ($HOURS_AGO hour(s) ago)"
      else
        echo "🟡 $agent: expected now but last seen $HOURS_AGO hour(s) ago"
      fi
    else
      # Outside active hours; just note last activity
      echo "🟢 $agent: off-duty (last: $HOURS_AGO hour(s) ago, schedule $SCHEDULE UTC)"
    fi
  fi
done
