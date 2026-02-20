#!/usr/bin/env bash
# Prebuild: Copy research markdown files into the app's public data directory
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
APP_DIR="$WORKSPACE/apps/research-hub"
RESEARCH_SRC="${RESEARCH_PATH:-$WORKSPACE/research}"
DEST_DIR="$APP_DIR/public/research"

mkdir -p "$DEST_DIR"
echo "Copying research files from $RESEARCH_SRC to $DEST_DIR"
cp "$RESEARCH_SRC"/*.md "$DEST_DIR/" 2>/dev/null || echo "No research files found"
echo "Copied $(ls -1 "$DEST_DIR" | wc -l) files"
