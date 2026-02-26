#!/usr/bin/env bash
# Update Research Hub INDEX.md from all research/*.md files.
# Generates a markdown index sorted by date descending.

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

INDEX_FILE="apps/research-hub/INDEX.md"
mkdir -p "$(dirname "$INDEX_FILE")"

echo "# Research Hub — Index" > "$INDEX_FILE"
echo "" >> "$INDEX_FILE"
echo "Last updated: $(date -u '+%Y-%m-%d %H:%M UTC')" >> "$INDEX_FILE"
echo "" >> "$INDEX_FILE"
echo "| Date | Title | Topics | TTS |" >> "$INDEX_FILE"
echo "|------|-------|--------|-----|" >> "$INDEX_FILE"

# Parse each research file for title and topics
for md in research/*.md; do
  [ -f "$md" ] || continue
  filename=$(basename "$md")
  # Extract date from filename: YYYY-MM-DD...
  DATE=$(echo "$filename" | sed -n 's/^\(202[0-9]-[0-9][0-9]-[0-9][0-9]\).*/\1/p')
  # Extract title: first line starting with '# '
  TITLE=$(grep -m1 '^# ' "$md" | sed 's/^# //; s/[\r\n]//g')
  # Extract topics from the first paragraph (heuristic: look for keywords)
  TOPICS=$(grep -m1 -E '^[A-Za-z]' "$md" | head -1 | sed 's/[\r\n]//g' | cut -c1-80)
  # TTS status
  if [ -f "research/${filename%.md}.mp3" ]; then
    TTS="✅"
  else
    TTS="❌"
  fi
  # Escape pipes in title/topics
  TITLE=$(echo "$TITLE" | sed 's/|/\\|/g')
  TOPICS=$(echo "$TOPICS" | sed 's/|/\\|/g')
  echo "| $DATE | $TITLE | $TOPICS | $TTS |" >> "$INDEX_FILE"
done

echo "✅ Research Hub index updated: $INDEX_FILE"
echo "💡 Deploy with: quick deploy-research-hub"
