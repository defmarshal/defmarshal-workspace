#!/usr/bin/env bash
# Send a cozy music recommendation to Telegram
# Usage: ./scripts/music-recommend.sh

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

# Curated list of cozy streams
declare -a STREAMS=(
  "Lofi Girl — beats to relax/study to • https://www.youtube.com/watch?v=jfKfPfyJRdk"
  "Chillhop Radio — jazzy lofi beats • https://www.youtube.com/watch?v=5yx6BWlEVcY"
  "DI.FM LoFi Hip-Hop — textured atmospheres • https://www.di.fm/lofihiphop"
  "Chillsky Radio — 24/7 lofi from China • https://www.chillsky.com/"
  "Zeno.FM City Pop — smooth Japanese vibes • https://zeno.fm/radio/city-pop/"
  "vo-radio.com City Pop — high quality • https://vo-radio.com/genres/80s/citypop"
  "SoundCloud City Pop Radio • https://soundcloud.com/user-339347298"
)

# Pick a random stream
RECOMMENDATION="${STREAMS[$RANDOM % ${#STREAMS[@]}]}"

# Compose message
MSG="🎧 Cozy Music Moment (${RECOMMENDATION}) 🌙\n\nHere’s a smooth stream to brighten your day! Press play and let the good vibes flow.\n\n— mewmew (◕‿◕)♡"

# Send to Telegram (uses OpenClaw message tool)
echo "Sending music recommendation to Telegram..."
message --channel telegram --to 952170974 --text "$MSG" --silent 2>/dev/null || echo "Note: message tool failed; ensure Telegram channel configured."
