#!/usr/bin/env bash
# API endpoint for mood ring data
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

if [ "$REQUEST_METHOD" != "GET" ]; then
  echo "Status: 405 Method Not Allowed"
  echo "Content-Type: application/json"
  echo ""
  echo '{"ok":false,"error":"GET only"}'
  exit 0
fi

# Run the mood ring script and capture output
if [ -f "/home/ubuntu/.openclaw/workspace/scripts/mood-ring.sh" ]; then
  /home/ubuntu/.openclaw/workspace/scripts/mood-ring.sh
fi

# Read the generated mood file
MOOD_FILE="memory/mood-ring.md"
if [ -f "$MOOD_FILE" ]; then
  # Parse the markdown file
  MOOD=$(grep -m1 "^## Mood:" "$MOOD_FILE" | cut -d':' -f2- | xargs)
  EMOJI=$(grep -m1 "^## Emoji:" "$MOOD_FILE" | cut -d':' -f2- | xargs)
  TIMESTAMP=$(grep -m1 "^## Timestamp:" "$MOOD_FILE" | cut -d':' -f2- | xargs)
  REFLECTION=$(grep -A 100 "^## Reflection" "$MOOD_FILE" | sed -n '/---/q;p' | tail -n +2 | xargs)
  
  cat >> /dev/stdout << EOF
Content-Type: application/json

{
  "ok": true,
  "mood": {
    "text": "${MOOD}",
    "emoji": "${EMOJI}",
    "timestamp": "${TIMESTAMP}",
    "reflection": "${REFLECTION}"
  }
}
