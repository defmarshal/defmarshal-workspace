#!/usr/bin/env bash
# Deploy Research Hub to Vercel
set -euo pipefail

cd /home/ubuntu/.openclaw/workspace/apps/research-hub

echo "=== Research Hub Deploy ==="

# Check if vercel is installed
if ! command -v vercel &>/dev/null; then
  echo "Vercel CLI not found. Install with: npm i -g vercel"
  exit 1
fi

# Check authentication
if ! vercel whoami &>/dev/null; then
  echo "Vercel not authenticated. Please run: vercel login"
  exit 1
fi

# Link project (if not already linked)
if ! vercel project ls | grep -q "research-hub"; then
  echo "Linking project to Vercel..."
  vercel link --project research-hub --confirm
else
  echo "Project already linked."
fi

# Run prebuild to ensure research data is up-to-date
echo "Running prebuild to copy research files..."
bash prebuild.sh

# Deploy to production
echo "Deploying to production..."
vercel --prod

echo "✅ Research Hub deployed!"
