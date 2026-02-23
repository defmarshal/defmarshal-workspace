#!/usr/bin/env bash
# Show research reports by age (oldest first)

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"

echo "Research Reports by Age (oldest first)"
echo "---------------------------------------"

if [ ! -d "$RESEARCH_DIR" ]; then
  echo "Research directory not found: $RESEARCH_DIR"
  exit 1
fi

# Find .md files, print mtime (epoch) and path, sort numerically
find "$RESEARCH_DIR" -maxdepth 1 -name "*.md" -type f -printf "%T@ %p\n" 2>/dev/null | sort -n | while read -r timestamp path; do
  file=$(basename "$path")
  # Compute age in whole days
  now=$(date +%s)
  file_ts=${timestamp%.*}
  age=$(( (now - file_ts) / 86400 ))
  printf "%-35s %4d days\n" "$file" "$age"
done

total=$(ls -1 "$RESEARCH_DIR"/*.md 2>/dev/null | wc -l)
echo
echo "Total reports: $total"
