#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/git-janitor.log"
mkdir -p memory

# Configuration
STALE_BRANCH_DAYS=7    # Consider branches older than this many days as stale
DRY_RUN=0              # Set to 1 to log without deleting

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
fi

# ------------------------------------------------------------
# Cleanup stale idea branches (safe: only merged and old)
# ------------------------------------------------------------
cleanup_idea_branches() {
  set +e  # disable errexit for this function; we handle errors manually
  local current_branch
  current_branch=$(git rev-parse --abbrev-ref HEAD)
  local cutoff_seconds=$((STALE_BRANCH_DAYS * 86400))
  local now_seconds=$(date +%s)
  local cleaned=0
  local skipped_recent=0
  local skipped_unmerged=0
  local none_found=1

  # Get list of local branches matching 'idea/*' excluding current
  while IFS= read -r branch; do
    branch_name="${branch//[[:space:]]/}"  # trim whitespace
    [[ -z "$branch_name" ]] && continue
    [[ "$branch_name" == "$current_branch" ]] && continue
    none_found=0

    # Check if branch is fully merged into current branch (safe to delete)
    if git merge-base --is-ancestor "refs/heads/$branch_name" HEAD 2>/dev/null; then
      # Branch is merged; now check age via last commit on that branch
      branch_commit=$(git rev-parse "refs/heads/$branch_name" 2>/dev/null) || continue
      commit_time=$(git show -s --format=%ct "$branch_commit" 2>/dev/null) || continue
      age_seconds=$((now_seconds - commit_time))

      if (( age_seconds > cutoff_seconds )); then
        if (( DRY_RUN )); then
          log "DRY-RUN: Would delete stale merged branch: $branch_name (age: $((age_seconds/86400)) days)"
        else
          git branch -D "$branch_name" 2>/dev/null && {
            log "Deleted stale merged branch: $branch_name (age: $((age_seconds/86400)) days)"
            cleaned=$((cleaned + 1))
          } || log "Failed to delete branch: $branch_name (may be protected)"
        fi
      else
        skipped_recent=$((skipped_recent + 1))
      fi
    else
      skipped_unmerged=$((skipped_unmerged + 1))
    fi
  done < <(git branch --list 'idea/*' | sed 's/^* //')

  if (( none_found )); then
    log "No idea branches found for cleanup."
  else
    log "Idea branch cleanup: deleted=$cleaned, skipped_recent=$skipped_recent, skipped_unmerged=$skipped_unmerged"
  fi
  set -e  # re-enable errexit
}

cleanup_idea_branches

log "Git janitor completed"
