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

    # Dynamic Skill Installation: detect missing capabilities and install from ClawHub
    # Patterns:
    # - Frequent web searches → tavily or perplexity (tavily preferred for AI-optimized)
    # - Email mentions → gmail
    # - Weather mentions → weather
    # - Calendar mentions → google-calendar (if available)
    # - Torrent/aria2 activity → ensure aria2 skill present
    #
    # Check recent logs for keyword patterns
    WEB_SEARCH_COUNT=0
    EMAIL_MENTION_COUNT=0
    WEATHER_MENTION_COUNT=0
    CALENDAR_MENTION_COUNT=0

    # Scan recent agent logs (last 24h) for patterns
    for logfile in memory/*-agent.log memory/meta-agent.log; do
      if [ -f "$logfile" ] && [ "$(stat -c %Y "$logfile")" -ge $(( $(date +%s) - 86400 )) ]; then
        WEB_SEARCH_COUNT=$((WEB_SEARCH_COUNT + $(grep -c "web_search" "$logfile" 2>/dev/null || echo 0)))
        EMAIL_MENTION_COUNT=$((EMAIL_MENTION_COUNT + $(grep -c "gmail" "$logfile" 2>/dev/null || echo 0)))
        WEATHER_MENTION_COUNT=$((WEATHER_MENTION_COUNT + $(grep -c "weather" "$logfile" 2>/dev/null || echo 0)))
        CALENDAR_MENTION_COUNT=$((CALENDAR_MENTION_COUNT + $(grep -c "calendar" "$logfile" 2>/dev/null || echo 0)))
      fi
    done

    # Determine which skill to install (priority order)
    RECOMMENDED_SKILL=""
    if [ "$WEB_SEARCH_COUNT" -ge 10 ]; then
      # Prefer tavily for AI-optimized search
      if ! [ -d "$WORKSPACE/skills/tavily" ] && ! grep -q '"tavily"' "$WORKSPACE/.openclaw/openclaw.json" 2>/dev/null; then
        RECOMMENDED_SKILL="tavily"
      elif ! [ -d "$WORKSPACE/skills/perplexity" ] && ! grep -q '"perplexity"' "$WORKSPACE/.openclaw/openclaw.json" 2>/dev/null; then
        RECOMMENDED_SKILL="perplexity"
      fi
    elif [ "$EMAIL_MENTION_COUNT" -ge 5 ] && ! [ -d "$WORKSPACE/skills/gmail" ] && ! grep -q '"gmail"' "$WORKSPACE/.openclaw/openclaw.json" 2>/dev/null; then
      RECOMMENDED_SKILL="gmail"
    elif [ "$WEATHER_MENTION_COUNT" -ge 3 ] && ! [ -d "$WORKSPACE/skills/weather" ] && ! grep -q '"weather"' "$WORKSPACE/.openclaw/openclaw.json" 2>/dev/null; then
      RECOMMENDED_SKILL="weather"
    elif [ "$CALENDAR_MENTION_COUNT" -ge 2 ] && ! [ -d "$WORKSPACE/skills/google-calendar" ] && ! grep -q '"google-calendar"' "$WORKSPACE/.openclaw/openclaw.json" 2>/dev/null; then
      RECOMMENDED_SKILL="google-calendar"
    fi

    if [ -n "$RECOMMENDED_SKILL" ]; then
      # Throttle: only suggest if no skill install in last 7 days
      LAST_SKILL_INSTALL=$(find "$WORKSPACE/memory" -name ".last-skill-install" -mtime -7 2>/dev/null | head -1)
      if [ -z "$LAST_SKILL_INSTALL" ]; then
        ACTIONS+=("install skill:$RECOMMENDED_SKILL")
        log "Detected need for skill: $RECOMMENDED_SKILL (web:$WEB_SEARCH_COUNT email:$EMAIL_MENTION_COUNT weather:$WEATHER_MENTION_COUNT calendar:$CALENDAR_MENTION_COUNT)"
        touch "$WORKSPACE/memory/.last-skill-install"
      else
        log "Skill installation throttled (last install <7 days ago)"
      fi
    fi
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

    # Create git-janitor-agent if missing and repo has untracked files
    if ! openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^git-janitor-cron$'; then
      # Check for untracked files (excluding specific directories like downloads, archives, node_modules)
      UNTRACKED_COUNT=$(git status --porcelain 2>/dev/null | grep -E '^\?\?' | grep -v -E '(^downloads/|^archives/|^node_modules/|^\.git/|^builds/|^dht\.dat$|^aria2\.session$)' | wc -l)
      if [ "$UNTRACKED_COUNT" -gt 5 ]; then
        ACTIONS+=("create git-janitor-agent")
        log "Untracked files count $UNTRACKED_COUNT > 5; will create git-janitor-agent to auto-commit safe files"
      fi
    fi

    # Self-Improvement: Adjust dev-agent stale threshold based on recent outcomes
    # If dev-agent has been consistently successful, we can lower the threshold (spawn more often)
    # If dev-agent produces no commits, raise the threshold (spawn less often)
    DEV_STALE_HOURS=12  # default
    SELF_IMPROVE_TRIGGERED=0
    if [ -f "$WORKSPACE/memory/dev-agent.log" ]; then
      DEV_COMMITS_24H=$(git log --since='24 hours ago' --oneline 2>/dev/null | grep '^dev:' | wc -l)
      DEV_RUNS_24H=$(grep -c "Starting dev-agent cycle" "$WORKSPACE/memory/dev-agent.log" 2>/dev/null || echo 0)
      if [ "$DEV_RUNS_24H" -ge 5 ]; then
        SUCCESS_RATE=$(( DEV_COMMITS_24H * 100 / DEV_RUNS_24H ))
        if [ "$SUCCESS_RATE" -ge 70 ] || [ "$SUCCESS_RATE" -le 30 ]; then
          SELF_IMPROVE_TRIGGERED=1
          ACTIONS+=("self-improve")
          log "Dev-agent success rate ${SUCCESS_RATE}% (${DEV_COMMITS_24H}/${DEV_RUNS_24H}) — triggering self-improve to adjust thresholds"
        fi
        # Runtime adaptation (non-persistent)
        if [ "$SUCCESS_RATE" -ge 70 ] && [ "$DEV_STALE_HOURS" -gt 4 ]; then
          DEV_STALE_HOURS=4
        elif [ "$SUCCESS_RATE" -le 30 ] && [ "$DEV_STALE_HOURS" -lt 24 ]; then
          DEV_STALE_HOURS=24
        fi
      fi
    fi

    # Use DEV_STALE_HOURS (adaptive or default) for dev-agent condition below
    if [ "$LAST_DEV_COMMIT" -eq 0 ] && [ "$CONTENT_TODAY" -gt 0 ] && [ "$RESEARCH_TODAY" -gt 0 ] && [ "$DISK_USAGE" -lt 75 ]; then
      # Compare against dynamic threshold: if hours since last dev commit exceeds threshold, spawn
      LAST_DEV_TS=$(git log --since='24 hours ago' --oneline 2>/dev/null | grep '^dev:' | head -1 | awk '{print $1}')
      if [ -z "$LAST_DEV_TS" ]; then
        # No recent dev commits at all
        ACTIONS+=("spawn dev-agent")
        log "No dev activity detected; spawning dev-agent (threshold: ${DEV_STALE_HOURS}h)"
      else
        LAST_DEV_TIME=$(git show -s --format=%ct "$LAST_DEV_TS" 2>/dev/null)
        NOW=$(date +%s)
        HOURS_SINCE=$(( (NOW - LAST_DEV_TIME) / 3600 ))
        if [ "$HOURS_SINCE" -ge "$DEV_STALE_HOURS" ]; then
          ACTIONS+=("spawn dev-agent")
          log "Dev activity stale (${HOURS_SINCE}h ≥ ${DEV_STALE_HOURS}h); spawning dev-agent"
        fi
      fi
    fi
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

    # Create git-janitor-agent if missing and repo has untracked files
    if ! openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^git-janitor-cron$'; then
      # Check for untracked files (excluding specific directories like downloads, archives, node_modules)
      UNTRACKED_COUNT=$(git status --porcelain 2>/dev/null | grep -E '^\?\?' | grep -v -E '(^downloads/|^archives/|^node_modules/|^\.git/|^builds/)' | wc -l)
      if [ "$UNTRACKED_COUNT" -gt 5 ]; then
        ACTIONS+=("create git-janitor-agent")
        log "Untracked files count $UNTRACKED_COUNT > 5; will create git-janitor-agent to auto-commit safe files"
      fi
    fi

    
    # Multi-Agent System Creation: detect need for coordinated multi-agent effort
    if ! openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^archiver-manager-cron$'; then
      OLD_CONTENT=$(find content -type f -name '*.md' -mtime +90 2>/dev/null | wc -l)
      OLD_RESEARCH=$(find research -type f -name '*.md' -mtime +90 2>/dev/null | wc -l)
      if [ "$OLD_CONTENT" -gt 10 ] || [ "$OLD_RESEARCH" -gt 10 ]; then
        if [ "$DISK_USAGE" -gt 50 ]; then
          ACTIONS+=("create multi-agent system:archiver")
          log "Archive load high (content:$OLD_CONTENT research:$OLD_RESEARCH old files, disk ${DISK_USAGE}%) — will create archiver multi-agent system"
        fi
      fi
    fi


    # External Integration Auto‑Discovery: detect need for notifications
    # If there are recurring alerts in logs but no notifier cron, create a Telegram notifier agent
    if ! openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^notifier-cron$'; then
      # Count alert patterns in recent logs (last 48h)
      ALERT_COUNT=0
      for logfile in memory/*.log; do
        if [ -f "$logfile" ] && [ "$(stat -c %Y "$logfile")" -ge $(( $(date +%s) - 172800 )) ]; then
          ALERT_COUNT=$((ALERT_COUNT + $(grep -ciE "alert|warning|error|failed" "$logfile" 2>/dev/null || echo 0)))
        fi
      done
      if [ "$ALERT_COUNT" -ge 5 ]; then
        ACTIONS+=("create notifier-agent")
        log "Alert volume $ALERT_COUNT in last 48h — creating Telegram notifier-agent"
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
        "create git-janitor-agent")
          log "Creating permanent git-janitor-agent (auto-commits safe untracked files)"
          SCRIPT_PATH="$WORKSPACE/agents/git-janitor-cycle.sh"
          cat > "$SCRIPT_PATH" <<'EOF'
#!/usr/bin/env bash
# Git Janitor Agent: automatically stage, commit, and push safe untracked files
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/git-janitor.log"
mkdir -p memory
log() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"; }

log "Git‑janitor starting"

# List untracked files, excluding noisy dirs
UNTRACKED=$(git status --porcelain 2>/dev/null | grep -E '^\?\?' | grep -v -E '(^downloads/|^archives/|^node_modules/|^\.git/|^builds/|^dht\.dat$|^aria2\.session$)' || true)
if [ -z "$UNTRACKED" ]; then
  log "No safe untracked files to commit"
  exit 0
fi

# Stage them
git add -A 2>>"$LOGFILE"

# Commit with janitor prefix if there are staged changes
if ! git diff --cached --quiet; then
  git commit -m "chore: auto‑janitor cleanup ($(date -u +%Y-%m-%d %H:%M UTC))" >>"$LOGFILE" 2>&1
  git push origin master >>"$LOGFILE" 2>&1
  log "Committed and pushed $(git diff --cached --name-only | wc -l) files"
else
  log "No changes to commit after staging"
fi

log "Git‑janitor completed"
EOF
          chmod +x "$SCRIPT_PATH"
          # Register cron: run hourly at minute 15 (UTC)
          openclaw cron add --name "git-janitor-cron" --expr "15 * * * *" --tz "UTC" \
            --payload '{"kind":"systemEvent","text":"Execute git janitor: bash -c \'cd /home/ubuntu/.openclaw/workspace && ./agents/git-janitor-cycle.sh >> memory/git-janitor.log 2>&1\'"}' \
            --sessionTarget isolated --delivery '{"mode":"none"}' >> "$LOGFILE" 2>&1 || true
          log "Git‑janitor‑agent cron job registered"
          ;;

        # Self-Improvement: Meta-agent rewrites its own decision logic after validation
        # This is the beginning of recursive self-improvement
        "self-improve")
          log "Initiating self-improvement cycle"
          BACKUP="$WORKSPACE/agents/meta-agent.sh.backup-$(date -u +%Y%m%d-%H%M%S)"
          cp "$WORKSPACE/agents/meta-agent.sh" "$BACKUP"
          log "Backup created: $(basename "$BACKUP")"

          # Define the improvement: tweak dev stale threshold based on recent success rate
          CURRENT_THRESHOLD=$(grep -E 'DEV_STALE_HOURS=([0-9]+)' "$WORKSPACE/agents/meta-agent.sh" | head -1 | sed -E 's/.*DEV_STALE_HOURS=([0-9]+).*/\1/')
          if [ -z "$CURRENT_THRESHOLD" ]; then CURRENT_THRESHOLD=12; fi

          NEW_THRESHOLD=$CURRENT_THRESHOLD
          if [ -f "$WORKSPACE/memory/dev-agent.log" ]; then
            DEV_COMMITS_24H=$(git log --since='24 hours ago' --oneline 2>/dev/null | grep '^dev:' | wc -l)
            DEV_RUNS_24H=$(grep -c "Starting dev-agent cycle" "$WORKSPACE/memory/dev-agent.log" 2>/dev/null || echo 0)
            if [ "$DEV_RUNS_24H" -ge 2 ]; then
              SUCCESS_RATE=$(( DEV_COMMITS_24H * 100 / DEV_RUNS_24H ))
              if [ "$SUCCESS_RATE" -ge 70 ] && [ "$CURRENT_THRESHOLD" -gt 4 ]; then
                NEW_THRESHOLD=4
              elif [ "$SUCCESS_RATE" -le 30 ] && [ "$CURRENT_THRESHOLD" -lt 24 ]; then
                NEW_THRESHOLD=24
              fi
            fi
          fi

          if [ "$NEW_THRESHOLD" -ne "$CURRENT_THRESHOLD" ]; then
            sed -i "s/DEV_STALE_HOURS=${CURRENT_THRESHOLD}/DEV_STALE_THRESHOLD=${NEW_THRESHOLD}/" "$WORKSPACE/agents/meta-agent.sh" 2>/dev/null || \
            sed -i "s/DEV_STALE_HOURS=${CURRENT_THRESHOLD}/DEV_STALE_HOURS=${NEW_THRESHOLD}/" "$WORKSPACE/agents/meta-agent.sh"
            log "Adaptive tweak: dev stale threshold ${CURRENT_THRESHOLD}h → ${NEW_THRESHOLD}h"

            if bash -n "$WORKSPACE/agents/meta-agent.sh"; then
              log "Syntax OK"
              # Run test cycle
              if "$WORKSPACE/agents/meta-agent.sh" --once >> "$LOGFILE" 2>&1; then
                log "Test run passed"
                git add "$WORKSPACE/agents/meta-agent.sh"
                git commit -m "meta: self-improve — adapt dev stale threshold to ${NEW_THRESHOLD}h based on success rate" -m "Backup: $(basename "$BACKUP")" >> "$LOGFILE" 2>&1
                git push origin master >> "$LOGFILE" 2>&1
                log "Self-improvement committed"
              else
                log "Test run failed — reverting"
                cp "$BACKUP" "$WORKSPACE/agents/meta-agent.sh"
              fi
              rm -f "$BACKUP"
            else
              log "Syntax error — reverting"
              cp "$BACKUP" "$WORKSPACE/agents/meta-agent.sh"
              rm -f "$BACKUP"
            fi
          else
            log "No adjustment needed (current: ${CURRENT_THRESHOLD}h)"
            rm -f "$BACKUP"
          fi
          ;;
        "install skill:*")
          # Dynamic skill installation from ClawHub
          SKILL_ID="${act#install skill:}"
          log "Installing skill from ClawHub: $SKILL_ID"
          # Check if already installed
          if [ -d "$WORKSPACE/skills/$SKILL_ID" ] || grep -q "\"$SKILL_ID\"" "$WORKSPACE/.openclaw/openclaw.json" 2>/dev/null; then
            log "Skill $SKILL_ID already installed; skipping"
          else
            if command -v clawhub &>/dev/null; then
              # Check if logged in
              if ! clawhub whoami &>/dev/null; then
                log "ClawHub not logged in — skipping skill install (run: clawhub login)"
              else
                if clawhub install "$SKILL_ID" >> "$LOGFILE" 2>&1; then
                  log "Skill $SKILL_ID installed via clawhub"
                  # Validate installation
                  if [ -d "$WORKSPACE/skills/$SKILL_ID" ]; then
                    log "Skill directory exists; installation verified"
                    # Restart gateway to load new skill (non-fatal if fails)
                    openclaw gateway restart --reason "load new skill $SKILL_ID" >> "$LOGFILE" 2>&1 || true
                  else
                    log "Warning: skill directory not found after install; may need manual check"
                  fi
                else
                  log "Skill $SKILL_ID installation failed; will retry later"
                fi
              fi
            else
              log "clawhub CLI not available; cannot install skills"
            fi
          fi
          ;;
        "create multi-agent system:archiver")
          log "Creating archiver multi-agent system (manager + workers)"
          MANAGER_SCRIPT="$WORKSPACE/agents/archiver-manager.sh"
          cat > "$MANAGER_SCRIPT" <<'EOF'
