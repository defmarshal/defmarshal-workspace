#!/usr/bin/env bash
# Show recent research reports with TTS audio status
# Excludes non-report files: INDEX.md, watchlist*.md, README.md

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"
APPS_DIR="$WORKSPACE/apps/research-hub/public/research"
LIMIT="${1:-10}"

echo "Recent Research Reports (last ${LIMIT})"
echo "---------------------------------"

# Get latest dated reports only (YYYY-MM-DD-*.md)
mapfile -t reports < <(ls -t "$RESEARCH_DIR"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.md 2>/dev/null | head -"$LIMIT")

if [ ${#reports[@]} -eq 0 ]; then
  echo "No research reports found."
  exit 0
fi

printf "%-55s %-12s %s\n" "REPORT" "TTS" "CREATED"
echo "----------------------------------------------------------------------"

has_audio=0
no_audio=0

for report in "${reports[@]}"; do
  filename=$(basename "$report" .md)
  # Check audio in Research Hub public/ OR alongside .md in research/
  audio_hub="$APPS_DIR/$filename.mp3"
  audio_local="$RESEARCH_DIR/$filename.mp3"
  if [ -f "$audio_hub" ] || [ -f "$audio_local" ]; then
    tts="✅"
    has_audio=$(( has_audio + 1 ))
  else
    tts="❌"
    no_audio=$(( no_audio + 1 ))
  fi
  created=$(stat -c %y "$report" 2>/dev/null | cut -d' ' -f1,2 | sed 's/ /T/' | cut -c1-19)
  printf "%-55s %-12s %s\n" "${filename:0:55}" "$tts" "$created"
done

total=$(( has_audio + no_audio ))
if (( total > 0 )); then
  pct=$(( has_audio * 100 / total ))
  echo ""
  echo "TTS coverage: ${has_audio}/${total} (${pct}%) in this view"
fi
