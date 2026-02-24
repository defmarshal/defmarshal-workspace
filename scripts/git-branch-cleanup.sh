#!/usr/bin/env bash
# Clean up stale feature branches (idea/*, hotfix/*, etc.) older than 30 days
# Prompts for confirmation before deletion.

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

echo "Stale Branch Cleanup"
echo "--------------------"
echo "This will list branches older than 30 days (not including main/master/develop)."
echo

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Find stale branches
STALE_BRANCHES=$(git branch --list --sort=-committerdate | while read -r branch; do
  # Skip current branch, main, master, develop
  if [ "$branch" = "$CURRENT_BRANCH" ] || [ "$branch" = "main" ] || [ "$branch" = "master" ] || [ "$branch" = "develop" ]; then
    continue
  fi
  # Get last commit date
  LAST_COMMIT=$(git log -1 --format=%ci "$branch" 2>/dev/null)
  if [ -n "$LAST_COMMIT" ]; then
    LAST_EPOCH=$(date -d "$LAST_COMMIT" +%s 2>/dev/null || echo 0)
    NOW_EPOCH=$(date +%s)
    AGE_DAYS=$(( (NOW_EPOCH - LAST_EPOCH) / 86400 ))
    if [ "$AGE_DAYS" -gt 30 ]; then
      echo "$branch|$AGE_DAYS days|$LAST_COMMIT"
    fi
  fi
done)

if [ -z "$STALE_BRANCHES" ]; then
  echo "✅ No stale branches found (older than 30 days)."
  exit 0
fi

echo "Stale branches (older than 30 days):"
echo
printf "%-30s %-12s %s\n" "BRANCH" "AGE" "LAST COMMIT"
echo "------------------------------------------------------------"
echo "$STALE_BRANCHES" | while IFS='|' read -r branch age last; do
  printf "%-30s %-12s %s\n" "$branch" "$age" "${last:0:19}"
done
echo
read -p "Delete these branches? (yes/no): " CONFIRM
if [ "$CONFIRM" = "yes" ]; then
  echo "$STALE_BRANCHES" | cut -d'|' -f1 | while read -r branch; do
    git branch -D "$branch" 2>/dev/null && echo "🗑️  Deleted: $branch" || echo "❌ Failed: $branch"
  done
  echo "Cleanup complete."
else
  echo "Aborted."
fi
