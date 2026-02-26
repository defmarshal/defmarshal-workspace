#!/usr/bin/env bash
# List local Git branches that haven't been merged and are older than 30 days.
# Helps clean up stale feature branches. Use --delete to actually delete them (dry-run by default).

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

# Threshold: branches with no commits in last 30 days
THRESHOLD_DAYS=30
THRESHOLD_SECONDS=$((THRESHOLD_DAYS * 86400))
NOW=$(date +%s)

# Get all local branches (excluding main/master and current branch)
CURRENT_BRANCH=$(git branch --show-current)
git for-each-ref --format='%(refname:short) %(committerdate:unix)' refs/heads/ | while read branch commit_ts; do
  # Skip current branch
  if [ "$branch" = "$CURRENT_BRANCH" ] || [ "$branch" = "master" ] || [ "$branch" = "main" ]; then
    continue
  fi
  AGE_SECONDS=$((NOW - commit_ts))
  if [ "$AGE_SECONDS" -gt "$THRESHOLD_SECONDS" ]; then
    DAYS_OLD=$((AGE_SECONDS / 86400))
    echo "$branch (last commit $DAYS_OLD days ago)"
  fi
done
