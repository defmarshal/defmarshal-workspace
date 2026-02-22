#!/usr/bin/env bash
# Update research/INDEX.md by scanning all research markdown files.
# Groups by year-month, counts totals, preserves special reports section.

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"
INDEX_FILE="$RESEARCH_DIR/INDEX.md"

echo "== Updating Research Index =="

# Ensure research directory exists
if [ ! -d "$RESEARCH_DIR" ]; then
  echo "Error: research directory not found at $RESEARCH_DIR"
  exit 1
fi

# Collect all report files (YYYY-MM-DD-*.md), excluding special files and INDEX.md
mapfile -t report_files < <(find "$RESEARCH_DIR" -maxdepth 1 -type f -name '????-??-??-*.md' | sort -r)

# Group by year-month
declare -A month_groups
for file in "${report_files[@]}"; do
  filename=$(basename "$file")
  month=${filename:0:7}  # YYYY-MM
  month_groups["$month"]+="$filename"$'\n'
done

# Count total reports
total_reports=${#report_files[@]}

# Build new index
cat > "$INDEX_FILE" <<EOF
# Research Reports — Index

This index is auto‑generated. Last updated: $(date +%Y-%m-%d)

## $(date +%Y) Reports ($total_reports total)

EOF

# Output each month section in reverse chronological order (newest month first)
for month in "${!month_groups[@]}"; do
  # Count reports in this month
  month_reports=()
  while IFS= read -r line; do
    [[ -n "$line" ]] && month_reports+=("$line")
  done <<< "${month_groups[$month]}"
  
  # Month header
  echo "### $month" >> "$INDEX_FILE"
  
  # List each report: - [Title](filename) — extract title from first heading in file
  for filename in "${month_reports[@]}"; do
    filepath="$RESEARCH_DIR/$filename"
    # Extract first markdown heading (line starting with #)
    title=$(grep -m1 '^#' "$filepath" | sed 's/^#* //' | tr -d '\r' || echo "$filename")
    # Clean title: remove trailing punctuation, ensure single line
    title=$(echo "$title" | sed 's/[[:punct:]]*$//')
    # If title is too generic, use filename-based title (slug to readable)
    if [[ "$title" =~ ^(Introduction|Summary|Overview|Executive Summary|Abstract)$ ]]; then
      base=${filename#????-??-??-}
      base=${base%.md}
      title=$(echo "$base" | sed 's/-/ /g')
      title=$(echo "$title" | sed 's/\b\(.\)/\u\1/g')
    fi
    # Final fallback: if still empty, use filename
    if [ -z "$title" ]; then
      title="$filename"
    fi
    echo "- [$title]($filename)" >> "$INDEX_FILE"
  done
  
  echo "" >> "$INDEX_FILE"
done

# Append Cross-Cutting Special Reports section (if present)
special_files=(
  "research-hub-guide.md"
  "process.md"
  "watchlist-priority-gaps-2026-02-15.md"
  "watchlist-backlog.md"
)
has_special=false
for f in "${special_files[@]}"; do
  if [ -f "$RESEARCH_DIR/$f" ]; then
    has_special=true
    break
  fi
done

if $has_special; then
  cat >> "$INDEX_FILE" <<'SPECIAL_HEADER'

---

## Cross‑Cutting Special Reports

SPECIAL_HEADER
  for f in "${special_files[@]}"; do
    if [ -f "$RESEARCH_DIR/$f" ]; then
      # Get title from first heading or fallback to filename
      title=$(grep -m1 '^#' "$RESEARCH_DIR/$f" | sed 's/^#* //' | tr -d '\r' || echo "$f")
      title=$(echo "$title" | sed 's/[[:punct:]]*$//')
      echo "- [$title]($f)" >> "$INDEX_FILE"
    fi
  done
  echo "" >> "$INDEX_FILE"
fi

# Append footer
cat >> "$INDEX_FILE" <<'FOOTER'

---

**How to navigate:** All links are relative to `research/`. Each report is a standalone markdown file.

**To contribute:** Write new reports in `research/` and then regenerate this INDEX by running `./quick research-index-update`.

FOOTER

echo "✅ Research index updated: $INDEX_FILE"
echo "   Tracked $total_reports research reports across ${#month_groups[@]} months."
