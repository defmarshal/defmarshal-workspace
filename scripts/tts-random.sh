#!/usr/bin/env bash
# Play a random TTS-narrated research report
# Usage: quick tts-random

WORKSPACE="/home/ubuntu/.openclaw/workspace"

# Find all mp3 files in research/
mapfile -t mp3s < <(find "$WORKSPACE/research" -name "*.mp3" -type f | sort)

if [ ${#mp3s[@]} -eq 0 ]; then
  echo "No TTS audio files found. Run 'quick tts-research-all' first."
  exit 1
fi

# Pick random
choice=$((RANDOM % ${#mp3s[@]}))
file="${mp3s[$choice]}"

echo "Playing: $(basename "$file")"
echo "From: $(dirname "$file" | sed 's|.*/||')"

# Send to Telegram
"$WORKSPACE/quick" telegram-send-media "$file"
