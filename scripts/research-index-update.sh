#!/usr/bin/env bash
# Regenerate Research Hub INDEX.md from actual research files

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"
INDEX_FILE="$WORKSPACE/apps/research-hub/public/research/INDEX.md"

echo "Regenerating Research Hub INDEX.md..."
echo

# Get all .md files except INDEX.md itself, sort by name
mapfile -t files < <(ls -1 "$RESEARCH_DIR"/*.md 2>/dev/null | grep -v 'INDEX.md' | xargs -I{} basename {} .md | sort)

if [ ${#files[@]} -eq 0 ]; then
  echo "❌ No research reports found in $RESEARCH_DIR"
  exit 1
fi

# Generate INDEX.md with simple markdown list
cat > "$INDEX_FILE" << EOF
# Research Hub Index

Updated: $(date -u '+%Y-%m-%d %H:%M UTC')

Total reports: ${#files[@]}

## Reports

EOF

for file in "${files[@]}"; do
  echo "- [$file]($file.md)" >> "$INDEX_FILE"
done

echo "✅ INDEX.md generated with ${#files[@]} entries"
echo "   Location: $INDEX_FILE"
