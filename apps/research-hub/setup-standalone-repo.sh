#!/usr/bin/env bash
# Extract Research Hub into its own repository and push to GitHub
# Run this from the workspace root: ./apps/research-hub/setup-standalone-repo.sh

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
APP_DIR="$WORKSPACE/apps/research-hub"
NEW_REPO_DIR="/tmp/research-hub-standalone"

echo "=== Research Hub Standalone Repo Setup ==="
echo ""

# Check prerequisites
if ! command -v gh &>/dev/null; then
  echo "GitHub CLI (gh) not found. Please install it first:"
  echo "  sudo apt update && sudo apt install gh"
  exit 1
fi

if ! gh auth status &>/dev/null; then
  echo "Please authenticate GitHub CLI first:"
  echo "  gh auth login"
  exit 1
fi

# Step 1: Copy files to temp directory
echo "Step 1: Copying Research Hub to temporary directory..."
rm -rf "$NEW_REPO_DIR"
mkdir -p "$NEW_REPO_DIR"
cp -r "$APP_DIR"/* "$NEW_REPO_DIR/"
cp "$APP_DIR/../.."/research "$NEW_REPO_DIR/public/" 2>/dev/null || echo "Warning: research folder not copied (will need to copy manually or use symlink)"
echo "Files copied."

# Step 2: Initialize new git repo
echo "Step 2: Initializing standalone git repository..."
cd "$NEW_REPO_DIR"
git init
git add -A
git commit -m "Initial commit: Research Hub"

# Step 3: Create GitHub repo and push
echo "Step 3: Creating GitHub repo 'research-hub'..."
if gh repo view defmarshal/research-hub &>/dev/null; then
  echo "Repo already exists on GitHub. Adding remote..."
else
  gh repo create research-hub --public --source=. --remote=origin
fi

git branch -M main
git push -u origin main

# Step 4: Optional: Link to Vercel
echo ""
echo "Step 4: Vercel setup"
echo "Now you can deploy to Vercel:"
echo "  cd $NEW_REPO_DIR"
echo "  vercel link --project research-hub"
echo "  vercel --prod"
echo ""
echo "Or visit https://vercel.com/new and import the 'research-hub' repo."
echo ""
echo "✅ Research Hub is now a standalone repo at: https://github.com/defmarshal/research-hub"
echo "📁 Temporary location: $NEW_REPO_DIR (you can delete after verification)"
