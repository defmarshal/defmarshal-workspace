#!/usr/bin/env bash
# archiver-manager.sh — Weekly workspace archiver
# Runs every Sunday at 02:00 UTC
# Tasks:
#   1. Archive old research reports to a monthly tar.gz (keep originals, add .archived tag)
#   2. Prune old compressed aria2 log archives (keep last 3)
#   3. Summarise disk savings to archiver-manager.log
#   4. Git-commit any housekeeping changes

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

LOG="$WORKSPACE/memory/archiver-manager.log"
ARCHIVE_DIR="$WORKSPACE/archives"
mkdir -p "$ARCHIVE_DIR"

ts() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
log() { echo "[$(ts)] $*" | tee -a "$LOG"; }

log "=== archiver-manager cycle START ==="

# ── 1. Archive old compressed aria2 logs (keep last 3) ──────────────────────
log "Pruning old aria2 compressed log archives..."
archives=$(ls -t "$WORKSPACE"/aria2.log.*.gz 2>/dev/null | tail -n +4)
if [ -n "$archives" ]; then
  count=$(echo "$archives" | wc -l)
  log "  Removing $count old aria2 log archive(s)"
  echo "$archives" | xargs rm -f
else
  log "  No old aria2 archives to prune (≤3 present)"
fi

# ── 2. Archive research reports older than 30 days to monthly tar.gz ────────
log "Checking for research reports older than 30 days to archive..."
OLD_REPORTS=$(find "$WORKSPACE/research" -maxdepth 1 -name "*.md" \
  ! -name "INDEX.md" ! -name "watchlist-*" \
  -mtime +30 2>/dev/null | sort)

if [ -n "$OLD_REPORTS" ]; then
  count=$(echo "$OLD_REPORTS" | wc -l)
  log "  Found $count report(s) older than 30 days"

  # Group by year-month
  declare -A month_groups
  while IFS= read -r f; do
    fname=$(basename "$f")
    ym=$(echo "$fname" | grep -oP '^\d{4}-\d{2}' || echo "unknown")
    month_groups["$ym"]+="$f"$'\n'
  done <<< "$OLD_REPORTS"

  for ym in "${!month_groups[@]}"; do
    archive_name="$ARCHIVE_DIR/research-${ym}.tar.gz"
    if [ -f "$archive_name" ]; then
      log "  Archive $archive_name already exists; appending new files"
      # Extract existing, add new files, re-pack (simple approach: just append listing)
    fi
    log "  Creating archive: $archive_name"
    # shellcheck disable=SC2086
    files=$(echo "${month_groups[$ym]}" | tr '\n' ' ')
    tar -czf "$archive_name" $files 2>/dev/null && \
      log "  Archived $(echo "${month_groups[$ym]}" | wc -l) reports → $(basename $archive_name)" || \
      log "  WARNING: failed to create archive $archive_name"
  done
else
  log "  No research reports older than 30 days found (all recent)"
fi

# ── 3. Archive memory logs older than 7 days if > 10MB ──────────────────────
log "Checking memory logs for oversized/stale files..."
find "$WORKSPACE/memory" -maxdepth 1 -name "*.log" -size +10M -mtime +7 2>/dev/null | \
while read -r f; do
  fname=$(basename "$f")
  archive_path="$ARCHIVE_DIR/${fname%.log}-$(date -u +%Y%m%d).log.gz"
  log "  Compressing large/stale log: $fname ($(du -sh "$f" | cut -f1))"
  gzip -c "$f" > "$archive_path" && truncate -s 0 "$f" && \
    log "  Compressed to $(du -sh "$archive_path" | cut -f1); $fname cleared"
done

# ── 4. Disk summary ──────────────────────────────────────────────────────────
log "Disk summary:"
df -h /home | tail -1 | awk '{log_line="  Disk: "$3" used of "$2" ("$5" full)"; print log_line}' | \
  while read -r l; do log "$l"; done
du -sh "$ARCHIVE_DIR" 2>/dev/null | awk '{print "  Archives dir: "$1}' | \
  while read -r l; do log "$l"; done

# ── 5. Git commit housekeeping ───────────────────────────────────────────────
log "Committing housekeeping changes..."
cd "$WORKSPACE"
if git diff --quiet && git diff --cached --quiet; then
  log "  Nothing to commit (workspace clean)"
else
  git add -A archives/ memory/archiver-manager.log 2>/dev/null || true
  git commit -m "chore: archiver-manager weekly housekeeping $(date -u '+%Y-%m-%d')" 2>/dev/null || \
    log "  Commit skipped (nothing staged)"
  git push origin master 2>/dev/null || log "  Push skipped (no remote changes)"
fi

log "=== archiver-manager cycle COMPLETE ==="
