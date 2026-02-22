#!/usr/bin/env bash
# Prebuild: Copy research markdown files into Research Hub's public directory
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
SOURCE="$WORKSPACE/research"
DEST="$WORKSPACE/apps/research-hub/public/research"

echo "=== Research Hub Prebuild ==="
echo "Copying research files from: $SOURCE"
echo "To: $DEST"

# Ensure source exists
if [ ! -d "$SOURCE" ]; then
  echo "Error: Source directory $SOURCE does not exist"
  exit 1
fi

# Create destination if it doesn't exist
mkdir -p "$DEST"

# Copy all markdown and mp3 files (rsync for efficiency)
echo "Syncing files..."
rsync -av --delete --include="*.md" --include="*.mp3" --exclude="*" "$SOURCE/" "$DEST/"

echo "✅ Prebuild complete: $(ls -1 "$DEST" | wc -l) research files in $DEST"
