#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/git-janitor.log"
mkdir -p memory

log() {
  echo "$(date -u +%Y-%m-%d\ %H:%M:%S) UTC - $*" >> "$LOGFILE"
}

log "Git janitor starting"

# Define safe patterns for auto-commit (production artifacts)
SAFE_PATTERNS=(
  "memory/*.json"
  "memory/*.md"
  "reports/*.md"
  "agents/ideas/*.json"
  "projects.md"
  "active-tasks.md"
  "CRON_JOBS.md"
)

# Stage only safe untracked files
for pattern in "${SAFE_PATTERNS[@]}"; do
  git add $pattern 2>/dev/null || true
done

# Auto-commit if there are changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
  git commit -m "auto: maintenance update $(date -u '+%Y-%m-%d %H:%M UTC')" 2>/dev/null || true
  # Push if commit succeeded and we have a remote
  git push origin HEAD 2>/dev/null || true
  # Cleanup stale idea branches (feature branches for executed ideas)
  # These are short-lived and should be deleted after validation
  git branch -D idea/* 2>/dev/null || true
fi

log "Git janitor completed"
