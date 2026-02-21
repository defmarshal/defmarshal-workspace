#!/usr/bin/env bash
# Clean up merged Git branches (safe defaults)
# Usage: quick git-branch-clean [--dry-run] [--all]

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

DRY_RUN=true
INCLUDE_ALL=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --execute)
      DRY_RUN=false
      shift
      ;;
    --all)
      INCLUDE_ALL=true
      shift
      ;;
    -h|--help)
      cat <<EOF
Usage: quick git-branch-clean [OPTIONS]

Delete local branches that have been merged into the current branch.
By default, protects: master, main, and the current branch.

Options:
  --execute    Actually delete branches (default: dry-run only)
  --all        Also delete other branches merged into master (not just current)
  -h, --help   Show this help message

Examples:
  quick git-branch-clean          # Show what would be deleted (dry-run)
  quick git-branch-clean --execute  # Delete merged branches (safe)
  quick git-branch-clean --all --execute  # Aggressive cleanup (merged into master)
EOF
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
echo "Protected branches: master, main, $CURRENT_BRANCH"
echo ""

# Get merged branches
if [ "$INCLUDE_ALL" = true ]; then
  echo "Finding branches merged into master (excluding protected)..."
  MERGED=$(git branch --merged master | grep -vE "^\*| master$| main$")
else
  echo "Finding branches merged into $CURRENT_BRANCH (excluding protected)..."
  MERGED=$(git branch --merged "$CURRENT_BRANCH" | grep -vE "^\*| master$| main$| $CURRENT_BRANCH$")
fi

if [ -z "$MERGED" ]; then
  echo "✅ No merged branches to clean."
  exit 0
fi

echo "The following branches are merged and can be deleted:"
echo "$MERGED" | sed 's/^/  - /'
echo ""

if [ "$DRY_RUN" = true ]; then
  echo "💡 Dry-run mode. Use --execute to actually delete these branches."
  exit 0
fi

echo "Deleting..."
echo "$MERGED" | xargs git branch -d
echo "✅ Done."
