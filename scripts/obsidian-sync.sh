#!/usr/bin/env bash
# obsidian-sync - Sync OpenClaw outputs to an Obsidian vault (plain markdown approach)
# Works without external CLI tools — just copy/transform files.

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
VAULT_DIR="${OBSIDIAN_VAULT:-$HOME/obsidian-vault}"
mkdir -p "$VAULT_DIR"

echo "Syncing OpenClaw outputs to Obsidian vault at: $VAULT_DIR"

# 1. Daily note (YYYY-MM-DD.md in vault root or Daily Notes folder)
DATE=$(date +%Y-%m-%d)
DAILY_NOTE="$VAULT_DIR/$DATE.md"
mkdir -p "$VAULT_DIR/Daily"

# Build daily summary
SUMMARY="# $DATE — OpenClaw Summary\n\n"
SUMMARY+="**Generated:** $(date -u '+%Y-%m-%d %H:%M UTC')\n\n"

# Research today
RESEARCH_COUNT=$(ls -1 research/${DATE}-*.md 2>/dev/null | wc -l)
if [ "$RESEARCH_COUNT" -gt 0 ]; then
  SUMMARY+="## Research ($RESEARCH_COUNT)\n"
  for f in research/${DATE}-*.md; do
    [ -e "$f" ] || continue
    TITLE=$(head -1 "$f" | sed 's/^# //;s/\.md$//')
    SUMMARY+="- [[$TITLE]] (research/$(basename $f))\n"
  done
  SUMMARY+="\n"
fi

# Content today
CONTENT_COUNT=$(ls -1 content/${DATE}-*.md 2>/dev/null | wc -l)
if [ "$CONTENT_COUNT" -gt 0 ]; then
  SUMMARY+="## Content ($CONTENT_COUNT)\n"
  for f in content/${DATE}-*.md; do
    [ -e "$f" ] || continue
    TITLE=$(head -1 "$f" | sed 's/^# //;s/\.md$//')
    SUMMARY+="- [[$TITLE]] (content/$(basename $f))\n"
  done
  SUMMARY+="\n"
fi

# System health
HEALTH=$(./quick health 2>/dev/null || echo "N/A")
SUMMARY+="## System Health\n"
SUMMARY+="- $(echo "$HEALTH" | head -1)\n"
SUMMARY+="- Memory: $(./quick memory-status 2>/dev/null | head -1 || echo "N/A")\n"
SUMMARY+="- Gateway: $(openclaw gateway status 2>/dev/null | head -1 || echo "N/A")\n"

# Write daily note
echo -e "$SUMMARY" > "$DAILY_NOTE"
echo "✓ Created daily note: $DAILY_NOTE"

# 2. Create an index note for latest research (if it doesn't exist or update it)
INDEX_NOTE="$VAULT_DIR/Research/Index.md"
mkdir -p "$VAULT_DIR/Research"
if [ ! -f "$INDEX_NOTE" ]; then
  cat > "$INDEX_NOTE" <<'EOF'
# Research Index

This note is auto-generated. It lists all research reports by date.

```dataview
TABLE file.mtime as Updated
FROM "Research"
SORT file.name DESC
```
EOF
  echo "✓ Created research index"
fi

# 3. Copy today's research files to vault (as symlinks or copies)
RESEARCH_VAULT="$VAULT_DIR/Research/$(date +%Y-%m)"
mkdir -p "$RESEARCH_VAULT"
for f in research/${DATE}-*.md; do
  [ -e "$f" ] || continue
  DEST="$RESEARCH_VAULT/$(basename $f)"
  if [ ! -f "$DEST" ]; then
    cp "$f" "$DEST"
    echo "✓ Copied $(basename $f) to vault"
  fi
done

# 4. Create/update a dashboard note with stats
DASHBOARD="$VAULT_DIR/Dashboard.md"
TOTAL_RESEARCH=$(ls research/*.md 2>/dev/null | wc -l)
TOTAL_CONTENT=$(ls content/*.md 2>/dev/null | wc -l)
cat > "$DASHBOARD" <<EOF
# OpenClaw Dashboard

**Last updated:** $(date -u '+%Y-%m-%d %H:%M UTC')

## Stats
- Research reports: $TOTAL_RESEARCH
- Content files: $TOTAL_CONTENT
- Disk usage: $(df -h . | awk 'NR==2 {print $5}')

## Latest Research

\`\`\`dataview
TABLE file.mtime as Updated
FROM "Research"
SORT file.mtime DESC
LIMIT 10
\`\`\`

## Upcoming Holidays
$(./quick holidays 2>/dev/null | head -10 | sed 's/^/ - /')
EOF
echo "✓ Updated dashboard"

echo ""
echo "Sync complete! Open your Obsidian vault to see changes."
echo "If you use Dataview plugin, the dashboard and index will show live tables."