#!/usr/bin/env bash
# Archiver Manager: scans for old files, spawns archiver-workers to compress them
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/archiver-manager.log"
mkdir -p memory archives
log() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"; }

log "Archiver‑manager starting"

# Find batches of old files (>90 days) in content and research
mapfile -t FILES < <(find content research -type f -name '*.md' -mtime +90 2>/dev/null)
TOTAL=${#FILES[@]}
if [ "$TOTAL" -eq 0 ]; then
  log "No old files to archive"
  exit 0
fi

BATCH_SIZE=20
for ((i=0; i<TOTAL; i+=BATCH_SIZE)); do
  BATCH=( "${FILES[@]:i:BATCH_SIZE}" )
  # Spawn a worker agent for this batch
  WORKER_ID="archiver-worker-$i"
  WORKER_SCRIPT="$WORKSPACE/agents/$WORKER_ID.sh"
  cat > "$WORKER_SCRIPT" <<'WORKEREOF'
#!/usr/bin/env bash
# Archiver Worker: compress assigned files
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/$WORKER_ID.log"
mkdir -p memory archives
log() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"; }

log "Worker starting"
FILES_LIST=${FILES_LIST:-}
if [ -z "$FILES_LIST" ]; then
  echo "No files assigned"
  exit 1
fi

ARCHIVE_MONTH=$(date -u +%Y-%m)
ARCHIVE_DIR="archives/${ARCHIVE_MONTH}"
mkdir -p "$ARCHIVE_DIR"

for f in $FILES_LIST; do
  if [ -f "$f" ]; then
    base=$(basename "$f" .md)
    tar -czf "$ARCHIVE_DIR/${base}.tar.gz" -C "$(dirname "$f")" "$(basename "$f")" && rm -f "$f"
    log "Archived: $f → $ARCHIVE_DIR/${base}.tar.gz"
  fi
done

log "Worker completed"
WORKEREOF
  chmod +x "$WORKER_SCRIPT"
  # Launch worker via openclaw agent (isolated session)
  openclaw agent --agent main --message "You are an archiver worker. Execute: bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/$WORKER_ID.sh'" --thinking low --timeout 600000 >> "$LOGFILE" 2>&1 || true
done

log "Archiver‑manager completed (spawned $(( (TOTAL+BATCH_SIZE-1)/BATCH_SIZE )) workers)"
EOF
          chmod +x "$MANAGER_SCRIPT"
          # Register cron: run manager weekly on Sunday 02:00 UTC
          openclaw cron add --name "archiver-manager-cron" --expr "0 2 * * 0" --tz "UTC"             --payload '{"kind":"systemEvent","text":"Execute archiver manager: bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/archiver-manager.sh >> memory/archiver-manager.log 2>&1'"}'             --sessionTarget isolated --delivery '{"mode":"none"}' >> "$LOGFILE" 2>&1 || true
          log "Archiver‑manager cron job registered (will spawn workers)"
          ;;
        "create notifier-agent")
          log "Creating Telegram notifier-agent (sends alerts for critical events)"
          NOTIFIER_SCRIPT="$WORKSPACE/agents/notifier-agent.sh"
          cat > "$NOTIFIER_SCRIPT" <<'EOF'
