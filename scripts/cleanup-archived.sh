#!/usr/bin/env bash
# Clean up archived files older than 90 days (dry-run by default)

WORKSPACE="/home/ubuntu/.openclaw/workspace"
ARCHIVE_DIR="${ARCHIVE_DIR:-$WORKSPACE/archive}"

echo "Archive Cleanup"
echo "---------------"

if [ ! -d "$ARCHIVE_DIR" ]; then
  echo "Archive directory not found: $ARCHIVE_DIR"
  exit 0
fi

# Find files older than 90 days, null-separated
mapfile -d '' old_files < <(find "$ARCHIVE_DIR" -type f -mtime +90 -print0 2>/dev/null)

count=${#old_files[@]}

if [ $count -eq 0 ]; then
  echo "No archived files older than 90 days."
  exit 0
fi

echo "Found $count archived files older than 90 days:"
printf '  %s\n' "${old_files[@]}"

if [ "${1:-}" = "--execute" ]; then
  echo
  echo "Deleting..."
  printf '%s\0' "${old_files[@]}" | xargs -0 rm -f
  echo "Done."
else
  echo
  echo "Dry-run: use '--execute' to actually delete these files."
fi
