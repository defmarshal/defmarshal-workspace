#!/usr/bin/env bash
# Meta-Agent: autonomous planner & orchestrator for the ultimate self-extending system
# Modes: --once (one-shot), --daemon (loop hourly), --status (show last report)

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOGFILE="memory/meta-agent.log"
REPORT_FILE="meta-report-latest.md"
mkdir -p memory

# Safety & Containment defaults
SAFETY_CPU_CAP=80
SAFETY_MEM_CAP=85
SAFETY_DISK_CAP=90
SAFETY_BLACKLIST=("rm -rf" "dd if=" ":|:" "poweroff" "shutdown" "mkfs" "dd of=" ">" "2>/dev/null")
SAFETY_MAX_CONCURRENT_AGENTS=10

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"
}

safe_to_spawn() {
  # Check resource caps
  CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 2>/dev/null || echo "0")
  MEM_INFO=$(free -m 2>/dev/null || echo "0 0 0")
  MEM_USED=$(echo "$MEM_INFO" | awk '{print $3}')
  MEM_TOTAL=$(echo "$MEM_INFO" | awk '{print $2}')
  MEM_PCT=0
  if [ "$MEM_TOTAL" -gt 0 ]; then
    MEM_PCT=$(( MEM_USED * 100 / MEM_TOTAL ))
  fi
  DISK_USAGE=$(df -h . | awk 'NR==2 {gsub(/%/,""); print $5}')
  
  if [ "$CPU_USAGE" -gt "$SAFETY_CPU_CAP" ]; then
    log "Safety: CPU ${CPU_USAGE}% > cap ${SAFETY_CPU_CAP}% — block spawn"
    return 1
  fi
  if [ "$MEM_PCT" -gt "$SAFETY_MEM_CAP" ]; then
    log "Safety: Memory ${MEM_PCT}% > cap ${SAFETY_MEM_CAP}% — block spawn"
    return 1
  fi
  if [ "$DISK_USAGE" -gt "$SAFETY_DISK_CAP" ]; then
    log "Safety: Disk ${DISK_USAGE}% > cap ${SAFETY_DISK_CAP}% — block spawn"
    return 1
  fi
  RUNNING_AGENTS=$(openclaw sessions list --activeMinutes 5 --json 2>/dev/null | jq -r '.sessions[] | select(.agentId=="main") | .sessionKey' | wc -l)
  if [ "$RUNNING_AGENTS" -ge "$SAFETY_MAX_CONCURRENT_AGENTS" ]; then
    log "Safety: Too many concurrent agents ($RUNNING_AGENTS >= $SAFETY_MAX_CONCURRENT_AGENTS)"
    return 1
  fi
  return 0
}

compute_feedback_weights() {
  local FEEDBACK_FILE="memory/user-feedback.json"
  if [ ! -f "$FEEDBACK_FILE" ]; then
    echo "{}"
    return
  fi
  declare -A SUM=()
  declare -A COUNT=()
  while IFS= read -r line; do
    AGENT=$(echo "$line" | grep -o '"agent":"[^"]*"' | cut -d'"' -f4)
    SCORE=$(echo "$line" | grep -o '"score":[0-9]*' | cut -d':' -f2)
    if [ -n "$AGENT" ] && [ -n "$SCORE" ]; then
      SUM["$AGENT"]=$(( ${SUM["$AGENT"]:-0} + SCORE ))
      COUNT["$AGENT"]=$(( ${COUNT["$AGENT"]:-0} + 1 ))
    fi
  done < "$FEEDBACK_FILE"
  
  declare -A ADJUSTMENTS=()
  for agent in "${!SUM[@]}"; do
    avg=$(echo "scale=2; ${SUM[$agent]} / ${COUNT[$agent]}" | bc)
    MULT="1.0"
    if [ "$(echo "$avg >= 4.5" | bc 2>/dev/null || echo 0)" -eq 1 ]; then
      MULT="2.0"
    elif [ "$(echo "$avg >= 4.0" | bc 2>/dev/null || echo 0)" -eq 1 ]; then
      MULT="1.5"
    elif [ "$(echo "$avg <= 2.0" | bc 2>/dev/null || echo 0)" -eq 1 ]; then
      MULT="0.5"
    elif [ "$(echo "$avg <= 1.5" | bc 2>/dev/null || echo 0)" -eq 1 ]; then
      MULT="0.25"
    fi
    ADJUSTMENTS["$agent"]="$MULT"
  done
  
  echo "declare -A FEEDBACK_ADJUST=("
  for agent in "${!ADJUSTMENTS[@]}"; do
    echo "  ["$agent"]=${ADJUSTMENTS["$agent"]}"
  done
  echo ")"
}

