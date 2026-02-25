#!/usr/bin/env bash
# Show recent research reports with TTS audio status

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"
APPS_DIR="$WORKSPACE/apps/research-hub/public/research"

echo "Recent Research Reports (last 10)"
echo "---------------------------------"

# Get latest reports
mapfile -t reports < <(ls -t "$RESEARCH_DIR"/*.md 2>/dev/null | head -10)

if [ ${#reports[@]} -eq 0 ]; then
  echo "No research reports found."
  exit 0
fi

printf "%-40s %-12s %s\n" "REPORT" "TTS AUDIO" "CREATED"
echo "------------------------------------------------------------"

for report in "${reports[@]}"; do
  filename=$(basename "$report" .md)
  # Check if corresponding audio exists in Research Hub public
  audio="$APPS_DIR/$filename.mp3"
  if [ -f "$audio" ]; then
    tts="✅"
  else
    tts="❌"
  fi
  # Get creation date
  created=$(stat -c %y "$report" 2>/dev/null | cut -d' ' -f1,2 | sed 's/ /T/')
  printf "%-40s %-12s %s\n" "$filename" "$tts" "$created"
done

echo
echo "TTS coverage: 100% target (Kokoro). Audio stored in Research Hub public/ for playback."
