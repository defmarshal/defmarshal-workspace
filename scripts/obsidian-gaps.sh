#!/usr/bin/env bash
# obsidian-gaps — Create/update a Kanban board of research gaps in Obsidian
# Reads research/INDEX.md to identify 🟡 MEDIUM and 🔴 HIGH gaps

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
VAULT_DIR="${OBSIDIAN_VAULT:-$HOME/obsidian-vault}"
INDEX_FILE="$WORKSPACE/research/INDEX.md"

if [ ! -f "$INDEX_FILE" ]; then
  echo "ERROR: Research index not found at $INDEX_FILE" >&2
  exit 1
fi

mkdir -p "$VAULT_DIR/Planning"

KANBAN="$VAULT_DIR/Planning/Research Gaps.md"

# Parse gaps from INDEX.md; allow grep to fail without aborting
# Look for lines like: - [🟡 MEDIUM] ...
MEDIUM_GAPS=$( { grep -E '\[🟡 MEDIUM\]' "$INDEX_FILE" 2>/dev/null || true; } | sed -E 's/^- \[🟡 MEDIUM\] //;s/\[🟡 MEDIUM\]/- [ ] /' )
HIGH_GAPS=$( { grep -E '\[🔴 HIGH\]' "$INDEX_FILE" 2>/dev/null || true; } | sed -E 's/^- \[🔴 HIGH\] //;s/\[🔴 HIGH\]/- [ ] /' )

cat > "$KANBAN" <<EOF
# Research Gaps — Kanban

**Auto‑generated** from research/INDEX.md. Drag cards in Obsidian (Kanban plugin).

## 🟡 MEDIUM PRIORITY

$( [ -n "$MEDIUM_GAPS" ] && echo "$MEDIUM_GAPS" || echo "*No medium gaps tracked*" )

## 🔴 HIGH PRIORITY

$( [ -n "$HIGH_GAPS" ] && echo "$HIGH_GAPS" || echo "*All high gaps cleared!*" )

---

## DONE (Archived)

Move completed research here with a brief result link:

- [x] Example: Anime Streaming Economics → [[2026-02-21-anime-streaming-economics-revenue-growth-cac]]
- [x] Example: CBDC & Stablecoin Reality Check → [[2026-02-21-cbdc-stablecoin-scaling-compliance]]

*Last updated: $(date -u '+%Y-%m-%d %H:%M UTC')*
EOF

echo "✓ Kanban board updated: $KANBAN"
