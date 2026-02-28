#!/usr/bin/env bash
# Vercel Deployment Helper — link, configure, and deploy a project to Vercel
# Usage: quick vercel [subcommand]
# Subcommands: init, deploy, logs, link, unlink

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"

show_help() {
  cat <<EOF
Vercel deployment utility

Commands:
  init             Initialize Vercel project in current repo (interactive)
  deploy           Trigger a deployment (git push if needed)
  link             Link local repo to existing Vercel project
  unlink           Remove Vercel project association
  logs             Show recent deployment logs (via vercel --prod --yes)
  status           Show current Vercel project association

Examples:
  quick vercel init      # first-time setup
  quick vercel deploy    # deploy latest
  quick vercel link      # connect to an existing Vercel project
EOF
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  init)
    echo "Initializing Vercel project..."
    echo "NOTE: This requires Vercel CLI to be installed and you to be logged in."
    echo "1. Install: npm i -g vercel"
    echo "2. Login: vercel login"
    echo "Then run 'quick vercel link' after creating project on Vercel dashboard."
    ;;
  link)
    PROJECT_NAME="${1:-$(basename "$WORKSPACE")}"
    echo "Linking to Vercel project: $PROJECT_NAME"
    vercel link --yes --project "$PROJECT_NAME" || true
    ;;
  unlink)
    rm -f .vercel/project.json || true
    echo "Unlinked from Vercel project."
    ;;
  deploy)
    if [ ! -f .vercel/project.json ]; then
      echo "Not linked to a Vercel project. Run 'quick vercel link' first."
      exit 1
    fi
    echo "Deploying to Vercel..."
    vercel --prod --yes
    ;;
  logs)
    if [ ! -f .vercel/project.json ]; then
      echo "Not linked to a Vercel project."
      exit 1
    fi
    vercel logs --production --yes | tail -50
    ;;
  status)
    if [ -f .vercel/project.json ]; then
      cat .vercel/project.json
    else
      echo "No Vercel project linked."
    fi
    ;;
  *)
    show_help
    ;;
esac
