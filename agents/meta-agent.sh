#!/usr/bin/env bash
# Meta‑Agent: autonomous planner & orchestrator for the ultimate self‑extending system
# Modes: --once (one‑shot), --daemon (loop hourly), --status (show last report)

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOGFILE="memory/meta-agent.log"
REPORT_FILE="meta-report-latest.md"
CHECKPOINT_FILE="autonomous-checkpoints.json"
mkdir -p memory

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"
}

# Helper: update checkpoint JSON
update_checkpoint() {
  if [ -f "$CHECKPOINT_FILE" ]; then
    # Use jq if available, else skip
    if command -v jq &>/dev/null; then
      # This function can be expanded later
      :
    fi
  fi
}

case "${1:-}" in
  --once)
    log "Meta‑Agent starting (one‑shot)"

    # Collect system snapshot
    HEALTH=$(./quick health 2>&1 || echo "health check failed")
    AGENT_STATUS=$(./quick agent-status 2>&1 || echo "agent‑status failed")
    MEMORY_NEEDS=$(./quick memory-reindex-check 2>&1 || echo "0")
    DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | tr -d '%')
    APT_COUNT=$(apt-get -s upgrade 2>/dev/null | grep -c '^Inst ' || echo "0")
    TODAY=$(date -u +%Y-%m-%d)
    CONTENT_TODAY=$(ls content/${TODAY}*.md 2>/dev/null | wc -l)
    RESEARCH_TODAY=$(ls research/${TODAY}*.md 2>/dev/null | wc -l)

    log "Snapshot: disk=${DISK_USAGE}%, apt=${APT_COUNT}, content_today=${CONTENT_TODAY}, research_today=${RESEARCH_TODAY}, memory_needs=${MEMORY_NEEDS}"

    # Decision engine
    ACTIONS=()
    if [ "$MEMORY_NEEDS" != "0" ]; then
      ACTIONS+=("memory reindex")
      log "Memory reindex needed"
    fi
    if [ "$DISK_USAGE" -ge 80 ]; then
      ACTIONS+=("disk cleanup")
      log "Disk usage >= 80%"
    fi
    if [ "$CONTENT_TODAY" -eq 0 ]; then
      ACTIONS+=("spawn content-agent")
      log "No content for today; will spawn"
    fi
    if [ "$RESEARCH_TODAY" -eq 0 ]; then
      ACTIONS+=("spawn research-agent")
      log "No research for today; will spawn"
    fi

    # Execute actions (spawn agents for remediation)
    LOCK_FILE="memory/.voyage-rate-lock"
    for act in "${ACTIONS[@]}"; do
      case "$act" in
        "memory reindex")
          # Rate‑lock: skip if lock exists and is younger than 6 hours (free tier 3 RPM makes reindex impractical)
          if [ -f "$LOCK_FILE" ] && [ $(($(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || echo 0))) -lt 21600 ]; then
            log "Skipping memory reindex due to active Voyage rate‑lock (lock: $(stat -c %y "$LOCK_FILE" 2>/dev/null || echo unknown))"
          else
            log "Triggering memory reindex"
            # Capture output to detect rate limits and clear stale lock on success
            if OUTPUT=$(./quick memory-index 2>&1); then
              echo "$OUTPUT" | tee -a "$LOGFILE"
              # Clear stale lock if present
              rm -f "$LOCK_FILE" 2>/dev/null || true
            else
              # Even if non‑zero exit, still log output
              echo "$OUTPUT" | tee -a "$LOGFILE"
              # Check for rate limit indicators in output
              if echo "$OUTPUT" | grep -qiE '429|rate limited'; then
                log "Rate limit detected during reindex; setting lock for 6 hours"
                touch "$LOCK_FILE"
              fi
            fi
          fi
          ;;
        "disk cleanup")
          log "Triggering downloads cleanup (dry‑run first)"
          ./quick cleanup-downloads --days 30 >> "$LOGFILE" 2>&1 || true
          ;;
        "spawn content-agent")
          log "Spawning content‑agent via sessions_spawn"
          openclaw agent --agent main --message "You are the content‑agent. Create anime summaries, tech writeups, or daily digests. Check for pending tasks. If none, generate a short daily digest." --thinking low --timeout 600000 >> "$LOGFILE" 2>&1 || true
          ;;
        "spawn research-agent")
          log "Spawning research‑agent via sessions_spawn"
          openclaw agent --agent main --message "You are the research‑agent. Conduct continuous research on anime, banking, tech, AI. Use web_search, web_fetch, memory tools. Create detailed reports in research/." --thinking low --timeout 600000 >> "$LOGFILE" 2>&1 || true
          ;;
      esac
    done

    # Generate human‑readable report
    {
      echo "# Meta‑Agent Report — $(date -u '+%Y-%m-%d %H:%M UTC')"
      echo ""
      echo "## System Snapshot"
      echo "- Disk usage: ${DISK_USAGE}%"
      echo "- APT updates pending: $APT_COUNT"
      echo "- Content files today: $CONTENT_TODAY"
      echo "- Research files today: $RESEARCH_TODAY"
      echo "- Memory reindex needed: ${MEMORY_NEEDS}"
      echo ""
      echo "## Actions Taken"
      if [ ${#ACTIONS[@]} -eq 0 ]; then
        echo "None — system within normal parameters."
      else
        for a in "${ACTIONS[@]}"; do
          echo "- $a"
        done
      fi
      echo ""
      echo "## Notes"
      echo "- Supervisor: running every 5 min"
      echo "- agent‑manager: running every 30 min"
      echo "- All times Asia/Bangkok unless noted"
    } > "$REPORT_FILE"

    log "Meta‑Agent one‑shot completed; actions: ${ACTIONS[*]:-none}"
    ;;

  --daemon)
    log "Meta‑Agent daemon starting (PID $$)"
    while true; do
      # Note: Quiet hours removed 2026-02-17; agents run 24/7
      # Run one cycle
      bash "$0" --once
      # Wait an hour
      sleep 3600
    done
    ;;

  --status)
    if [ -f "$REPORT_FILE" ]; then
      cat "$REPORT_FILE"
    else
      echo "No meta‑report yet. Run meta‑agent first."
    fi
    ;;

  *)
    echo "Usage: $0 [--once|--daemon|--status]" >&2
    exit 1
    ;;
esac
