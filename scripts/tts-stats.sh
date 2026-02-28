#!/usr/bin/env bash
set -euo pipefail
# Show TTS coverage statistics for research reports

WORKSPACE="/home/ubuntu/.openclaw/workspace"

total=0
with_tts=0
english=0
japanese=0
other=0
missing_files=()

for md in "$WORKSPACE"/research/*.md; do
  [ -f "$md" ] || continue
  total=$((total+1))
  mp3="${md%.md}.mp3"
  if [ -f "$mp3" ]; then
    with_tts=$((with_tts+1))
    # Detect language by checking for Japanese chars in the markdown
    if grep -q '[^[:print:]]' "$md" 2>/dev/null; then
      japanese=$((japanese+1))
    else
      english=$((english+1))
    fi
  else
    missing_files+=("$(basename "$md")")
  fi
done

other=$((total - english - japanese))

echo "TTS Coverage Statistics"
echo "----------------------"
printf "Total reports: %d\n" "$total"
printf "With audio: %d (%.1f%%)\n" "$with_tts" "$(awk "BEGIN {printf ($with_tts/$total)*100}")"
printf "English (Kokoro): %d\n" "$english"
printf "Japanese (Edge): %d\n" "$japanese"
printf "Other/Unclassified: %d\n" "$other"
echo
echo "Missing audio: $((total - with_tts)) files"
if [ ${#missing_files[@]} -gt 0 ]; then
  echo "Files without audio:"
  printf '  - %s\n' "${missing_files[@]}"
fi
