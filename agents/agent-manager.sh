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

  # Quiet hours check (Asia/Bangkok 23:00–08:00)
  HOUR=$(TZ=Asia/Bangkok date +%H)
  if (( HOUR >= 23 || HOUR < 8 )); then
    log "Quiet hours; skipping checks"
    return 0
  fi

  # 1. Git dirty
  if ! git diff --quiet && ! git diff --cached --quiet; then
    if [ "$(git status --porcelain | wc -l)" -lt 10 ]; then
      log "Git dirty but seems minor; attempting commit"
      git add -A
      git commit -m "build: auto-commit from agent-manager ($(date -u +%Y-%m-%d))" || true
      git push origin master || true
    else
      log "Git dirty with many changes; skipping auto-commit"
    fi
  fi

  # 2. Memory index health
  if ./quick memory-reindex-check >/dev/null 2>&1; then
    log "Memory reindex needed; triggering"
    ./quick memory-index >> "$LOGFILE" 2>&1 || true
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