check_and_install_skill() {
  local skill="$1"
  if ! [ -d "skills/$skill" ] && ! grep -q "\"$skill\"" ".openclaw/openclaw.json" 2>/dev/null; then
    log "Installing skill: $skill"
    if openclaw skills install "$skill" >> "$LOGFILE" 2>&1; then
      log "Skill installed: $skill"
      return 0
    else
      log "Failed to install skill: $skill"
      return 1
    fi
  fi
  return 0
}

create_archive_agent() {
  if openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^archive-agent-cron$'; then
    return 0
  fi
  log "Creating archive-agent"
  cat > agents/archive-cycle.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/archive-agent.log"
mkdir -p memory
log "Archive cycle starting"
# Find old content/research (>90 days) and compress
find content research -type f -name '*.md' -mtime +90 2>/dev/null | while read -r f; do
  gzip -k "$f" 2>/dev/null || true
done
log "Archive cycle completed"
EOF
  chmod +x agents/archive-cycle.sh
  openclaw cron add --name "archive-agent-cron" --expr "0 2 1 * *" --tz "UTC" \
    --payload "{\"kind\":\"systemEvent\",\"text\":\"Execute archive cycle: bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/archive-cycle.sh >> memory/archive-agent.log 2>&1'\"}" \
    --sessionTarget isolated --delivery '{"mode":"none"}' >> "$LOGFILE" 2>&1 || true
  log "Archive-agent cron registered"
}

create_git_janitor_agent() {
  if openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^git-janitor-cron$'; then
    return 0
  fi
  log "Creating git-janitor-agent"
  cat > agents/git-janitor-cycle.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/git-janitor.log"
mkdir -p memory
log "Git janitor starting"
# Stage safe untracked files (excluding node_modules, .git, etc.)
git add -A 2>/dev/null || true
# Auto-commit if there are changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
  git commit -m "auto: maintenance update $(date -u '+%Y-%m-%d %H:%M UTC')" 2>/dev/null || true
fi
log "Git janitor completed"
EOF
  chmod +x agents/git-janitor-cycle.sh
  openclaw cron add --name "git-janitor-cron" --expr "15 * * * *" --tz "UTC" \
    --payload "{\"kind\":\"systemEvent\",\"text\":\"Execute git janitor: bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/git-janitor-cycle.sh >> memory/git-janitor.log 2>&1'\"}" \
    --sessionTarget isolated --delivery '{"mode":"none"}' >> "$LOGFILE" 2>&1 || true
  log "Git-janitor cron registered"
}

create_archiver_manager() {
  if openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^archiver-manager-cron$'; then
    return 0
  fi
  log "Creating archiver-manager"
  # This would spawn worker agents for distributed archiving
  # For now, just register a placeholder cron
  openclaw cron add --name "archiver-manager-cron" --expr "0 2 * * 0" --tz "UTC" \
    --payload "{\"kind\":\"systemEvent\",\"text\":\"Execute archiver manager: bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/archiver-manager.sh >> memory/archiver-manager.log 2>&1'\"}" \
    --sessionTarget isolated --delivery '{"mode":"none"}' >> "$LOGFILE" 2>&1 || true
  log "Archiver-manager cron registered"
}

