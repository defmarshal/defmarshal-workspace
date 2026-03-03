#!/usr/bin/env bash
# Archive old downloads to tar.gz to reclaim disk space
# Usage: ./quick archive-downloads [--days N] [--execute] [--dry-run]
# Default: --days 14 (archive folders older than 14 days)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

DAYS=14
DRY_RUN=true
EXECUTE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --days) DAYS="$2"; shift 2 ;;
    --execute) EXECUTE=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help) echo "Archive old downloads to tar.gz. Options: --days N, --execute, --dry-run, -h"; exit 0 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

echo "Scanning downloads/ for folders older than $DAYS days..."
echo "Dry run: $DRY_RUN | Execute: $EXECUTE"
echo ""

# Find directories older than DAYS (excluding already archived .tar.gz)
mapfile -t TARGETS < <(find downloads -maxdepth 1 -type d ! -name '.*' -mtime +"$DAYS" | sort)

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  echo "No folders older than $DAYS days to archive."
  exit 0
fi

TOTAL_SAVED=0
for DIR in "${TARGETS[@]}"; do
  # Skip if not a directory
  [[ -d "$DIR" ]] || continue

  # Archive name: folder path with .tar.gz
  ARCHIVE="${DIR}.tar.gz"

  # Skip if archive already exists
  if [[ -f "$ARCHIVE" ]]; then
    echo "SKIP: Archive already exists: $ARCHIVE"
    continue
  fi

  ORIG_SIZE=$(du -sm "$DIR" 2>/dev/null | awk '{print $1}')
  echo "Processing: $DIR (${ORIG_SIZE}MB)"

  if $EXECUTE; then
    echo "  → Creating archive..."
    tar -czf "$ARCHIVE" -C downloads "$(basename "$DIR")" 2>/dev/null
    if [[ $? -eq 0 ]]; then
      ARCHIVE_SIZE=$(du -sm "$ARCHIVE" 2>/dev/null | awk '{print $1}')
      SAVED=$((ORIG_SIZE - ARCHIVE_SIZE))
      TOTAL_SAVED=$((TOTAL_SAVED + SAVED))
      echo "  ✓ Archived. Original: ${ORIG_SIZE}MB, Archive: ${ARCHIVE_SIZE}MB, Saved: ${SAVED}MB"
      echo "  → Removing original directory..."
      rm -rf "$DIR"
      echo "  ✓ Removed."
    else
      echo "  ✗ Archive failed for $DIR"
    fi
  else
    echo "  [DRY RUN] Would create: $ARCHIVE and remove $DIR (estimated savings: ~$((ORIG_SIZE/2))MB)"
  fi
done

if $EXECUTE; then
  echo ""
  echo "Total space saved in this run: ${TOTAL_SAVED}MB"
else
  echo ""
  echo "This was a dry run. Run with --execute to perform archiving."
fi
