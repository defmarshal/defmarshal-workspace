#!/usr/bin/env bash
# Update research/INDEX.md by scanning all research markdown files.
# Groups by year-month, lists reports with readable titles.
# Automatically includes special reports section if present.

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

# Collect all report files (YYYY-MM-DD-*.md), sorted reverse chronological (newest first)
mapfile -t report_files < <(find "$RESEARCH_DIR" -maxdepth 1 -type f -name '????-??-??-*.md' | sort -r)

if [ ${#report_files[@]} -eq 0 ]; then
  echo "Warning: no research report files found."
  cat > "$INDEX_FILE" <<EOF
# Research Reports — Index

This index is auto‑generated. Last updated: $(date +%Y-%m-%d)

## No reports found

EOF
  exit 0
fi

# Group files by month (YYYY-MM)
declare -A month_files
for file in "${report_files[@]}"; do
  filename=$(basename "$file")
  month=${filename:0:7}  # YYYY-MM
  month_files["$month"]+="$filename"$'\n'
done

# Sort months descending (newest first)
sorted_months=($(printf "%s\n" "${!month_files[@]}" | sort -r))

# Build new index
cat > "$INDEX_FILE" <<EOF
# Research Reports — Index

This index is auto‑generated. Last updated: $(date +%Y-%m-%d)

## ${sorted_months[0]:0:4} Reports (${#report_files[@]} total)

EOF

# Output each month section
for month in "${sorted_months[@]}"; do
  echo "### $month" >> "$INDEX_FILE"
  
  # Get files for this month (newline-separated)
  files_str=${month_files[$month]}
  # Iterate each filename
  while IFS= read -r filename; do
    [ -z "$filename" ] && continue
    filepath="$RESEARCH_DIR/$filename"
    # Extract first markdown heading (line starting with #) as title
    title=$(grep -m1 '^#' "$filepath" 2>/dev/null | sed 's/^#* //' | tr -d '\r' || echo "$filename")
    # Clean title: remove trailing punctuation
    title=$(echo "$title" | sed 's/[[:punct:]]*$//')
    # Fallback: if title is generic or empty, convert filename slug to title
    if [[ "$title" =~ ^(Introduction|Summary|Overview|Executive Summary|Abstract|Note)$ ]] || [ -z "$title" ]; then
      base=${filename#????-??-??-}
      base=${base%.md}
      title=$(echo "$base" | sed 's/-/ /g')
      title=$(echo "$title" | sed 's/\b\(.\)/\u\1/g')
    fi
    echo "- [$title]($filename)" >> "$INDEX_FILE"
  done <<< "$files_str"
  
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
      title=$(grep -m1 '^#' "$RESEARCH_DIR/$f" 2>/dev/null | sed 's/^#* //' | tr -d '\r' || echo "$f")
      title=$(echo "$title" | sed 's/[[:punct:]]*$//')
      echo "- [$title]($f)" >> "$INDEX_FILE"
    fi
  done
  echo "" >> "$INDEX_FILE"
fi

# Footer
cat >> "$INDEX_FILE" <<'FOOTER'

---

**How to navigate:** All links are relative to `research/`. Each report is a standalone markdown file.

**To contribute:** Write new reports in `research/` and then regenerate this INDEX by running `./quick research-index-update`.

FOOTER

echo "✅ Research index updated: $INDEX_FILE"
echo "   Tracked ${#report_files[@]} research reports across ${#sorted_months[@]} months."