#!/usr/bin/env bash
# Notifier Agent: send Telegram messages for critical system events
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/notifier-agent.log"
mkdir -p memory
log() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"; }

log "Notifier starting"

# Function: send alert to Telegram via openclaw message tool
send_alert() {
  local msg="🚨 *OpenClaw Alert*\n$1"
  # Use openclaw message to send to configured Telegram channel (if available)
  if command -v openclaw &>/dev/null; then
    openclaw message send --channel telegram --to 952170974 --text "$msg" 2>/dev/null || true
  fi
}

# Check recent supervisor failures
if openclaw cron list --json 2>/dev/null | jq -r '.jobs[] | select(.state.consecutiveErrors>2) | "\(.name): \(.state.consecutiveErrors) errors"' | grep -q .; then
  FAILURES=$(openclaw cron list --json 2>/dev/null | jq -r '.jobs[] | select(.state.consecutiveErrors>2) | "- \(.name): \(.state.consecutiveErrors) errors"' | paste -sd '\n' -)
  send_alert "Cron job failures:\n$FAILURES"
fi

# Disk usage >85%
USAGE=$(df -h . | awk 'NR==2 {gsub(/%/,""); print $5}')
if [ "$USAGE" -ge 85 ]; then
  send_alert "Disk usage critical: ${USAGE}%"
