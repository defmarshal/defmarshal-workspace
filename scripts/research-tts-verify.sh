#!/usr/bin/env bash
# Verify TTS coverage for research reports.
# Lists reports that lack a corresponding .mp3 file.
# Use --generate to automatically run tts-research.sh on missing items.

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

GENERATE=false
if [ "${1:-}" = "--generate" ]; then
  GENERATE=true
fi

echo "Checking TTS coverage for research/*.md..."
MISSING=0
for md in research/*.md; do
  [ -f "$md" ] || continue
  base=$(basename "$md" .md)
  mp3="research/$base.mp3"
  if [ ! -f "$mp3" ]; then
    echo "Missing: $base.mp3"
    MISSING=$((MISSING + 1))
    if [ "$GENERATE" = true ]; then
      echo "Generating TTS for $base..."
      scripts/tts-research.sh "$md"
    fi
  fi
done

TOTAL=$(ls -1 research/*.md 2>/dev/null | wc -l)
HAVED=$(ls -1 research/*.mp3 2>/dev/null | wc -l)
COVERAGE=$(( HAVE * 100 / TOTAL ))
echo "Summary: $HAVE / $TOTAL have TTS ($COVERAGE%). Missing: $MISSING"

if [ "$MISSING" -gt 0 ] && [ "$GENERATE" = false ]; then
  echo "To generate missing MP3 files: quick research-tts-verify --generate"
fi
