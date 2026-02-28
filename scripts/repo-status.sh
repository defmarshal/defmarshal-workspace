#!/usr/bin/env bash
set -euo pipefail
# Show git repository status (branch, remote, recent commits)

WORKSPACE="/home/ubuntu/.openclaw/workspace"

cd "$WORKSPACE" || exit 1

echo "Git Repository Status"
echo "---------------------"

# Current branch
BRANCH=$(git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD)
echo "Current branch: $BRANCH"

# Remote and tracking
REMOTE=$(git config --get branch.$BRANCH.remote 2>/dev/null || echo "no remote")
if [ -n "$REMOTE" ]; then
  REMOTE_URL=$(git config --get remote.$REMOTE.url 2>/dev/null || echo "unknown")
  echo "Tracking remote: $REMOTE ($REMOTE_URL)"
else
  echo "Tracking remote: none"
fi

# Ahead/behind
if [ "$REMOTE" != "no remote" ] && [ "$REMOTE" != "" ]; then
  git fetch --quiet 2>/dev/null
  AHEAD=$(git rev-list --count HEAD...@"$REMOTE"/"$BRANCH" 2>/dev/null || echo 0)
  BEHIND=$(git rev-list --count @"$REMOTE"/"$BRANCH"...HEAD 2>/dev/null || echo 0)
  if [ "$AHEAD" -gt 0 ] || [ "$BEHIND" -gt 0 ]; then
    echo "Sync status: ahead $AHEAD, behind $BEHIND"
  else
    echo "Sync status: up to date"
  fi
fi

# Recent commits (last 3)
echo
echo "Recent commits:"
git log --oneline -3 --decorate --graph 2>/dev/null || git log --oneline -3

# Working tree status
echo
if git status --porcelain | grep -q .; then
  echo "Working tree:"
  git status --short
else
  echo "Working tree: clean"
fi
