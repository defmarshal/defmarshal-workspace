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

# Absolute workspace path for lock file consistency
WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOCK_FILE="$WORKSPACE/memory/.voyage-rate-lock"

case "${1:-}" in
  --once)
    log "Meta‑Agent starting (one‑shot)"

    # Collect system snapshot
    HEALTH=$(./quick health 2>&1 || echo "health check failed")
    AGENT_STATUS=$(./quick agent-status 2>&1 || echo "agent‑status failed")
    # Run memory reindex check; capture output for logging and exit code for decision
    set +e
    MEMORY_NEEDS=$(./quick memory-reindex-check 2>&1)
    MEMORY_NEEDS_EXIT=$?
    set -e
    DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | tr -d '%')
    APT_COUNT=$(apt-get -s upgrade 2>/dev/null | grep -c '^Inst ' || echo "0")
    TODAY=$(date -u +%Y-%m-%d)
    CONTENT_TODAY=$(ls content/${TODAY}*.md 2>/dev/null | wc -l)
    RESEARCH_TODAY=$(ls research/${TODAY}*.md 2>/dev/null | wc -l)

    log "Snapshot: disk=${DISK_USAGE}%, apt=${APT_COUNT}, content_today=${CONTENT_TODAY}, research_today=${RESEARCH_TODAY}, memory_needs=${MEMORY_NEEDS}"

    # Decision engine
    ACTIONS=()
    # Memory reindex disabled to avoid Voyage AI rate limits (user request)
    # Uncomment below to re-enable when a provider is configured
    # if [ "$MEMORY_NEEDS_EXIT" -ne 0 ]; then
    #   ACTIONS+=("memory reindex")
    #   log "Memory reindex needed (exit code: $MEMORY_NEEDS_EXIT)"
    # fi
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

    # Create permanent archive-agent if missing and old content exists + disk >60%
    if ! openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^archive-agent-cron$'; then
      if find content -type f -name '*.md' -mtime +90 2>/dev/null | read -r; then
        if [ "$DISK_USAGE" -gt 60 ]; then
          ACTIONS+=("create archive-agent")
          log "No archive-agent cron found, old content exists, disk usage ${DISK_USAGE}% >60% — will create permanent archive agent"
        fi
      fi
    fi

    # Dev Agent: Proactive development when system is stable and dev activity stale
    # Conditions:
    # - No dev commit in the last 12 hours
    # - Content and research are both active today (system producing)
    # - Disk usage < 75% (enough headroom for dev work)
    LAST_DEV_COMMIT=$(git log --since='12 hours ago' --oneline 2>/dev/null | grep '^dev:' | wc -l)
    if [ "$LAST_DEV_COMMIT" -eq 0 ] && [ "$CONTENT_TODAY" -gt 0 ] && [ "$RESEARCH_TODAY" -gt 0 ] && [ "$DISK_USAGE" -lt 75 ]; then
      ACTIONS+=("spawn dev-agent")
      log "No dev activity in 12h; content and research active; spawning dev-agent"
    fi

    # Creative Innovation: Periodically spawn dev-agent to build something entirely new
    # Conditions:
    # - System is healthy (disk <70%, memory clean, gateway up)
    # - Has not spawned creative dev in the last 48h (avoid flooding)
    # - Weekends (Saturday/Sunday Asia/Bangkok) to encourage exploratory work
    INNOVATION_TRIGGER_FILE="$WORKSPACE/memory/.last-innovation"
    if [ "$DISK_USAGE" -lt 70 ] && [ "$APT_COUNT" -lt 10 ] && grep -q "Memory:.*clean" <<<"$HEALTH" 2>/dev/null; then
      WEEKDAY=$(TZ='Asia/Bangkok' date +%u)  # 1=Mon, 6=Sat, 7=Sun
      if [ "$WEEKDAY" -ge 6 ]; then
        NEED_INNOVATION=0
        if [ ! -f "$INNOVATION_TRIGGER_FILE" ]; then
          NEED_INNOVATION=1
        else
          AGE_HOURS=$(( ( $(date +%s) - $(stat -c %Y "$INNOVATION_TRIGGER_FILE") ) / 3600 ))
          if [ "$AGE_HOURS" -ge 48 ]; then
            NEED_INNOVATION=1
          fi
        fi
        if [ "$NEED_INNOVATION" -eq 1 ]; then
          ACTIONS+=("spawn dev-agent:innovate")
          log "Weekend detected, system healthy, and no recent innovation — spawning dev-agent with creative mandate"
          touch "$INNOVATION_TRIGGER_FILE"
        fi
      fi
    fi

    # Execute actions (spawn agents for remediation)
    # Use workspace-defined LOCK_FILE with absolute path (already set above)
    for act in "${ACTIONS[@]}"; do
      case "$act" in
        "memory reindex")
          # Disabled to avoid Voyage AI usage
          # To re-enable: remove this block and uncomment action decision above
          log "Memory reindex disabled (Voyage AI not in use); skipping"
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
        "spawn dev-agent")
          log "Spawning dev‑agent via sessions_spawn"
          openclaw agent --agent main --message "You are the dev-agent. Continuous development of tools, automations, and infrastructure. Scan the workspace for improvements. Implement small utilities, fix deprecations, test, commit with 'dev:' prefix, push to GitHub. Log actions to dev-agent.log. (Quiet hours removed; agents run 24/7.) After completing, output a brief summary." --thinking low --timeout 600000 >> "$LOGFILE" 2>&1 || true
          ;;
        "spawn dev-agent:innovate")
          log "Spawning dev‑agent with creative innovation mandate"
          openclaw agent --agent main --message "You are the dev-agent on an innovation sprint! Your mission: conceive and build something entirely new that does not exist in this workspace yet. Think outside the box — could be a new utility, integration, automation, skill, dashboard, notification system, or tool that would significantly improve the system's capabilities. Research current gaps, design a novel solution, implement it, test it, and commit with prefix 'dev:innovation'. Be creative and bold! Log your progress to dev-agent.log. After completing, output a brief summary of what you built." --thinking medium --timeout 720000 >> "$LOGFILE" 2>&1 || true
          ;;
        "create archive-agent")
          log "Creating permanent archive-agent (compresses old content/research)"
          SCRIPT_PATH="$WORKSPACE/agents/archive-cycle.sh"
          cat > "$SCRIPT_PATH" <<'EOF'
