#!/usr/bin/env bash
# torrent-manager-loop.sh — unified daemon: keeps agent session alive AND auto-fetches random torrents
# 24/7 operation; quiet hours removed (but internal checks can be re-enabled if needed)

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

AGENT_LABEL="torrent-manager"
FETCH_INTERVAL=$((60 * 60 * 2))  # 2 hours (in seconds)
QUIET_HOURS=0  # set 1 to re-enable UTC+7 23:00-08:00 quiet window
DISK_THRESHOLD=90  # % used; stop fetching if >= this

while true; do
  # Ensure agent session exists
  if ! openclaw sessions list --json 2>/dev/null | grep -q "\"label\":\"${AGENT_LABEL}\""; then
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Starting ${AGENT_LABEL} session..."
    openclaw agents spawn \
      --agentId torrent-bot \
      --label "${AGENT_LABEL}" \
      --task "Torrent management slash-command bot" \
      --thinking "low" \
      --timeoutSeconds 3600 \
      --runTimeoutSeconds 0 \
      --cleanup keep
  fi

  # Auto-fetch logic (runs only if not in quiet hours and disk has space)
  if [ $QUIET_HOURS -eq 1 ]; then
    TZ='Asia/Bangkok' H=$(date +%H)
    if (( 23 <= H || H < 8 )); then
      logger -t "${AGENT_LABEL}" "Quiet hours, skipping fetch this cycle"
      sleep $FETCH_INTERVAL
      continue
    fi
  fi

  FREE_PCT=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
  if (( FREE_PCT >= DISK_THRESHOLD )); then
    logger -t "${AGENT_LABEL}" "Low disk (${FREE_PCT}% used), skipping fetch this cycle"
    sleep $FETCH_INTERVAL
    continue
  fi

  # Attempt to add a random torrent (3 tries)
  for ATTEMPT in 1 2 3; do
    NUM=$((RANDOM % 20 + 1))
    RAW_OUTPUT=$(./quick nyaa-top --limit 20 --max-size 1G --pick "$NUM" 2>/dev/null) || {
      logger -t "${AGENT_LABEL}" "Attempt $ATTEMPT: nyaa-top failed, retrying..."
      sleep 0.5
      continue
    }
    MAGNET=$(echo "$RAW_OUTPUT" | grep -E '^Magnet: ' | head -1 | sed 's/^Magnet: //' | tr -d '\r\n' || echo "")
    if [ -z "$MAGNET" ]; then
      logger -t "${AGENT_LABEL}" "Attempt $ATTEMPT: no magnet for pick $NUM, retrying..."
      sleep 0.5
      continue
    fi
    # Check if already in aria2
    if /home/ubuntu/.npm-global/bin/openclaw tools elevated exec -- aria2c --rpc-listen-port 6800 --rpc-secret=openclaw_secret_123 --method aria2.tellStatus 2>/dev/null | grep -F "$MAGNET" >/dev/null 2>&1; then
      logger -t "${AGENT_LABEL}" "Torrent already queued, skipping: $(echo "$MAGNET" | cut -c1-60)..."
      exit 0
    fi
    echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - Adding torrent #$NUM: $(echo "$MAGNET" | cut -c1-60)..."
    ./quick torrent-add "$MAGNET" 2>&1 | logger -t "${AGENT_LABEL}" || true
    exit 0
  done

  logger -t "${AGENT_LABEL}" "Failed to pick valid torrent after 3 attempts; will try next cycle"
  sleep $FETCH_INTERVAL
done
