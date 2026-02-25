#!/usr/bin/env bash
# Check TTS audio coverage for research reports

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"
PUBLIC_DIR="$WORKSPACE/apps/research-hub/public/research"

echo "Research TTS Coverage Check"
echo "--------------------------"

# Get all report .md files (excluding INDEX.md and other non-reports)
mapfile -t reports < <(ls -1 "$RESEARCH_DIR"/*.md 2>/dev/null | grep -v 'INDEX.md' | grep -v '^findings\.md$' | grep -v '^task_plan\.md$' | grep -v '^progress\.md$' | xargs -I{} basename {} .md)

# Get all audio files
mapfile -t audio_files < <(ls -1 "$PUBLIC_DIR"/*.mp3 2>/dev/null | xargs -I{} basename {} .mp3)

TOTAL_REPORTS=${#reports[@]}
TOTAL_AUDIO=${#audio_files[@]}

echo "Total reports: $TOTAL_REPORTS"
echo "Audio files:   $TOTAL_AUDIO"

if [ $TOTAL_REPORTS -eq 0 ]; then
  echo "❌ No reports found"
  exit 1
fi

# Count missing
missing=0
for report in "${reports[@]}"; do
  found=0
  for audio in "${audio_files[@]}"; do
    if [ "$report" = "$audio" ]; then
      found=1
      break
    fi
  done
  if [ $found -eq 0 ]; then
    echo "  ❌ Missing audio: $report"
    missing=$((missing+1))
  fi
done

echo
if [ $missing -eq 0 ]; then
  echo "✅ 100% TTS coverage! All reports have audio."
else
  PERCENT=$(( (TOTAL_REPORTS - missing) * 100 / TOTAL_REPORTS ))
  echo "⚠️  Coverage: $PERCENT% ($missing missing)"
  echo "   To generate TTS for missing reports, run the TTS script manually."
fi
