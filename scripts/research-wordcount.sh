#!/usr/bin/env bash
# Show word count statistics for research reports

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"

echo "Research Report Word Count Statistics"
echo "-------------------------------------"

if [ ! -d "$RESEARCH_DIR" ]; then
  echo "Research directory not found: $RESEARCH_DIR"
  exit 1
fi

# Count words in each report, sort by size
declare -a counts
total_words=0
file_count=0

while IFS= read -r file; do
  [ -f "$file" ] || continue
  words=$(wc -w < "$file" 2>/dev/null || echo "0")
  counts+=("$words $(basename "$file")")
  total_words=$((total_words + words))
  file_count=$((file_count + 1))
done < <(find "$RESEARCH_DIR" -maxdepth 1 -name "*.md" -type f)

# Sort numerically by word count (largest first)
IFS=$'\n' sorted=($(sort -rn <<<"${counts[*]}"))
unset IFS

echo "Top 10 longest reports:"
for i in "${!sorted[@]}"; do
  if [ $i -lt 10 ]; then
    words=$(echo "${sorted[$i]}" | awk '{print $1}')
    file=$(echo "${sorted[$i]}" | cut -d' ' -f2-)
    printf "  %6d words  %s\n" "$words" "$file"
  fi
done

echo
echo "Bottom 5 shortest reports:"
j=0
for i in "${!sorted[@]}"; do
  idx=$((file_count - 1 - i))
  if [ $idx -lt 5 ] && [ $i -ge 0 ]; then
    words=$(echo "${sorted[$idx]}" | awk '{print $1}')
    file=$(echo "${sorted[$idx]}" | cut -d' ' -f2-)
    printf "  %6d words  %s\n" "$words" "$file"
    j=$((j+1))
    if [ $j -ge 5 ]; then break; fi
  fi
done

echo
echo "Summary:"
echo "  Total reports: $file_count"
echo "  Total words:   $total_words"
echo "  Average:       $((total_words / file_count)) words/report"
