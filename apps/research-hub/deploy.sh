#!/usr/bin/env bash
# Deploy Research Hub to Vercel
# Usage: From workspace root, run: ./apps/research-hub/deploy.sh

set -euo pipefail

cd "$(dirname "$0")"

echo "=== Research Hub Vercel Deployment ==="
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &>/dev/null; then
  echo "Vercel CLI not found. Install with: npm i -g vercel"
  exit 1
fi

# Ensure we have a .env file with GitHub token if needed
if [ ! -f .env ]; then
  echo "Creating .env (optional) for GITHUB_TOKEN if pushing private repo..."
  touch .env
fi

# Step 1: Create GitHub repo (if not exists)
# You need to be logged in via gh CLI or have GITHUB_TOKEN set
echo "Step 1: Create GitHub repo 'research-hub'"
echo "If repo already exists, skip this step."
echo "To create manually:"
echo "  gh repo create research-hub --public --source=. --remote=origin"
echo ""

# Step 2: Link to Vercel
echo "Step 2: Link to Vercel project"
if [ ! -f .vercel/project.json ]; then
  vercel link --yes --project research-hub
else
  echo "Already linked."
fi

# Step 3: Deploy to production
echo "Step 3: Deploy to production (will build and deploy)"
echo "Make sure your research files are up to date in ../../research"
vercel --prod --yes

echo "Done! (◕‿◕)"
