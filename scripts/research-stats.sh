#!/usr/bin/env bash
# Show research library statistics

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"

total=$(ls -1 "$RESEARCH_DIR"/*.md 2>/dev/null | wc -l)
with_mp3=$(ls -1 "$RESEARCH_DIR"/*.mp3 2>/dev/null | wc -l)
remaining=$((total - with_mp3))

echo "Research Library Stats"
echo "---------------------"
echo "Total reports: $total"
echo "With TTS audio: $with_mp3 ($((with_mp3 * 100 / total))% coverage)"
echo "Missing audio: $remaining"
echo
echo "Latest reports:"
ls -1t "$RESEARCH_DIR"/*.md 2>/dev/null | head -5 | xargs -n1 basename | sed 's/\.md$//'
echo
echo "RSS feed: https://research-hub-flame.vercel.app/feed"
echo "Hub URL: https://research-hub-flame.vercel.app"
