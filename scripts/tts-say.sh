#!/usr/bin/env bash
# Quick TTS: speak any text via Kokoro
# Usage: tts-say "Your text here"

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
KOKORO_HELPER="$WORKSPACE/scripts/kokoro-generate.py"
KOKORO_VENV_PYTHON="$WORKSPACE/skills/kokoro-tts/venv/bin/python"

if [ $# -lt 1 ]; then
  echo "Usage: $0 <text>"
  echo "Example: $0 \"Hello, world!\""
  exit 1
fi

TEXT="$*"
OUTPUT="/tmp/tts-quick-$(date +%s).mp3"

# Use English voice by default (can add --lang/--voice flags later)
"$KOKORO_VENV_PYTHON" "$KOKORO_HELPER" --lang a --voice af_heart --speed 1.1 --file /dev/stdin "$OUTPUT" <<< "$TEXT"

if [ -f "$OUTPUT" ]; then
  echo "Generated: $OUTPUT"
  # On Telegram, we can't directly play audio, but we can output the path
  # For now, just print the file location; user can play it manually
  echo "Play with: aplay \"$OUTPUT\" 2>/dev/null || open \"$OUTPUT\" 2>/dev/null || echo \"File ready\""
else
  echo "Error: TTS generation failed" >&2
  exit 1
fi
