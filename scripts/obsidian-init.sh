#!/usr/bin/env bash
# obsidian-init — Set up a fresh Obsidian vault with OpenClaw integrations

set -euo pipefail

VAULT_DIR="${OBSIDIAN_VAULT:-$HOME/obsidian-vault}"

if [ -d "$VAULT_DIR" ] && [ "$(ls -A "$VAULT_DIR")" ]; then
  echo "ERROR: Vault directory '$VAULT_DIR' is not empty. Remove or choose another location." >&2
  exit 1
fi

mkdir -p "$VAULT_DIR"/{Daily,Research,Content,Planning,Weekly,Dashboards}

# Create initial README for the vault
cat > "$VAULT_DIR/README.md" <<'EOF'
# OpenClaw Knowledge Vault

This vault is automatically synchronized with the OpenClaw workspace.

## Folders

- **Daily** — daily notes (auto‑created)
- **Research** — research reports by year-month
- **Content** — content digests
- **Planning** — Kanban boards, todo lists
- **Weekly** — weekly summary notes
- **Dashboards** — curated Dataview queries

## Plugins to Install

- **Dataview** — for live queries (essential)
- **Kanban** — for gap tracking
- **Calendar** — for daily notes navigation
- **QuickAdd** — for rapid capture

## Sync

Run `quick obsidian-sync` from the OpenClaw workspace to update this vault.

EOF

# Create dashboard template
cat > "$VAULT_DIR/Dashboards/Overview.md" <<'EOF'
# OpenClaw Overview

**Last sync:** `=date(this.file.mtime)`

## All Recent Research

```dataview
TABLE file.mtime as Updated, join(tags, ", ") as Tags
FROM "Research"
SORT file.mtime DESC
LIMIT 20
```

## Content This Month

```dataview
TABLE file.mtime as Updated
FROM "Content"
WHERE file.mtime >= this.week
SORT file.mtime DESC
```

## Upcoming Events

```dataview
TABLE date as Date, description as Event
FROM "Daily"
WHERE contains(text, "Holiday") OR contains(text, "Event")
SORT date ASC
LIMIT 10
```

EOF

echo "✓ Obsidian vault initialized at: $VAULT_DIR"
echo "  Open Obsidian → Open folder as vault → install Dataview & Kanban"
echo "  Then run: quick obsidian-sync"
