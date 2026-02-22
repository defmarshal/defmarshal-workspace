#!/usr/bin/env bash
# Play a TTS MP3 file (uses aplay on Linux, afplay on macOS, or fallback)
# Usage: tts-play <mp3-file>

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <mp3-file>"
  echo "Example: $0 research/2026-02-22-ai-infrastructure-constraints-2026-2028-power-water-grid-reckoning.mp3"
  exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: file not found: $FILE" >&2
  exit 1
fi

# Determine player
if command -v aplay &>/dev/null; then
  PLAYER="aplay"
elif command -v afplay &>/dev/null; then
  PLAYER="afplay"
elif command -v mpg123 &>/dev/null; then
  PLAYER="mpg123"
else
  echo "Error: No audio player found (install aplay/afplay/mpg123)" >&2
  exit 1
fi

echo "Playing: $FILE"
"$PLAYER" "$FILE"
