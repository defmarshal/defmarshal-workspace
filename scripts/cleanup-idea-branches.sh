#!/usr/bin/env bash
# Clean up stale idea/* branches (merged or explicitly listed)

set -euo pipefail
WORKSPACE="${WORKSPACE:-/home/ubuntu/.openclaw/workspace}"
cd "$WORKSPACE"

# Refresh remote references
git fetch --prune origin

echo "Stale idea branches cleanup"
echo "--------------------------"

# Local branches: merged into current branch (master/main)
echo "Local branches (merged into current):"
merged_local=$(git branch --merged | grep '^[* ]*idea/' | sed 's/^[* ]*//' || true)
if [ -z "${merged_local:-}" ]; then
  echo "  (none)"
else
  echo "$merged_local"
fi

# Remote branches: merged into current branch
echo "Remote branches (merged into current):"
merged_remote=$(git branch -r --merged | grep 'origin/idea/' | sed 's|origin/||' || true)
if [ -z "${merged_remote:-}" ]; then
  echo "  (none)"
else
  echo "$merged_remote"
fi

# If --execute flag not provided, exit here (dry-run)
if [ "${1:-}" != "--execute" ]; then
  echo
  echo "Dry-run only. Use '$0 --execute' to delete these branches."
  exit 0
fi

# Deletion loop
deleted=0
for branch in ${merged_local:-}; do
  echo "Deleting local branch: $branch"
  git branch -d "$branch" 2>/dev/null || git branch -D "$branch"
  deleted=$((deleted+1))
done

for branch in ${merged_remote:-}; do
  echo "Deleting remote branch: origin/$branch"
  git push origin --delete "$branch"
  deleted=$((deleted+1))
done

echo "Cleanup complete. Deleted $deleted branch(es)."
