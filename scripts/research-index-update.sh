#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
INDEX_FILE="$WORKSPACE/apps/research-hub/INDEX.md"
RESEARCH_DIR="$WORKSPACE/research"

# Rebuild index from scratch
{
  echo "# Research Hub — All Reports"
  echo

  # Find all markdown files and extract dates
  declare -A files_by_date
  for md in "$RESEARCH_DIR"/*.md; do
    [ -f "$md" ] || continue
    filename=$(basename "$md")
    date=$(echo "$filename" | sed -n 's/^\(202[0-9]-[0-9][0-9]-[0-9][0-9]\).*/\1/p')
    [ -n "$date" ] && files_by_date["$date"]+="$md "
  done

  # Sort dates descending
  for date in $(printf "%s\n" "${!files_by_date[@]}" | sort -r); do
    echo "## $date"
    echo
    for md in ${files_by_date["$date"]}; do
      filename=$(basename "$md")
      # Title: first line that starts with '# '
      title_line=$(grep -m1 '^# ' "$md" || true)
      if [ -n "$title_line" ]; then
        title=$(echo "$title_line" | sed 's/^# //; s/[\r\n]//g')
      else
        title="$filename"
      fi
      # Topics: first non-empty line that starts with a letter (after title, but we'll approximate)
      topics_line=$(grep -m1 -E '^[A-Za-z]' "$md" | head -1 || true)
      if [ -n "$topics_line" ]; then
        topics=$(echo "$topics_line" | sed 's/[\r\n]//g' | cut -c1-80)
      else
        topics="-"
      fi
      echo "- [${title}](research/${filename}) — ${topics}"
    done
    echo
  done

} > "$INDEX_FILE"

echo "INDEX.md updated with ${#files_by_date[@]} dates"