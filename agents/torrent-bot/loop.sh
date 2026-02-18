#!/usr/bin/env bash
# torrent-bot-loop.sh — unified daemon: keepalive + auto-fetch every 2h (24/7)

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

FETCH_INTERVAL=$((60*60*2))  # 2 hours in seconds
SLEEP_SECONDS=30
last_fetch=0

while true; do
  # Ensure agent session exists (keepalive)
  if ! openclaw sessions list --json 2>/dev/null | grep -q '"label":"torrent-bot"'; then
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Starting torrent-bot session..."
    openclaw agents spawn \
      --agentId torrent-bot \
      --label torrent-bot \
      --task "Torrent management slash-command bot" \
      --thinking "low" \
      --timeoutSeconds 3600 \
      --runTimeoutSeconds 0 \
      --cleanup keep
  fi

  # Auto-fetch every FETCH_INTERVAL
  now=$(date +%s)
  if (( now - last_fetch >= FETCH_INTERVAL )); then
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Running auto-fetch cycle..."
    # Quiet hours check (UTC+7 23:00-08:00) - optional, disable by setting QUIET_HOURS=0
    QUIET_HOURS=0
    if [ $QUIET_HOURS -eq 1 ]; then
      TZ='Asia/Bangkok' H=$(date +%H)
      if (( 23 <= H || H < 8 )); then
        echo "Quiet hours, skipping fetch this cycle"
        last_fetch=$now
        sleep $SLEEP_SECONDS
        continue
      fi
    fi

    # Disk space guard: skip if >=90% used
    FREE_PCT=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
    if (( FREE_PCT >= 90 )); then
      echo "Low disk (${FREE_PCT}% used), skipping fetch this cycle"
      last_fetch=$now
      sleep $SLEEP_SECONDS
      continue
    fi

    # Attempt to add a random torrent (up to 3 tries)
    for ATTEMPT in 1 2 3; do
      NUM=$((RANDOM % 20 + 1))
      RAW_OUTPUT=$(./quick nyaa-top --limit 20 --max-size 1G --pick "$NUM" 2>/dev/null) || {
        echo "Attempt $ATTEMPT: nyaa-top failed, retrying..."
        sleep 0.5
        continue
      }
      MAGNET=$(echo "$RAW_OUTPUT" | grep -E '^Magnet: ' | head -1 | sed 's/^Magnet: //' | tr -d '\r\n' || echo "")
      if [ -z "$MAGNET" ]; then
        echo "Attempt $ATTEMPT: no magnet for pick $NUM, retrying..."
        sleep 0.5
        continue
      fi
      # Check if already in aria2
      if /home/ubuntu/.npm-global/bin/openclaw tools elevated exec -- aria2c --rpc-listen-port 6800 --rpc-secret=openclaw_secret_123 --method aria2.tellStatus 2>/dev/null | grep -F "$MAGNET" >/dev/null 2>&1; then
        echo "Torrent already queued, skipping: $(echo "$MAGNET" | cut -c1-60)..."
        break
      fi
      echo "Adding torrent #$NUM: $(echo "$MAGNET" | cut -c1-60)..."
      ./quick torrent-add "$MAGNET" 2>&1 | logger -t torrent-bot || true
      break
    done

    last_fetch=$now
  fi

  sleep $SLEEP_SECONDS
done
