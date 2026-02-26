#!/usr/bin/env bash
# Deploy Research Hub to Vercel (production).
# Requires Vercel CLI installed and logged in.

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE/apps/research-hub" || {
  echo "❌ research-hub app not found at $WORKSPACE/apps/research-hub"
  exit 1
}

# Ensure INDEX.md is up to date
"$WORKSPACE/scripts/research-index-update.sh"

echo "🚀 Deploying Research Hub to Vercel (production)..."
vercel --prod

echo "✅ Deployment complete. Live at: $(vercel ls | grep -Eo 'https://[^ ]+' | head -1)"
