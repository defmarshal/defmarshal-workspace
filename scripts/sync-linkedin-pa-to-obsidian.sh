#!/usr/bin/env bash
# Sync LinkedIn PA content to Obsidian vault

WORKSPACE="/home/ubuntu/.openclaw/workspace"
CONTENT_DIR="$WORKSPACE/content/linkedin-pa"

# Configurable Obsidian vault path (set in env or default)
OBSIDIAN_VAULT="${OBSIDIAN_VAULT:-$HOME/Documents/Obsidian/PlanningAnalytics}"

echo "Syncing LinkedIn PA content to Obsidian vault..."
echo "Source: $CONTENT_DIR"
echo "Target: $OBSIDIAN_VAULT"

if [ ! -d "$CONTENT_DIR" ]; then
  echo "Error: Content directory not found: $CONTENT_DIR"
  exit 1
fi

# Create vault if missing
mkdir -p "$OBSIDIAN_VAULT"

# Copy all markdown files, preserving dates
echo "Copying files..."
cp -a "$CONTENT_DIR"/*.md "$OBSIDIAN_VAULT/" 2>/dev/null || true

# Count copied files
copied=$(ls -1 "$OBSIDIAN_VAULT"/*.md 2>/dev/null | wc -l)
echo "✅ Synced $copied files to Obsidian vault"

# Optional: print latest file
latest=$(ls -1t "$OBSIDIAN_VAULT"/*.md 2>/dev/null | head -1)
if [ -n "$latest" ]; then
  echo "Latest: $(basename "$latest")"
fi
