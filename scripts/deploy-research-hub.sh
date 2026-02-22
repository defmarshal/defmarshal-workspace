#!/usr/bin/env bash
# Auto-deploy Research Hub to Vercel when new research is available
# Usage: ./deploy-research-hub.sh [--dry-run]

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
APP_DIR="$WORKSPACE/apps/research-hub"
DRY_RUN=0

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

echo "=== Research Hub Deploy ==="

# Check for Vercel CLI
if ! command -v vercel &>/dev/null; then
  echo "Vercel CLI not installed. Skipping deploy."
  exit 1
fi

# Prebuild: sync research + audio
echo "Running prebuild..."
bash "$APP_DIR/prebuild.sh"

# Build (optional check)
if [ $DRY_RUN -eq 1 ]; then
  echo "Dry run: would build and deploy now."
  exit 0
fi

# Deploy to production
echo "Deploying to Vercel production..."
cd "$APP_DIR"
vercel --prod --yes

echo "✅ Research Hub deployed!"
