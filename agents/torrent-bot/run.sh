#!/bin/bash
# Start the torrent-bot agent in an isolated session
# Usage: ./agents/torrent-bot/run.sh

AGENT_DIR="$(dirname "$0")"
cd "$AGENT_DIR" || exit 1

# Spawn an isolated agent session
exec openclaw agents spawn \
  --agentId torrent-bot \
  --label torrent-bot \
  --task "Torrent management slash-command bot. Use /torrent help for commands." \
  --thinking "low" \
  --timeoutSeconds 3600 \
  --runTimeoutSeconds 0 \
  --cleanup delete \
  --message "Torrent-bot is starting... Use /torrent help"