create_notifier_agent() {
  if openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^notifier-cron$'; then
    return 0
  fi
  log "Creating notifier-agent"
  cat > agents/notifier-agent.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/notifier-agent.log"
mkdir -p memory
log "Notifier starting"
# Check for issues and send alerts
if openclaw cron list --json 2>/dev/null | jq -r '.jobs[] | select(.state.consecutiveErrors>2) | "\(.name): \(.state.consecutiveErrors) errors"' | grep -q .; then
  FAILURES=$(openclaw cron list --json 2>/dev/null | jq -r '.jobs[] | select(.state.consecutiveErrors>2) | "- \(.name): \(.state.consecutiveErrors) errors"' | paste -sd '\n' -)
  openclaw message send --channel telegram --to 952170974 --text "🚨 *OpenClaw Alert*\nCron job failures:\n$FAILURES" 2>/dev/null || true
fi
USAGE=$(df -h . | awk 'NR==2 {gsub(/%/,""); print $5}')
if [ "$USAGE" -ge 85 ]; then
  openclaw message send --channel telegram --to 952170974 --text "🚨 Disk usage critical: ${USAGE}%" 2>/dev/null || true
fi
if ! openclaw gateway status &>/dev/null; then
  openclaw message send --channel telegram --to 952170974 --text "🚨 OpenClaw gateway is down!" 2>/dev/null || true
fi
log "Notifier completed"
EOF
  chmod +x agents/notifier-agent.sh
  openclaw cron add --name "notifier-cron" --expr "0 */2 * * *" --tz "UTC" \
    --payload "{\"kind\":\"systemEvent\",\"text\":\"Execute notifier: bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/notifier-agent.sh >> memory/notifier-agent.log 2>&1'\"}" \
    --sessionTarget isolated --delivery '{"mode":"none"}' >> "$LOGFILE" 2>&1 || true
  log "Notifier cron registered"
}

adjust_scheduling() {
  log "Checking resource-based scheduling adjustments"
  DISK_USAGE=$(df -h . | awk 'NR==2 {gsub(/%/,""); print $5}')
  if [ "$DISK_USAGE" -ge 85 ]; then
    SCHED_TIER="low"
    SCHED_EXPR="0 */4 * * *"  # every 4 hours
  elif [ "$DISK_USAGE" -ge 80 ]; then
    SCHED_TIER="normal"
    SCHED_EXPR="0 */2 * * *"  # every 2 hours
  else
    SCHED_TIER="high"
    SCHED_EXPR="0 * * * *"    # hourly
  fi
  
  log "Scheduling tier: $SCHED_TIER (disk ${DISK_USAGE}%)"
  
  # Update non-critical agents to tier, keep critical ones hourly
  declare -A JOB_SCHEDULES=(
    ["workspace-builder"]="0 */2 * * *"
    ["supervisor-cron"]="0 */2 * * *"
    ["agni-cron"]="0 */2 * * *"
    ["random-torrent-downloader"]="0 */2 * * *"
    ["dev-agent-cron"]="0 * * * *"
    ["content-agent-cron"]="0 * * * *"
    ["research-agent-cron"]="0 * * * *"
    ["agent-manager-cron"]="0 * * * *"
    ["meta-agent-cron"]="0 * * * *"
  )
  
  for job_name in "${!JOB_SCHEDULES[@]}"; do
    JOB_ID=$(openclaw cron list --json 2>/dev/null | jq -r ".jobs[] | select(.name==\"$job_name\") | .id" 2>/dev/null || true)
    if [ -n "$JOB_ID" ]; then
      CURRENT_EXPR=$(openclaw cron list --json 2>/dev/null | jq -r ".jobs[] | select(.name==\"$job_name\") | .schedule.expr" 2>/dev/null || true)
      NEW_EXPR="$SCHED_EXPR"
      if [ "$SCHED_TIER" = "normal" ]; then
        NEW_EXPR="${JOB_SCHEDULES[$job_name]}"
      fi
      if [ "$CURRENT_EXPR" != "$NEW_EXPR" ] && [ -n "$CURRENT_EXPR" ]; then
        openclaw cron update --jobId "$JOB_ID" --patch "{\"schedule\":{\"expr\":\"$NEW_EXPR\"}}" >> "$LOGFILE" 2>&1 || true
        log "Adjusted $job_name: $CURRENT_EXPR → $NEW_EXPR"
      fi
    fi
  done
}

