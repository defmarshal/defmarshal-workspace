#!/usr/bin/env bash
# cleanup-backups.sh - Prune old openclaw backup tarballs in /home/ubuntu
# Default: dry-run, keep most recent 1 backup. Use --execute to actually delete.

set -euo pipefail

# Config
TARGET_DIR="/home/ubuntu"
PATTERN="openclaw-backup-*.tar.gz"
KEEP=${CLEANUP_BACKUPS_KEEP:-1}  # Allow override via env
DRY_RUN=1
VERBOSE=0

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --execute)
      DRY_RUN=0
      shift
      ;;
    --keep)
      KEEP="$2"
      shift 2
      ;;
    --verbose|-v)
      VERBOSE=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
done

# Ensure KEEP is a positive integer
if ! [[ "$KEEP" =~ ^[0-9]+$ ]] || [[ "$KEEP" -lt 0 ]]; then
  echo "Invalid --keep value: $KEEP" >&2
  exit 1
fi

# Find matching backups, sorted by modification time (newest first)
mapfile -t backups < <(find "$TARGET_DIR" -maxdepth 1 -name "$PATTERN" -type f -printf "%T@ %p\n" 2>/dev/null | sort -nr | cut -d' ' -f2-)

total=${#backups[@]}
if (( total == 0 )); then
  echo "INFO: No backups found in $TARGET_DIR matching $PATTERN"
  exit 0
fi

if (( total <= KEEP )); then
  echo "INFO: Found $total backup(s), keep=$KEEP → nothing to delete."
  exit 0
fi

to_delete=(${backups[@]:KEEP})  # Skip the first $KEEP (newest)

echo "INFO: Found $total backup(s), keep=$KEEP → delete $((total - KEEP)) older(s)."
if (( VERBOSE )); then
  echo "KEEPING (newest $KEEP):"
  for ((i=0; i<KEEP && i<total; i++)); do
    echo "  - ${backups[i]}"
  done
fi
echo "TO DELETE:"
for f in "${to_delete[@]}"; do
  echo "  - $f"
done

if (( DRY_RUN )); then
  echo "DRY-RUN: No files deleted. Use --execute to perform deletion."
  exit 0
fi

# Confirm non-interactive: we already printed what will be deleted. Proceed.
echo "Executing deletion..."
deleted=0
for f in "${to_delete[@]}"; do
  if rm -f "$f"; then
    ((deleted++)) || true
    echo "  DELETED: $f"
  else
    echo "  ERROR: failed to delete $f" >&2
  fi
done

echo "DONE: Deleted $deleted file(s)."
exit 0
