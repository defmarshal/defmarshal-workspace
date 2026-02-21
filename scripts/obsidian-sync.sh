#!/usr/bin/env bash
# obsidian-sync - Sync OpenClaw outputs to Obsidian vault (full-featured)
# Creates daily notes, copies research with tags, updates dashboards, gaps, weekly

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
VAULT_DIR="${OBSIDIAN_VAULT:-$HOME/obsidian-vault}"

echo "Syncing OpenClaw outputs to Obsidian vault at: $VAULT_DIR"
echo "--------------------------------"

# Ensure vault structure exists
mkdir -p "$VAULT_DIR"/{Daily,Research,Content,Planning,Weekly,Dashboards}

DATE=$(date +%Y-%m-%d)
DAILY_NOTE="$VAULT_DIR/Daily/$DATE.md"

# ===== 1. DAILY NOTE =====
echo "📅 Building daily note..."
SUMMARY="# ${DATE} — OpenClaw Daily\n\n"
SUMMARY+="**Generated:** $(date -u '+%Y-%m-%d %H:%M UTC')\n\n"

# Health snapshot
HEALTH=$(./quick health 2>/dev/null || echo "N/A")
SUMMARY+="## 🏥 System Health\n"
SUMMARY+="- $(echo "$HEALTH" | head -1)\n"
SUMMARY+="- Memory: $(./quick memory-status 2>/dev/null | head -1 || echo "N/A")\n"
SUMMARY+="- Gateway: $(openclaw gateway status 2>/dev/null | head -1 || echo "N/A")\n\n"

# Research today
shopt -s nullglob
RESEARCH_FILES=(research/${DATE}-*.md)
RESEARCH_COUNT=${#RESEARCH_FILES[@]}
shopt -u nullglob
if [ "$RESEARCH_COUNT" -gt 0 ]; then
  SUMMARY+="## 🔬 Research Today ($RESEARCH_COUNT)\n"
  for f in "${RESEARCH_FILES[@]}"; do
    [ -e "$f" ] || continue
    TITLE=$(head -1 "$f" | sed 's/^# //')
    CATEGORY=$(echo "$f" | grep -oE 'research/[0-9-]+-[a-z]+' | sed 's/^research\///')
    SUMMARY+="- [[$TITLE]] (./${CATEGORY}/$(basename $f .md))\n"
  done
  SUMMARY+="\n"
fi

# Content today
shopt -s nullglob
CONTENT_FILES=(content/${DATE}-*.md)
CONTENT_COUNT=${#CONTENT_FILES[@]}
shopt -u nullglob
if [ "$CONTENT_COUNT" -gt 0 ]; then
  SUMMARY+="## 📝 Content Today ($CONTENT_COUNT)\n"
  for f in "${CONTENT_FILES[@]}"; do
    [ -e "$f" ] || continue
    TITLE=$(head -1 "$f" | sed 's/^# //')
    SUMMARY+="- [[$TITLE]] (./content/$(basename $f .md))\n"
  done
  SUMMARY+="\n"
fi

# Link to Dashboard and Gaps
SUMMARY+="## 📊 Quick Links\n- [[Dashboards/Overview]]\n- [[Planning/Research Gaps]]\n"

echo -e "$SUMMARY" > "$DAILY_NOTE"
echo "✓ Daily note: $DAILY_NOTE"

# ===== 2. COPY RESEARCH WITH TAGGING =====
echo "🔬 Syncing research files..."
RESEARCH_VAULT="$VAULT_DIR/Research/$(date +%Y-%m)"
mkdir -p "$RESEARCH_VAULT"

# Function to extract category from filename: 2026-02-21-<category>-...
extract_category() {
  local filename=$(basename "$1" .md)
  # Remove date prefix (YYYY-MM-DD-) and get the category part (everything until next hyphen)
  local cat=$(echo "$filename" | sed -E 's/^[0-9]{4}-[0-9]{2}-[0-9]{2}-//' | cut -d'-' -f1)
  echo "$cat"
}

# Function to guess tags based on category and filename
guess_tags() {
  local category="$1"
  # Build a space-separated string of tags
  local tags=""
  case "$category" in
    anime*) tags="anime entertainment";;
    ai|llm|open-source-llm) tags="ai machine-learning";;
    banking|cbdc) tags="fintech finance";;
    quantum) tags="quantum physics";;
    edge-ai|nvidia|blackwell) tags="hardware infrastructure";;
    serverless|kubernetes) tags="devops cloud";;
    brownfield|ai-agent-frameworks) tags="software-engineering";;
    leo-satellite) tags="space telecom";;
    *) tags="misc";;
  esac
  echo "$tags"
}

