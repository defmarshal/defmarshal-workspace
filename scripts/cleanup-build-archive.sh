#!/usr/bin/env bash
# cleanup-build-archive — prune old build directories in builds/
# Default: dry-run, keep 10 newest builds. Use --execute to delete.

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
BUILDS_DIR="$WORKSPACE/builds"

# Defaults
DRY_RUN=1
KEEP=10

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --execute)
      DRY_RUN=0
      shift
      ;;
    --keep)
      KEEP="${2:?missing number}"
      shift 2
      ;;
    *)
      echo "Usage: $0 [--keep N] [--execute]" >&2
      exit 1
      ;;
  esac
done

# Ensure builds directory exists
if [ ! -d "$BUILDS_DIR" ]; then
  echo "Builds directory not found: $BUILDS_DIR"
  exit 0
fi

# Gather all build directories matching build-* pattern (non-recursive)
mapfile -t all_builds < <(find "$BUILDS_DIR" -maxdepth 1 -type d -name "build-*" | sort -r)

total=${#all_builds[@]}

if [ "$total" -le "$KEEP" ]; then
  echo "Build archive: $total builds, keeping $KEEP → nothing to do"
  exit 0
fi

# Determine which to delete: skip the first $KEEP (newest)
to_delete=("${all_builds[@]:KEEP}")
remove_count=${#to_delete[@]}

echo "Build archive cleanup:"
echo "  Total builds: $total"
echo "  Keeping: $KEEP newest"
echo "  To remove: $remove_count"

if [ "$DRY_RUN" -eq 1 ]; then
  echo "  (dry-run) Would remove:"
  for d in "${to_delete[@]}"; do
    echo "    $d"
  done
  # Exit code 2 indicates there are items to delete (dry-run)
  exit 2
else
  echo "  Removing..."
  for d in "${to_delete[@]}"; do
    rm -rf "$d"
    echo "    removed $d"
  done
  exit 0
fi
