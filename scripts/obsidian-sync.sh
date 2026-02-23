#!/usr/bin/env bash
# obsidian-sync - Sync OpenClaw outputs to an Obsidian vault (complete archive)
# Copies all research and content files, organized by year-month.
# Creates daily summary note and dashboard.

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
VAULT_DIR="${OBSIDIAN_VAULT:-$HOME/obsidian-vault}"

echo "== Syncing OpenClaw outputs to Obsidian vault =="
echo "Vault: $VAULT_DIR"
mkdir -p "$VAULT_DIR"

# 1. Create/update daily summary note for TODAY
DATE=$(date +%Y-%m-%d)
DAILY_NOTE="$VAULT_DIR/Daily/$DATE.md"
mkdir -p "$VAULT_DIR/Daily"

SUMMARY="# $DATE — OpenClaw Summary\n\n"
SUMMARY+="**Generated:** $(date -u '+%Y-%m-%d %H:%M UTC')\n\n"

# Today's research
TODAY_RESEARCH=$(ls -1 research/${DATE}-*.md 2>/dev/null || true)
if [ -n "$TODAY_RESEARCH" ]; then
  RESEARCH_COUNT=$(echo "$TODAY_RESEARCH" | wc -l)
  SUMMARY+="## Research Today ($RESEARCH_COUNT)\n"
  for f in $TODAY_RESEARCH; do
    TITLE=$(head -1 "$f" | sed 's/^# //;s/\.md$//')
    SUMMARY+="- [[$TITLE]] (Research/$(basename $f))\n"
  done
  SUMMARY+="\n"
fi

# Today's content
TODAY_CONTENT=$(ls -1 content/${DATE}-*.md 2>/dev/null || true)
if [ -n "$TODAY_CONTENT" ]; then
  CONTENT_COUNT=$(echo "$TODAY_CONTENT" | wc -l)
  SUMMARY+="## Content Today ($CONTENT_COUNT)\n"
  for f in $TODAY_CONTENT; do
    TITLE=$(head -1 "$f" | sed 's/^# //;s/\.md$//')
    SUMMARY+="- [[$TITLE]] (Content/$(basename $f))\n"
  done
  SUMMARY+="\n"
fi

# System health snapshot
HEALTH=$(./quick health 2>/dev/null || echo "N/A")
SUMMARY+="## System Health\n"
SUMMARY+="- $HEALTH\n"
SUMMARY+="- Memory: $(./quick memory-summary 2>/dev/null | head -1 || echo "N/A")\n"
SUMMARY+="- Gateway: $(openclaw gateway status 2>/dev/null | head -1 || echo "N/A")\n"

echo -e "$SUMMARY" > "$DAILY_NOTE"
echo "✓ Created daily note: $DAILY_NOTE"

# 2. Sync ALL research files (organized by year-month)
RESEARCH_VAULT="$VAULT_DIR/Research"
mkdir -p "$RESEARCH_VAULT"

# Copy all research reports (YYYY-MM-DD-*.md) preserving year-month structure
while IFS= read -r file; do
  filename=$(basename "$file")
  year_month=${filename:0:7}  # YYYY-MM
  dest_dir="$RESEARCH_VAULT/$year_month"
  mkdir -p "$dest_dir"
  dest="$dest_dir/$filename"
  if [ ! -f "$dest" ] || [ "$file" -nt "$dest" ]; then
    cp "$file" "$dest"
    echo "✓ Copied research: $year_month/$filename"
  fi
done < <(find research -maxdepth 1 -type f -name '????-??-??-*.md' 2>/dev/null | sort)

# 3. Sync ALL content files (organized by type)
# Regular content (daily digests, notes) → Content/YYYY-MM/
# LinkedIn PA posts → Content/LinkedIn/YYYY-MM/
CONTENT_VAULT="$VAULT_DIR/Content"
mkdir -p "$CONTENT_VAULT"

# 3a. Regular content (exclude LinkedIn PA specific files)
while IFS= read -r file; do
  filename=$(basename "$file")
  year_month=${filename:0:7}
  dest_dir="$CONTENT_VAULT/$year_month"
  mkdir -p "$dest_dir"
  dest="$dest_dir/$filename"
  if [ ! -f "$dest" ] || [ "$file" -nt "$dest" ]; then
    cp "$file" "$dest"
    echo "✓ Copied content: $year_month/$filename"
  fi