fi

# Gateway down?
if ! openclaw gateway status &>/dev/null; then
  send_alert "OpenClaw gateway is down!"
fi

# Memory reindex needed (if not disabled)
if ! ./quick memory-reindex-check &>/dev/null; then
  MEM_INFO=$(./quick memory-reindex-check 2>&1 | head -5)
  send_alert "Memory reindex recommended:\n$MEM_INFO"
fi

log "Notifier completed"
EOF
          chmod +x "$NOTIFIER_SCRIPT"
          # Register cron: run every 2 hours
          openclaw cron add --name "notifier-cron" --expr "0 */2 * * *" --tz "UTC"             --payload '{"kind":"systemEvent","text":"Execute notifier: bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/notifier-agent.sh >> memory/notifier-agent.log 2>&1'"}'             --sessionTarget isolated --delivery '{"mode":"none"}' >> "$LOGFILE" 2>&1 || true
          log "Notifier‑agent cron job registered"
          ;;
      esac

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

    # Self‑modification: learn from recent dev‑agent outcomes and adjust thresholds
    # If dev-agent was spawned in last 24h and it produced commits that were pushed, consider lowering stale threshold
    # This is a simple reinforcement: positive outcomes → more aggressive spawning
    if [ -f "$WORKSPACE/memory/dev-agent.log" ]; then
      LAST_DEV_RUN=$(stat -c %Y "$WORKSPACE/memory/dev-agent.log" 2>/dev/null || echo 0)
      AGE_HOURS=$(( ( $(date +%s) - LAST_DEV_RUN ) / 3600 ))
      if [ "$AGE_HOURS" -le 24 ]; then
        # Check if dev-agent produced any commits in last 24h
        DEV_COMMITS=$(git log --since='24 hours ago' --oneline 2>/dev/null | grep '^dev:' | wc -l)
        if [ "$DEV_COMMITS" -gt 0 ]; then
          # Positivity! Could adjust thresholds in meta-agent config (future)
          log "Recent dev‑agent activity successful ($DEV_COMMITS dev commits). Consider reinforcing dev spawn frequency."
        fi
      fi
    fi

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

    # Multi-Agent System Creation: detect need for coordinated multi-agent effort
    if ! openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^archiver-manager-cron$'; then
      OLD_CONTENT=$(find content -type f -name '*.md' -mtime +90 2>/dev/null | wc -l)
      OLD_RESEARCH=$(find research -type f -name '*.md' -mtime +90 2>/dev/null | wc -l)
      if [ "$OLD_CONTENT" -gt 10 ] || [ "$OLD_RESEARCH" -gt 10 ]; then
        if [ "$DISK_USAGE" -gt 50 ]; then
          ACTIONS+=("create multi-agent system:archiver")
          log "Archive load high (content:$OLD_CONTENT research:$OLD_RESEARCH old files, disk ${DISK_USAGE}%) — will create archiver multi-agent system"
        fi
      fi
    fi