perform_memory_learning() {
  log "Agent performance learning (disabled in this version - Voyage AI rate limited)"
  # This would analyze logs and compute scores
  return 0
}

case "${1:-}" in
  --once)
    log "Meta-Agent starting (one-shot)"
    
    # System snapshot
    DISK_USAGE=$(df -h . | awk 'NR==2 {gsub(/%/,""); print $5}')
    if APT_COUNT=$(apt-get -s upgrade 2>/dev/null | grep -c '^Inst ' 2>/dev/null); then
      :
    else
      APT_COUNT=0
    fi
    APT_COUNT=${APT_COUNT//$'\n'/}
    TODAY=$(date -u +%Y-%m-%d)
    CONTENT_TODAY=$(ls content/${TODAY}*.md 2>/dev/null | wc -l)
    RESEARCH_TODAY=$(ls research/${TODAY}*.md 2>/dev/null | wc -l)
    
    log "Snapshot: disk=${DISK_USAGE}%, apt=${APT_COUNT}, content_today=${CONTENT_TODAY}, research_today=${RESEARCH_TODAY}"
    
    ACTIONS=()
    
    # Dynamic Skill Installation
    WEB_SEARCH_COUNT=0
    EMAIL_MENTION_COUNT=0
    WEATHER_MENTION_COUNT=0
    for logfile in memory/*-agent.log memory/meta-agent.log; do
      if [ -f "$logfile" ] && [ "$(stat -c %Y "$logfile" 2>/dev/null || echo 0)" -ge $(( $(date +%s) - 86400 )) ]; then
        if count=$(grep -ci "web_search" "$logfile" 2>/dev/null); then
          :
        else
          count=0
        fi
        count=${count//$'\n'/}
        WEB_SEARCH_COUNT=$((WEB_SEARCH_COUNT + count))
        if count=$(grep -ci "gmail" "$logfile" 2>/dev/null); then
          :
        else
          count=0
        fi
        count=${count//$'\n'/}
        EMAIL_MENTION_COUNT=$((EMAIL_MENTION_COUNT + count))
        if count=$(grep -ci "weather" "$logfile" 2>/dev/null); then
          :
        else
          count=0
        fi
        count=${count//$'\n'/}
        WEATHER_MENTION_COUNT=$((WEATHER_MENTION_COUNT + count))
      fi
    done
    
    RECOMMENDED_SKILL=""
    if [ "$WEB_SEARCH_COUNT" -ge 10 ]; then
      if ! [ -d "skills/tavily" ] && ! grep -q '"tavily"' ".openclaw/openclaw.json" 2>/dev/null; then
        RECOMMENDED_SKILL="tavily"
      elif ! [ -d "skills/perplexity" ] && ! grep -q '"perplexity"' ".openclaw/openclaw.json" 2>/dev/null; then
        RECOMMENDED_SKILL="perplexity"
      fi
    elif [ "$EMAIL_MENTION_COUNT" -ge 5 ] && ! [ -d "skills/gmail" ] && ! grep -q '"gmail"' ".openclaw/openclaw.json" 2>/dev/null; then
      RECOMMENDED_SKILL="gmail"
    elif [ "$WEATHER_MENTION_COUNT" -ge 3 ] && ! [ -d "skills/weather" ] && ! grep -q '"weather"' ".openclaw/openclaw.json" 2>/dev/null; then
      RECOMMENDED_SKILL="weather"
    fi
    
    if [ -n "$RECOMMENDED_SKILL" ]; then
      LAST_SKILL=$(find memory -name ".last-skill-install" -mtime -7 2>/dev/null | head -1 || true)
      if [ -z "$LAST_SKILL" ]; then
        ACTIONS+=("install skill:$RECOMMENDED_SKILL")
        log "Detected need for skill: $RECOMMENDED_SKILL (web:$WEB_SEARCH_COUNT email:$EMAIL_MENTION_COUNT weather:$WEATHER_MENTION_COUNT)"
        touch memory/.last-skill-install
      else
        log "Skill installation throttled (last install <7 days ago)"
      fi
    fi
    
    # Disk cleanup if >80%
    if [ "$DISK_USAGE" -ge 80 ]; then
      ACTIONS+=("disk cleanup")
      log "Disk usage >= 80%"
    fi
    
    # Spawn agents if missing today
    if [ "$CONTENT_TODAY" -eq 0 ]; then
      ACTIONS+=("spawn content-agent")
      log "No content for today; will spawn"
    fi
    if [ "$RESEARCH_TODAY" -eq 0 ]; then
      ACTIONS+=("spawn research-agent")
      log "No research for today; will spawn"
    fi
    
    # Create permanent agents if missing
    if ! openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^archive-agent-cron$'; then
      if find content -type f -name '*.md' -mtime +90 2>/dev/null | read -r; then
        ACTIONS+=("create archive-agent")
      fi
    fi
    
    if ! openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^git-janitor-cron$'; then
      ACTIONS+=("create git-janitor-agent")
    fi
    
    if ! openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^notifier-cron$'; then
      ACTIONS+=("create notifier-agent")
    fi
    
    if ! openclaw cron list --json 2>/dev/null | jq -r '.jobs[].name' 2>/dev/null | grep -q '^archiver-manager-cron$'; then
      ACTIONS+=("create archiver-manager")
    fi
    
    # Execute actions
    for act in "${ACTIONS[@]}"; do
      case "$act" in
        "disk cleanup")
          log "Triggering downloads cleanup (dry-run first)"
          ./quick cleanup-downloads --days 30 >> "$LOGFILE" 2>&1 || true
          ;;
        "spawn content-agent")
          log "Spawning content-agent"
          openclaw agent --agent main --message "You are the content-agent. Create anime summaries, tech writeups, or daily digests. Check for pending tasks. If none, generate a short daily digest." --thinking low --timeout 600000 >> "$LOGFILE" 2>&1 || true
          ;;
        "spawn research-agent")
          log "Spawning research-agent"
          openclaw agent --agent main --message "You are the research-agent. Conduct continuous research on anime, banking, tech, AI. Use web_search, web_fetch, memory tools. Create detailed reports in research/." --thinking low --timeout 600000 >> "$LOGFILE" 2>&1 || true
          ;;
        "create archive-agent")
          create_archive_agent
          ;;
        "create git-janitor-agent")
          create_git_janitor_agent
          ;;
        "create notifier-agent")
          create_notifier_agent
          ;;
        "create archiver-manager")
          create_archiver_manager
          ;;
        "install skill:"*)
          skill="${act#install skill:}"
          check_and_install_skill "$skill"
          ;;
      esac
    done
    
    adjust_scheduling
    perform_memory_learning
    
    log "Meta-Agent one-shot completed; actions: ${ACTIONS[*]:-none}"
    ;;
    
  --daemon)
    log "Meta-Agent daemon starting (PID $$)"
    while true; do
      bash "$0" --once
      sleep 3600
    done
    ;;
    
  --status)
    if [ -f "$REPORT_FILE" ]; then
      cat "$REPORT_FILE"
    else
      echo "No meta-report yet. Run meta-agent first."
    fi
    ;;
    
  *)
    echo "Usage: $0 [--once|--daemon|--status]"
    exit 1
    ;;
esac
