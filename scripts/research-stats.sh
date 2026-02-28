#!/usr/bin/env bash
# Show research library statistics
# Excludes non-report files: INDEX.md, watchlist*.md, README.md

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"

# Count only dated reports (YYYY-MM-DD-*.md), not INDEX/watchlist/README
total=$(ls -1 "$RESEARCH_DIR"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.md 2>/dev/null | wc -l)
# Count mp3s that have a matching .md report (paired audio only)
with_mp3=0
while IFS= read -r mp3; do
  base="${mp3%.mp3}"
  [[ -f "${base}.md" ]] && with_mp3=$(( with_mp3 + 1 ))
done < <(ls -1 "$RESEARCH_DIR"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.mp3 2>/dev/null)
remaining=$((total - with_mp3))

# Guard against division by zero
pct=0
if (( total > 0 )); then
  pct=$(( with_mp3 * 100 / total ))
fi

# Reports today
today=$(date -u +%Y-%m-%d)
today_count=$(ls -1 "$RESEARCH_DIR"/${today}-*.md 2>/dev/null | wc -l)

echo "Research Library Stats"
echo "---------------------"
echo "Total reports:    $total"
echo "Reports today:    $today_count"
echo "With TTS audio:   $with_mp3 (${pct}% coverage)"
echo "Missing audio:    $remaining"
echo
echo "Latest reports:"
ls -1t "$RESEARCH_DIR"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.md 2>/dev/null \
  | head -5 | xargs -n1 basename | sed 's/\.md$//'
echo
echo "RSS feed: https://research-hub-flame.vercel.app/feed"
echo "Hub URL:  https://research-hub-flame.vercel.app"
