#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/git-janitor.log"
mkdir -p memory

log() {
  echo "$(date -u +'%Y-%m-%d %H:%M:%S UTC') - $*" >> "$LOGFILE"
}

log "Git janitor starting"
# Configure git if not already configured
if ! git config user.email >/dev/null 2>&1; then
  git config user.email "openclaw-bot@example.com"
  git config user.name "OpenClaw Bot"
fi
# Stage safe untracked files (excluding node_modules, .git, etc.)
git add -A 2>/dev/null || true
# Auto-commit if there are changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
  git commit -m "auto: maintenance update $(date -u '+%Y-%m-%d %H:%M UTC')" 2>/dev/null || true
fi
log "Git janitor completed"
