#!/usr/bin/env bash
# Polyglot TTS for research reports: fully Kokoro (English + Japanese)
# Usage: ./tts-research.sh <research-file.md>

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
KOKORO_HELPER="$WORKSPACE/scripts/kokoro-generate.py"
KOKORO_VENV_PYTHON="$WORKSPACE/skills/kokoro-tts/venv/bin/python"

if [ $# -lt 1 ]; then
  echo "Usage: $0 <research-file.md>"
  exit 1
fi

RESEARCH_FILE="$1"

if [ ! -f "$RESEARCH_FILE" ]; then
  echo "Error: file not found: $RESEARCH_FILE"
  exit 1
fi

# Resolve output file path
if [[ "$RESEARCH_FILE" = /* ]]; then
  OUTPUT_FILE="${RESEARCH_FILE%.md}.mp3"
else
  OUTPUT_FILE="$WORKSPACE/${RESEARCH_FILE%.md}.mp3"
fi

# Extract text summary (same approach as before)
mapfile -t lines < "$RESEARCH_FILE"

start_idx=0
for ((i=0; i<${#lines[@]}; i++)); do
  if [[ "${lines[i]}" =~ ^# ]]; then
    start_idx=$((i+1))
    break
  fi
done

section_start=-1
for ((i=start_idx; i<${#lines[@]}; i++)); do
  if [[ "${lines[i]}" =~ ^##\ (Executive\ Summary|Summary|Overview|Abstract|Key\ Findings) ]]; then
    section_start=$i
    break
  fi
done

text=""
if [ $section_start -ge 0 ]; then
  for ((i=section_start+1; i<${#lines[@]}; i++)); do
    line="${lines[i]}"
    if [[ "$line" =~ ^# ]]; then break; fi
    text+="$line"$'\n'
  done
else
  # No specific summary section found; collect initial content
  # Skip over headings but capture their child content (bullet points, paragraphs)
  count=0
  char_count=0
  for ((i=start_idx; i<${#lines[@]}; i++)); do
    line="${lines[i]}"
    if [[ "$line" =~ ^# ]]; then
      continue  # Skip heading lines, don't stop
    fi
    text+="$line"$'\n'
    count=$((count+1))
    char_count=$((char_count+${#line}))
    if [ $count -ge 30 ] || [ $char_count -ge 1200 ]; then break; fi
  done
fi

text=$(echo "$text" | tr '\n' ' ' | tr -s ' ')
text=$(echo "$text" | sed 's/\[[^]]*\]\([^)]*\)/\1/g')
text=$(echo "$text" | sed 's/[*`]//g')
text=$(echo "$text" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
text=$(echo "$text" | head -c 700)

if [ -z "$text" ]; then
  echo "Error: no text extracted"
  exit 1
fi

# Detect Japanese characters (Hiragana, Katakana, Kanji) using Python Unicode check
if python3 -c "import sys; s = sys.argv[1]; 
def is_ja(cp): return (0x3040 <= cp <= 0x309F or 0x30A0 <= cp <= 0x30FF or 0x4E00 <= cp <= 0x9FFF)
sys.exit(0 if any(is_ja(ord(c)) for c in s) else 1)" "$text"; then
  echo "Detected Japanese text → using Kokoro (jf_nezumi)"
  LANG_CODE='j'
  VOICE='jf_nezumi'
  SPEED=1.1
else
  echo "Detected non‑Japanese (English/other) → using Kokoro (af_heart)"
  LANG_CODE='a'
  VOICE='af_heart'
  SPEED=1.1
fi

"$KOKORO_VENV_PYTHON" "$KOKORO_HELPER" \
  --lang "$LANG_CODE" \
  --voice "$VOICE" \
  --speed "$SPEED" \
  --file /dev/stdin \
  "$OUTPUT_FILE" <<< "$text"

if [ -f "$OUTPUT_FILE" ]; then
  echo "✓ Created: $OUTPUT_FILE ($(du -h "$OUTPUT_FILE" | cut -f1))"
else
  echo "✗ Kokoro generation failed"
  exit 1
fi
