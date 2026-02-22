#!/usr/bin/env bash
# Safe git sync: fetch, check status, and optionally pull
# Usage: git-sync [--pull]

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

# Fetch all remotes
echo "Fetching from origin..."
git fetch --prune origin

# Check if any uncommitted changes
if [[ -n "$(git status --porcelain)" ]]; then
  echo "WARNING: Uncommitted changes present. Please commit or stash before pulling."
  git status --short
  exit 1
fi

# Check if local is behind
behind=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo 0)
ahead=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo 0)

if [ "$ahead" -gt 0 ]; then
  echo "Local is ahead by $ahead commit(s). Need to push."
  git log --oneline @{u}..HEAD
fi

if [ "$behind" -gt 0 ]; then
  echo "Local is behind by $behind commit(s)."
  if [[ "${1:-}" == "--pull" ]]; then
    echo "Pulling changes..."
    git pull --ff-only origin master
    echo "Pull complete."
  else
    echo "Run '$0 --pull' to merge changes."
    git log --oneline HEAD..@{u}
  fi
else
  echo "Up to date with origin/master."
fi