for f in research/${DATE}-*.md; do
  [ -e "$f" ] || continue
  CATEGORY=$(extract_category "$f")
  DEST="$RESEARCH_VAULT/$(basename $f)"
  
  # Add frontmatter if not present
  if ! head -1 "$f" | grep -q '^---'; then
    TAGS=$(guess_tags "$CATEGORY" | sed 's/ /, /g')
    TITLE=$(head -1 "$f" | sed 's/^# //')
    {
      echo "---"
      echo "title: \"$TITLE\""
      echo "date: $(echo "$f" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')"
      echo "category: $CATEGORY"
      echo "tags: [$TAGS]"
      echo "source: openclaw-research"
      echo "---"
      cat "$f"
    } > "$DEST.tmp"
    mv "$DEST.tmp" "$DEST"
    echo "  ✓ Enhanced $(basename $f) with frontmatter"
  else
    cp "$f" "$DEST"
    echo "  ✓ Copied $(basename $f)"
  fi
done

# ===== 3. CONTENT FOLDERS =====
echo "📝 Syncing content files..."
CONTENT_VAULT="$VAULT_DIR/Content/$(date +%Y-%m)"
mkdir -p "$CONTENT_VAULT"
for f in content/${DATE}-*.md; do
  [ -e "$f" ] || continue
  cp "$f" "$CONTENT_VAULT/"
  echo "  ✓ Copied $(basename $f)"
done

# ===== 4. DASHBOARDS =====
echo "📊 Updating dashboards..."
TOTAL_RESEARCH=$(find research -name '*.md' 2>/dev/null | wc -l)
TOTAL_CONTENT=$(find content -name '*.md' 2>/dev/null | wc -l)

# Overview dashboard
cat > "$VAULT_DIR/Dashboards/Overview.md" <<EOF
# OpenClaw Overview

**Last sync:** $(date -u '+%Y-%m-%d %H:%M UTC')

## 📈 Stats

- **Total research**: $TOTAL_RESEARCH
- **Total content**: $TOTAL_CONTENT
- **Vault disk usage**: $(df -h "$VAULT_DIR" | awk 'NR==2 {print $5 " used"}')

## 🔬 Latest Research (by mtime)

\`\`\`dataview
TABLE file.mtime as Updated, tags
FROM "Research"
SORT file.mtime DESC
LIMIT 15
\`\`\`

## 📝 Recent Content

\`\`\`dataview
TABLE file.mtime as Updated
FROM "Content"
SORT file.mtime DESC
LIMIT 10
\`\`\`

## 🏷️ Browse by Tag

\`\`\`dataview
TABLE count(links) as Mentions
FROM #ai OR #anime OR #finance OR #devops OR #hardware
WHERE file.etags != null
SORT Mentions DESC
\`\`\`

## 🔗 Quick Links

- [[Research Index]] — full list
- [[Planning/Research Gaps]] — what's next
- [[Weekly/$(date +%Y-%W)]]

EOF
echo "✓ Dashboard: Dashboards/Overview.md"

# Research index (aggregated over all months)
cat > "$VAULT_DIR/Research/Index.md" <<'EOF'
# Research Index

All research reports organized by date.

```dataview
TABLE file.mtime as Updated, category, join(tags, ", ") as Tags
FROM "Research"
SORT file.mtime DESC
```

## By Category

```dataview
TASK
WHERE category != null
GROUP BY category
SORT category ASC
```
EOF

# ===== 5. GAPS KANBAN =====
"$WORKSPACE/scripts/obsidian-gaps.sh"

# ===== 6. WEEKLY SUMMARY (if needed) =====
# Only create weekly note if it doesn't exist (avoid overwriting manual edits)
WEEKLY_DIR="$VAULT_DIR/Weekly"
YEAR=$(date +%Y)
WEEK=$(date +%V)
WEEKLY_NOTE="$WEEKLY_DIR/${YEAR}-W${WEEK}.md"
if [ ! -f "$WEEKLY_NOTE" ]; then
  "$WORKSPACE/scripts/obsidian-weekly.sh"
fi

echo ""
echo "✅ Sync complete! Open Obsidian and refresh the vault."
echo "   Install: Dataview (required), Kanban (for gaps), Calendar (optional)"
echo "   Vault location: $VAULT_DIR"