#!/usr/bin/env bash
# Archive-Agent: compress and archive old content/research to save disk space
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/archive-agent.log"
mkdir -p memory archives
log() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"; }

log "Archive‑agent starting"

# Archive content older than 90 days
ARCHIVE_MONTH=$(date -u +%Y-%m)
ARCHIVE_DIR="archives/${ARCHIVE_MONTH}"
mkdir -p "$ARCHIVE_DIR"

# Find and compress old content files
shopt -s nullglob
for f in content/*.md; do
  if [ "$(stat -c %Y "$f")" -lt $(( $(date +%s) - 90*86400 )) ]; then
    base=$(basename "$f" .md)
    tar -czf "$ARCHIVE_DIR/${base}.tar.gz" -C content "$base.md" && rm -f "$f"
    log "Archived content: $base.md → $ARCHIVE_DIR/${base}.tar.gz"
  fi
done

# Find and compress old research files
for f in research/*.md; do
  if [ "$(stat -c %Y "$f")" -lt $(( $(date +%s) - 90*86400 )) ]; then
    base=$(basename "$f" .md)
    tar -czf "$ARCHIVE_DIR/${base}.tar.gz" -C research "$base.md" && rm -f "$f"
    log "Archived research: $base.md → $ARCHIVE_DIR/${base}.tar.gz"
  fi
done

# Optional: remove empty directories
find content research -type d -empty -delete 2>/dev/null || true

log "Archive‑agent completed"
EOF
          chmod +x "$SCRIPT_PATH"
          # Register cron: run at 02:00 on the 1st of every month (UTC)
          openclaw cron add --name "archive-agent-cron" --expr "0 2 1 * *" --tz "UTC" \
            --payload '{"kind":"systemEvent","text":"Execute archive cycle: bash -c \'cd /home/ubuntu/.openclaw/workspace && ./agents/archive-cycle.sh >> memory/archive-agent.log 2>&1\'"}' \
            --sessionTarget isolated --delivery '{"mode":"none"}' >> "$LOGFILE" 2>&1 || true
          log "Archive‑agent cron job registered"
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
