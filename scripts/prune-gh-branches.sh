#!/usr/bin/env bash
# prune-gh-branches.sh — safely delete stale gh-pages-* and gh-deploy local branches
# These are development/test branches from Feb 2026 with no active purpose.
# Usage: scripts/prune-gh-branches.sh [--execute]
# Default: dry-run
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

DRY_RUN=true
[[ "${1:-}" == "--execute" ]] && DRY_RUN=false

# Branches to consider for pruning (not master, not idea/*, not feature branches)
CANDIDATES=(gh-deploy gh-pages gh-pages-deploy gh-pages-test)

echo "== GH Branch Prune $(date -u -Iseconds) =="
echo "Mode: $([ "$DRY_RUN" = true ] && echo 'dry-run' || echo 'execute')"
echo ""

PRUNED=0
for branch in "${CANDIDATES[@]}"; do
  if ! git branch --list "$branch" | grep -q "$branch"; then
    echo "  SKIP: $branch (does not exist)"
    continue
  fi

  # Check if merged into master
  if git merge-base --is-ancestor "$branch" master 2>/dev/null; then
    status="merged"
  else
    # Count commits ahead of master
    ahead=$(git log --oneline master.."$branch" 2>/dev/null | wc -l)
    status="${ahead} commits ahead (unmerged)"
  fi

  last_commit=$(git log -1 --format="%ai %s" "$branch" 2>/dev/null | cut -c1-60)

  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY] Would delete: $branch ($status)"
    echo "        Last: $last_commit"
  else
    git branch -D "$branch"
    echo "  [OK] Deleted: $branch ($status)"
    PRUNED=$((PRUNED + 1))
  fi
done

echo ""
if [ "$DRY_RUN" = true ]; then
  echo "Dry-run complete. Pass --execute to delete branches."
else
  echo "Pruned ${PRUNED} branch(es)."
fi
