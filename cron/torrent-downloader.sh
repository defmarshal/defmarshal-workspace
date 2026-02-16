#!/bin/bash
# Random torrent downloader: pick a random torrent from top 20 (max 1GB) and add to aria2 if not already present
# Respects quiet hours (23:00–08:00 UTC+7)

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

# Quiet hours check (UTC+7 23:00-08:00)
TZ='Asia/Bangkok' H=$(date +%H)
if (( 23 <= H || H < 8 )); then
  echo "$(date) - Quiet hours, skipping torrent download"
  exit 0
fi

# Check free space on root partition (must be >10% free, i.e., <90% used)
FREE_PCT=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if (( FREE_PCT >= 90 )); then
  echo "$(date) - Low disk space (${FREE_PCT}% used), skipping torrent download"
  exit 0
fi

# Retry up to 3 times if magnet extraction fails
for ATTEMPT in 1 2 3; do
  # Random number between 1 and 20
  NUM=$((RANDOM % 20 + 1))

  # Use quick wrapper (ensures proper environment); output is human‑readable text
  RAW_OUTPUT=$(./quick nyaa-top --limit 20 --max-size 1G --pick "$NUM" 2>/dev/null) || {
    echo "$(date) - Attempt $ATTEMPT: command failed (likely invalid pick), retrying..."
    sleep 0.5
    continue
  }

  # Extract magnet link from the "Magnet: " line
  MAGNET=$(echo "$RAW_OUTPUT" | grep -E '^Magnet: ' | head -1 | sed 's/^Magnet: //' | tr -d '\r\n' || echo "")

  if [ -z "$MAGNET" ]; then
    echo "$(date) - Attempt $ATTEMPT: no magnet found for pick $NUM, retrying..."
    sleep 0.5
    continue
  fi

  # Check if magnet already in aria2 (waiting or active)
  if /home/ubuntu/.npm-global/bin/openclaw tools elevated exec -- aria2c --rpc-listen-port 6800 --rpc-secret=openclaw_secret_123 --method aria2.tellStatus 2>/dev/null | grep -F "$MAGNET" >/dev/null 2>&1; then
    echo "$(date) - Torrent already in aria2, skipping: $(echo "$MAGNET" | cut -c1-60)..."
    exit 0
  fi

  # Add to aria2 via quick wrapper (which calls torrent-add)
  echo "$(date) - Adding torrent #$NUM: $(echo "$MAGNET" | cut -c1-60)..."
  ./quick torrent-add "$MAGNET" 2>&1 | logger -t torrent-downloader || true
  exit 0
done

# If we reach here, all attempts failed
echo "$(date) - Failed to retrieve a valid magnet after 3 attempts"
exit 1