done < <(find content -maxdepth 1 -type f -name '????-??-??-*.md' 2>/dev/null | grep -v 'linkedin-pa' | sort)

# 3b. LinkedIn PA specific content → Content/LinkedIn/YYYY-MM/
LINKEDIN_VAULT="$CONTENT_VAULT/LinkedIn"
mkdir -p "$LINKEDIN_VAULT"
while IFS= read -r file; do
  filename=$(basename "$file")
  year_month=${filename:0:7}
  dest_dir="$LINKEDIN_VAULT/$year_month"
  mkdir -p "$dest_dir"
  dest="$dest_dir/$filename"
  if [ ! -f "$dest" ] || [ "$file" -nt "$dest" ]; then
    cp "$file" "$dest"
    echo "✓ Copied LinkedIn PA: LinkedIn/$year_month/$filename"
  fi
done < <(find content -maxdepth 1 -type f -name '????-??-??-*linkedin-pa*.md' 2>/dev/null | sort)

# 4. Create/update Research Index note (with dataview suggestion)
RESEARCH_INDEX="$VAULT_DIR/Research/Index.md"
if [ ! -f "$RESEARCH_INDEX" ]; then
  cat > "$RESEARCH_INDEX" <<'EOF'
# Research Index

All research reports are organized by year-month folders below.

To browse, use the file pane or this Dataview query:

```dataview
TABLE file.mtime as Modified
FROM "Research"
SORT file.name DESC
```
EOF
  echo "✓ Created research index note"
fi

# 5. Create/update Content Index note
CONTENT_INDEX="$VAULT_DIR/Content/Index.md"
if [ ! -f "$CONTENT_INDEX" ]; then
  cat > "$CONTENT_INDEX" <<'EOF'
# Content Index

Daily digests and content notes organized by year-month.

```dataview
TABLE file.mtime as Modified
FROM "Content"
SORT file.name DESC
```
EOF
  echo "✓ Created content index note"
fi

# 5b. Create/update LinkedIn Index note
LINKEDIN_INDEX="$VAULT_DIR/Content/LinkedIn/Index.md"
if [ ! -f "$LINKEDIN_INDEX" ]; then
  mkdir -p "$VAULT_DIR/Content/LinkedIn"
  cat > "$LINKEDIN_INDEX" <<'EOF'
# LinkedIn Content Index

IBM Planning Analytics LinkedIn posts and digests organized by year-month.

```dataview
TABLE file.mtime as Modified
FROM "Content/LinkedIn"
SORT file.name DESC
```
EOF
  echo "✓ Created LinkedIn content index note"
fi

# 6. Update Dashboard with comprehensive stats
DASHBOARD="$VAULT_DIR/Dashboard.md"
TOTAL_RESEARCH=$(find research -name '????-??-??-*.md' 2>/dev/null | wc -l)
TOTAL_CONTENT=$(find content -maxdepth 1 -name '????-??-??-*.md' 2>/dev/null | grep -v 'linkedin-pa' | wc -l)
TOTAL_LINKEDIN=$(find content -maxdepth 1 -name '????-??-??-*linkedin-pa*.md' 2>/dev/null | wc -l)
TOTAL_DAILY=$(find Daily -name '*.md' 2>/dev/null | wc -l)

cat > "$DASHBOARD" <<EOF
# OpenClaw Dashboard

**Last sync:** $(date -u '+%Y-%m-%d %H:%M UTC')

## Archive Stats
- Research reports: $TOTAL_RESEARCH
- Content files: $TOTAL_CONTENT
- LinkedIn PA posts: $TOTAL_LINKEDIN
- Daily notes: $TOTAL_DAILY
- Workspace disk: $(df -h "$WORKSPACE" | awk 'NR==2 {print $5 " used"}')

## Quick Links
- [[Research/Index|Research Index]]
- [[Content/Index|Content Index]]
- [[LinkedIn/Index|LinkedIn Content]]
- [[Daily|Daily Notes]]

## Upcoming Indonesian Holidays
$(./quick holidays 2>/dev/null | sed -n '4,13p' | sed 's/^/ - /' || echo " - (none this month)")

## Recent Research (latest 5)
\`\`\`dataview
TABLE file.mtime as Modified
FROM "Research"
SORT file.name DESC
LIMIT 5
\`\`\`
EOF
echo "✓ Updated dashboard"

echo ""
echo "✅ Sync complete! All research and content archives are now in the vault."
echo "   Use Obsidian's file pane or Dataview queries to browse."
