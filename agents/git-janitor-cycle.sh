#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/git-janitor.log"
mkdir -p memory

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"
}

log "Git janitor starting"
# Stage safe untracked files (excluding node_modules, .git, etc.)
git add -A 2>/dev/null || true
# Auto-commit if there are changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
  git commit -m "auto: maintenance update $(date -u '+%Y-%m-%d %H:%M UTC')" 2>/dev/null || true
  # Push to remote if commit succeeded (ignore errors to avoid breaking cycle)
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    git push origin master 2>/dev/null || true
  fi
fi
log "Git janitor completed"
