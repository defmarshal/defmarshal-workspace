#!/usr/bin/env bash
# Check for consistent date formatting in filenames (YYYY-MM-DD-HHMM)

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "Date Format Consistency Check"
echo "----------------------------"

# Directories to scan
DIRS=("$WORKSPACE/content" "$WORKSPACE/research")

# Expected pattern: YYYY-MM-DD-HHMM followed by optional suffix
PATTERN='^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{4}'

issues=0
for dir in "${DIRS[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "⚠️  Directory missing: $dir"
    continue
  fi
  echo "Checking: $dir"
  while IFS= read -r file; do
    fname=$(basename "$file")
    if ! echo "$fname" | grep -qE "$PATTERN"; then
      echo "  ❌ Non-conforming: $fname"
      issues=$((issues+1))
    fi
  done < <(find "$dir" -maxdepth 1 -type f -name "*.md" 2>/dev/null)
done

echo
if [ $issues -eq 0 ]; then
  echo "✅ All .md filenames follow YYYY-MM-DD-HHMM format."
else
  echo "⚠️  Found $issues file(s) with non-standard date prefixes."
  echo "   Consider renaming to standard format for consistency."
fi
