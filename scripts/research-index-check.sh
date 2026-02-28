#!/usr/bin/env bash
set -euo pipefail
# Check Research Hub INDEX.md for consistency with research/ directory

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"
INDEX_FILE="$WORKSPACE/apps/research-hub/public/research/INDEX.md"

echo "Research Hub Index Check"
echo "-----------------------"

if [ ! -f "$INDEX_FILE" ]; then
  echo "❌ INDEX.md not found at: $INDEX_FILE"
  exit 1
fi

# Get listed reports from INDEX.md (lines starting with '- [' and ending with '.md')
mapfile -t listed < <(grep -E '^- \[.*\]\(.*\.md\)' "$INDEX_FILE" | sed -E 's/.*\[(.*)\]\(.*\.md\).*/\1/')

# Get actual report files (excluding INDEX.md itself)
mapfile -t actual < <(ls -1 "$RESEARCH_DIR"/*.md 2>/dev/null | grep -v 'INDEX.md' | xargs -I{} basename {} .md)

echo "Listed in INDEX.md: ${#listed[@]} entries"
echo "Actual .md files in research/: ${#actual[@]}"

# Find missing in INDEX
missing=0
for file in "${actual[@]}"; do
  found=0
  for listed_file in "${listed[@]}"; do
    if [ "$file" = "$listed_file" ]; then
      found=1
      break
    fi
  done
  if [ $found -eq 0 ]; then
    echo "  ➕ Not in INDEX: $file"
    missing=$((missing+1))
  fi
done

# Find extra in INDEX (no longer exist)
extra=0
for listed_file in "${listed[@]}"; do
  found=0
  for file in "${actual[@]}"; do
    if [ "$listed_file" = "$file" ]; then
      found=1
      break
    fi
  done
  if [ $found -eq 0 ]; then
    echo "  ➖ Missing file: $listed_file"
    extra=$((extra+1))
  fi
done

echo
if [ $missing -eq 0 ] && [ $extra -eq 0 ]; then
  echo "✅ INDEX.md is in sync with research/ directory."
else
  echo "⚠️  Discrepancies found: $missing missing, $extra extra"
  echo "   To regenerate INDEX.md, run: ./quick research-index-update"
fi
