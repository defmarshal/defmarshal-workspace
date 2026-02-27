#!/usr/bin/env bash
# Ensure Clawdash is up-to-date and deployed
# 1. Regenerate data.json
# 2. Commit to dashboard repo (if changed)
# 3. Trigger Vercel production deploy

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
DASHBOARD_DIR="$WORKSPACE/apps/dashboard"

echo "🔄 Regenerating dashboard data..."
"$WORKSPACE/scripts/generate-dashboard-data.sh"

cd "$DASHBOARD_DIR"
echo "📦 Checking for changes in data.json..."
if git diff --quiet data.json; then
  echo "✅ data.json already up-to-date."
else
  echo "📝 Committing data.json..."
  git add data.json
  git commit -m "chore: update dashboard data [$(date -u +%Y-%m-%d)]"
fi

echo "🚀 Triggering Vercel production deploy..."
vercel --prod --yes

echo "✅ Clawdash deployment initiated."
echo "   Live URL: https://openclaw-dashboard-delta.vercel.app"
echo "   (or check vercel ls for latest alias)"
