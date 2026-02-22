#!/usr/bin/env bash
# Generate TTS audio for a research report (summary version)
# Usage: ./tts-research.sh <research-file.md> [voice] [rate]

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
SCRIPTS_DIR="$WORKSPACE/skills/edge-tts/scripts"

if [ $# -lt 1 ]; then
  echo "Usage: $0 <research-file.md> [voice] [rate]"
  echo "Example: $0 research/2026-02-22-ai-infrastructure-constraints.md en-US-MichelleNeural +10%"
  exit 1
fi

RESEARCH_FILE="$1"
VOICE="${2:-en-US-MichelleNeural}"
RATE="${3:-+10%}"

if [ ! -f "$RESEARCH_FILE" ]; then
  echo "Error: file not found: $RESEARCH_FILE"
  exit 1
fi

# Resolve output file path: accept both absolute and workspace-relative
if [[ "$RESEARCH_FILE" = /* ]]; then
  OUTPUT_FILE="${RESEARCH_FILE%.md}.mp3"
else
  OUTPUT_FILE="$WORKSPACE/${RESEARCH_FILE%.md}.mp3"
fi

# Extract a concise summary: try "Executive Summary" or "Summary" section; else first paragraphs
mapfile -t lines < "$RESEARCH_FILE"

# Find start after title line (first line starting with #)
start_idx=0
for ((i=0; i<${#lines[@]}; i++)); do
  if [[ "${lines[i]}" =~ ^# ]]; then
    start_idx=$((i+1))
    break
  fi
done

# Look for a summary section
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
  count=0
  char_count=0
  for ((i=start_idx; i<${#lines[@]}; i++)); do
    line="${lines[i]}"
    if [[ "$line" =~ ^# ]]; then break; fi
    text+="$line"$'\n'
    count=$((count+1))
    char_count=$((char_count+${#line}))
    if [ $count -ge 30 ] || [ $char_count -ge 1200 ]; then break; fi
  done
fi

# Flatten to single line, preserve basic punctuation
text=$(echo "$text" | tr '\n' ' ' | tr -s ' ')
# Remove markdown links but keep link text
text=$(echo "$text" | sed 's/\[[^]]*\]\([^)]*\)/\1/g')
# Remove asterisks, backticks
text=$(echo "$text" | sed 's/[*`]//g')
# Trim
text=$(echo "$text" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

if [ -z "$text" ]; then
  echo "Error: no text extracted from report"
  exit 1
fi

# Limit length to 700 characters to avoid chunking issues
text=$(echo "$text" | head -c 700)

# OUTPUT_FILE already set by earlier conditional

echo "Generating TTS for: $(basename "$RESEARCH_FILE")"
echo "Voice: $VOICE, Rate: $RATE"
echo "Text length: ${#text} chars"
echo "Output: $OUTPUT_FILE"

cd "$SCRIPTS_DIR"
node tts-converter.js "$text" --voice "$VOICE" --rate "$RATE" --output "$OUTPUT_FILE"

if [ -f "$OUTPUT_FILE" ]; then
  echo "✓ Created: $OUTPUT_FILE ($(du -h "$OUTPUT_FILE" | cut -f1))"
else
  echo "✗ TTS generation failed"
  exit 1
fi
