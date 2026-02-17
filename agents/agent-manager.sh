#!/usr/bin/env bash
# Agent Manager — Proactive workspace maintenance daemon
# Spawns specialized agents for routine tasks; respects quiet hours; logs to memory/agent-manager.log

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOGFILE="memory/agent-manager.log"
mkdir -p memory

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"
}

log "Agent Manager starting (PID $$)"

# Lock to avoid duplicates
lockfile="agents/agent-manager/.lock"
mkdir -p "$(dirname "$lockfile")"
if [ -e "$lockfile" ]; then
  if kill -0 "$(cat "$lockfile" 2>/dev/null || echo 0)" 2>/dev/null; then
    log "Another instance running (PID $(cat "$lockfile" 2>/dev/null || echo unknown)). Exiting."
    exit 0
  else
    log "Stale lock detected; removing"
    rm -f "$lockfile"
  fi
fi
echo $$ > "$lockfile"

# Cleanup on exit
cleanup() {
  rm -f "$lockfile"
  log "Agent Manager stopped"
}
trap cleanup EXIT TERM INT

# Main loop
while true; do
  # Quiet hours check (Asia/Bangkok 23:00–08:00)
  HOUR=$(TZ=Asia/Bangkok date +%H)
  if (( HOUR >= 23 || HOUR < 8 )); then
    sleep 3600
    continue
  fi

  # 1. Git dirty: commit if stable and no pending changes after agent cycles
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

  # 3. Downloads cleanup threshold (if >2GB or >50 files)
  if [ -d "downloads" ]; then
    size=$(du -sm downloads 2>/dev/null | cut -f1 || echo 0)
    count=$(find downloads -type f 2>/dev/null | wc -l)
    if [ "$size" -gt 2000 ] || [ "$count" -gt 50 ]; then
      log "Downloads size ${size}MB or count ${count} exceeds threshold; cleaning"
      ./quick cleanup-downloads --days 30 --execute --verbose >> "$LOGFILE" 2>&1 || true
    fi
  fi

  # 4. Content freshness: if no content files for today, spawn content-agent
  today=$(date -u +%Y-%m-%d)
  if ! ls content/${today}*.md 1>/dev/null 2>&1; then
    log "No content for today; spawning content-agent"
    openclaw agent --agent main --message "You are the content-agent. Create anime summaries, tech writeups, or daily digests. Check for pending tasks. If none, generate a short daily digest." --thinking low --timeout 600000 >> "$LOGFILE" 2>&1 || true
  fi

  # 5. Research freshness: if no research files for today, spawn research-agent
  if ! ls research/${today}*.md 1>/dev/null 2>&1; then
    log "No research for today; spawning research-agent"
    openclaw agent --agent main --message "You are the research-agent. Conduct continuous research on anime, banking, tech, AI. Use web_search, web_fetch, memory tools. Create detailed reports in research/." --thinking low --timeout 600000 >> "$LOGFILE" 2>&1 || true
  fi

  # Sleep before next check
  sleep 1800  # 30 minutes
done
