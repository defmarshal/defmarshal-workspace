#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOGFILE="memory/agent-manager.log"
mkdir -p memory

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"
}

lockfile="agents/agent-manager/.lock"
mkdir -p "$(dirname "$lockfile")"

check_lock() {
  if [ -e "$lockfile" ]; then
    if kill -0 "$(cat "$lockfile" 2>/dev/null || echo 0)" 2>/dev/null; then
      log "Another instance running (PID $(cat "$lockfile" 2>/dev/null || echo unknown)). Exiting."
      return 1
    else
      log "Stale lock detected; removing"
      rm -f "$lockfile"
    fi
  fi
  echo $$ > "$lockfile"
}

cleanup() {
  rm -f "$lockfile"
  log "Agent Manager stopped"
}
trap cleanup EXIT TERM INT

run_checks() {
  log "Running maintenance checks"

  # 1. Git dirty (including untracked)
  changes=$(git status --porcelain | wc -l)
  if [ "$changes" -gt 0 ]; then
    if [ "$changes" -lt 10 ]; then
      log "Git dirty ($changes files) but seems minor; attempting commit"
      git add -A
      git commit -m "build: auto-commit from agent-manager ($(date -u +%Y-%m-%d))" || true
      git push origin master || true
    else
      log "Git dirty with many changes ($changes files); skipping auto-commit"
    fi
  fi

  # 2. Memory index health
  # memory-reindex-check exits 0 when OK (no reindex needed), 1 when recommended, 2 on error
  # Trigger reindex only when exit code is non-zero (needed or error)
  # Check if Voyage rate lock is active (6-hour backoff)
  SKIP_DUE_TO_LOCK=0
  if [ -f "memory/.voyage-rate-lock" ]; then
    LOCK_AGE_HOURS=$(( ( $(date +%s) - $(stat -c %Y "memory/.voyage-rate-lock") ) / 3600 ))
    if [ $LOCK_AGE_HOURS -lt 6 ]; then
      log "Voyage rate-lock active (${LOCK_AGE_HOURS}h old); skipping memory reindex"
      SKIP_DUE_TO_LOCK=1
    else
      rm -f "memory/.voyage-rate-lock"
    fi
  fi

  if [ $SKIP_DUE_TO_LOCK -eq 0 ]; then
    if ! ./quick memory-reindex-check >/dev/null 2>&1; then
      log "Memory reindex needed; triggering"
      TMP_REINDEX_LOG=$(mktemp)
      if ! ./quick memory-index 2>&1 | tee -a "$LOGFILE" | tee "$TMP_REINDEX_LOG"; then
        if grep -qiE '429|rate limited' "$TMP_REINDEX_LOG"; then
          touch memory/.voyage-rate-lock
          log "Voyage rate limit detected; rate lock set"
        fi
      fi
      rm -f "$TMP_REINDEX_LOG"
    fi
  fi

  # 3. Downloads cleanup
  if [ -d "downloads" ]; then
    size=$(du -sm downloads 2>/dev/null | cut -f1 || echo 0)
    count=$(find downloads -type f 2>/dev/null | wc -l)
    if [ "$size" -gt 2000 ] || [ "$count" -gt 50 ]; then
      log "Downloads size ${size}MB or count ${count} exceeds threshold; cleaning"
      ./quick cleanup-downloads --days 30 --execute --verbose >> "$LOGFILE" 2>&1 || true
    fi
  fi

  # 4. Content freshness
  today=$(date -u +%Y-%m-%d)
  if ! ls content/${today}*.md 1>/dev/null 2>&1; then
    log "No content for today; spawning content-agent"
    openclaw agent --agent main --message "You are the content-agent. Create anime summaries, tech writeups, or daily digests. Check for pending tasks. If none, generate a short daily digest." --thinking low --timeout 600000 >> "$LOGFILE" 2>&1 || true
  fi

  # 5. Research freshness
  if ! ls research/${today}*.md 1>/dev/null 2>&1; then
    log "No research for today; spawning research-agent"
    openclaw agent --agent main --message "You are the research-agent. Conduct continuous research on anime, banking, tech, AI. Use web_search, web_fetch, memory tools. Create detailed reports in research/." --thinking low --timeout 600000 >> "$LOGFILE" 2>&1 || true
  fi

  # 6. Cron schedule validation (enforce CRON_JOBS.md)
  log "Validating cron schedules against CRON_JOBS.md"
  ./scripts/validate-cron-schedules.sh >> "$LOGFILE" 2>&1 || true

  log "Checks completed"
}

case "${1:-}" in
  --once)
    check_lock || exit 0
    run_checks
    cleanup
    ;;
  --daemon|"")
    check_lock || exit 0
    log "Agent Manager starting daemon (PID $$)"
    while true; do
      run_checks
      sleep 1800
    done
    ;;
  *)
    echo "Usage: $0 [--once|--daemon]" >&2
    exit 1
    ;;
esac
