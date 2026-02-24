#!/usr/bin/env bash
# Show tag statistics for research reports

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"

echo "Research Report Tag Statistics"
echo "------------------------------"

if [ ! -d "$RESEARCH_DIR" ]; then
  echo "Research directory not found: $RESEARCH_DIR"
  exit 1
fi

# Extract tags from front matter (lines starting with "Tags:" or "tags:")
# Count occurrences of each tag across all reports
declare -A tag_counts

while IFS= read -r file; do
  # Get tags line (case-insensitive)
  tags_line=$(grep -iE '^tags:' "$file" | head -1)
  if [ -n "$tags_line" ]; then
    # Remove "Tags:" prefix, split by comma, trim spaces
    tags=$(echo "$tags_line" | sed -E 's/^[Tt]ags:[[:space:]]*//' | tr ',' '\n' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
    for tag in $tags; do
      tag_lower=$(echo "$tag" | tr '[:upper:]' '[:lower:]')
      tag_counts["$tag_lower"]=$((tag_counts["$tag_lower"]+1))
    done
  fi
done < <(find "$RESEARCH_DIR" -maxdepth 1 -name "*.md" -type f)

# Sort and display
if [ ${#tag_counts[@]} -eq 0 ]; then
  echo "No tags found in research reports."
  exit 0
fi

printf "%-25s %5s\n" "Tag" "Count"
echo "--------------------------------"
for tag in "${!tag_counts[@]}"; do
  printf "%-25s %5d\n" "$tag" "${tag_counts[$tag]}"
done | sort -k2,2nr -k1,1

total_reports=$(find "$RESEARCH_DIR" -maxdepth 1 -name "*.md" | wc -l)
echo
echo "Total reports: $total_reports"
echo "Unique tags: ${#tag_counts[@]}"
