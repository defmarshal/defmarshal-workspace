#!/usr/bin/env bash
# Check if the standalone game repo is in sync with the main workspace
# Usage: quick game-repo-sync

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
STANDALONE="/tmp/openclaw-idle-rpg-standalone"

echo "=== OpenClaw Idle RPG Repo Sync Check ==="
echo ""

if [ ! -d "$STANDALONE/.git" ]; then
  echo "❌ Standalone repo not found at $STANDALONE"
  echo "   Run ./setup-standalone-repo.sh to initialize"
  exit 1
fi

cd "$STANDALONE"

# Check if remote is configured
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "❌ No remote 'origin' configured in standalone repo"
  exit 1
fi

# Fetch latest from remote
echo "🔄 Fetching from remote..."
git fetch origin >/dev/null 2>&1

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Current branch: $CURRENT_BRANCH"
echo ""

# Check if local is ahead/behind
AHEAD=$(git rev-list --count HEAD@{upstream}..HEAD 2>/dev/null || echo 0)
BEHIND=$(git rev-list --count HEAD..HEAD@{upstream} 2>/dev/null || echo 0)

if [ "$AHEAD" -gt 0 ] && [ "$BEHIND" -gt 0 ]; then
  echo "⚠️  Diverged: ahead by $AHEAD, behind by $BEHIND"
  echo "   Consider pulling or pushing to reconcile"
  exit 2
elif [ "$AHEAD" -gt 0 ]; then
  echo "✅ Local is ahead by $AHEAD commit(s)"
  echo "   Run: git push origin $CURRENT_BRANCH"
  exit 0
elif [ "$BEHIND" -gt 0 ]; then
  echo "⚠️  Local is behind by $BEHIND commit(s)"
  echo "   Run: git pull origin $CURRENT_BRANCH"
  exit 1
else
  echo "✅ Local and remote are in sync!"
  exit 0
fi
