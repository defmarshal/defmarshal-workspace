#!/usr/bin/env bash
# Check Research Hub deployment status (local and Vercel)
# Usage: quick research-hub-status

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_HUB_REPO="https://github.com/defmarshal/research-hub"
VERCEL_PROJECT="research-hub-flame"

echo "=== Research Hub Deployment Status ==="
echo ""

# Check local standalone copy
STANDALONE="/tmp/research-hub-standalone"
if [ -d "$STANDALONE/.git" ]; then
  echo "📍 Local standalone repo: $STANDALONE"
  cd "$STANDALONE"
  LOCAL_BRANCH=$(git branch --show-current)
  echo "   Branch: $LOCAL_BRANCH"
  LOCAL_COMMIT=$(git rev-parse HEAD)
  echo "   Commit: ${LOCAL_COMMIT:0:8}"
  git fetch origin >/dev/null 2>&1
  REMOTE_COMMIT=$(git rev-parse origin/$LOCAL_BRANCH 2>/dev/null || echo "???")
  if [ "$REMOTE_COMMIT" = "$LOCAL_COMMIT" ]; then
    echo "   Status: ✅ In sync with remote"
  else
    echo "   Status: ⚠️  Diverged from remote ($REMOTE_COMMIT)"
  fi
else
  echo "❌ Local standalone repo not found at $STANDALONE"
  echo "   (Will be created when deployed via quick research-hub-deploy)"
fi

echo ""

# Check if Vercel project exists via vercel CLI
if command -v vercel &>/dev/null; then
  echo "🔗 Vercel project: $VERCEL_PROJECT"
  # Try to get project info quietly (may fail if not authenticated)
  if vercel ls --yes 2>/dev/null | grep -q "$VERCEL_PROJECT"; then
    echo "   Status: ✅ Project exists in Vercel"
    # Get latest deployment URL
    DEPLOY_URL=$(vercel ls --yes 2>/dev/null | grep "$VERCEL_PROJECT" | head -1 | awk '{print $2}' || echo "???")
    if [ "$DEPLOY_URL" != "???" ]; then
      echo "   URL: $DEPLOY_URL"
    fi
  else
    echo "   Status: ❌ Project not found in Vercel"
  fi
else
  echo "⚠️  Vercel CLI not installed"
fi

echo ""
echo "To deploy: quick research-hub-deploy"
