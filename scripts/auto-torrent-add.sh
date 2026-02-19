#!/usr/bin/env bash
# Auto-torrent adder: pick a random torrent from top 10 (max 2GB) and add to aria2
# Used by auto-torrent-cron (2 AM daily) to seed popular anime
# Runs 24/7 — quiet hours disabled for torrent operations

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

# Pick a random number between 1 and 5 (matches the number of torrents returned)
NUM=$((RANDOM % 5 + 1))

# Fetch that torrent's magnet and add to aria2
./quick nyaa-top --limit 10 --max-size 2G --pick "$NUM" --add >> memory/auto-torrent.log 2>&1 || {
  echo "$(date) - auto-torrent-add failed for pick $NUM" >&2
  exit 1
}
