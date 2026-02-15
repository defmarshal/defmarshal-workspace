#!/bin/bash
# torrent-bot-loop.sh — keep torrent bot running, respect quiet hours

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

while true; do
  # Quiet hours: 23:00-08:00 Asia/Bangkok → don't spawn new sessions
  HOUR=$(TZ=Asia/Bangkok date +%H)
  if (( HOUR >= 23 || HOUR < 8 )); then
    sleep 3600
    continue
  fi

  # Spawn agent if no running session with label torrent-bot
  if ! openclaw sessions list --json 2>/dev/null | grep -q '"label":"torrent-bot"'; then
    echo "[$(TZ=Asia/Bangkok date +'%Y-%m-%d %H:%M')] Starting torrent-bot..."
    openclaw agents spawn \
      --agentId torrent-bot \
      --label torrent-bot \
      --task "Torrent management slash-command bot" \
      --thinking "low" \
      --timeoutSeconds 3600 \
      --runTimeoutSeconds 0 \
      --cleanup keep
  fi

  sleep 30
done
