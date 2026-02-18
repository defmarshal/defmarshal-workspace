#!/usr/bin/env bash
# Auto-torrent adder: pick a random torrent from top 10 (max 2GB) and add to aria2
# Used by auto-torrent-cron (2 AM daily) to seed popular anime

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

# Quiet hours check (respect 23:00-08:00 Asia/Bangkok)
TZ='Asia/Bangkok' H=$(date +%H)
if (( 23 <= H || H < 8 )); then
  echo "$(date) - Quiet hours, skipping auto-torrent-add"
  exit 0
fi

# Pick a random number between 1 and 10
NUM=$((RANDOM % 10 + 1))

# Fetch that torrent's magnet and add to aria2
./quick nyaa-top --limit 10 --max-size 2G --pick "$NUM" --add >> memory/auto-torrent.log 2>&1 || {
  echo "$(date) - auto-torrent-add failed for pick $NUM" >&2
  exit 1
}
