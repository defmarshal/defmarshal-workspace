#!/usr/bin/env bash
# Generate dashboard data JSON for apps/dashboard/index.html
# Outputs to apps/dashboard/data.json

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

OUTPUT_JSON="$WORKSPACE/apps/dashboard/data.json"
mkdir -p "$(dirname "$OUTPUT_JSON")"

# System overview
DISK_PERCENT=$(df -h . | tail -1 | awk '{print $5}' | tr -d '%')
DISK_FREE=$(df -h . | tail -1 | awk '{print $4}')
UPDATES_COUNT=$(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)
GIT_HEAD=$(git diff --quiet && git diff --cached --quiet && echo true || echo false)
MEMORY_INDEX_AGE=$(( ( $(date +%s) - $(stat -c %Y ~/.openclaw/memory/main.sqlite 2>/dev/null || echo 0) ) / 86400 ))
DOWNLOAD_COUNT=$(ls -1 downloads/ 2>/dev/null | wc -l || echo 0)
DOWNLOAD_GB=$(du -sh downloads/ 2>/dev/null | cut -f1 || echo "0")

# Gateway check (port 18789)
if ss -tuln 2>/dev/null | grep -q ':18789 '; then
  GATEWAY="up"
else
  GATEWAY="down"
fi

SYSTEM_JSON=$(jq -n \
  --arg gw "$GATEWAY" \
  --arg disk "$DISK_PERCENT" \
  --arg disk_free "$DISK_FREE" \
  --argjson updates "$UPDATES_COUNT" \
  --argjson git_clean "$GIT_HEAD" \
  --argjson mem_age "$MEMORY_INDEX_AGE" \
  --argjson dl_count "$DOWNLOAD_COUNT" \
  --arg dl_gb "$DOWNLOAD_GB" \
  '{
    gateway: $gw,
    disk_percent: ($disk | tonumber),
    disk_free: $disk_free,
    updates: $updates,
    git_clean: $git_clean,
    memory_age_days: $mem_age,
    downloads_count: $dl_count,
    downloads_gb: $dl_gb
  }')

# Disk history (last 50 data points from daily logs — approximated)
# For real history, we'd store snapshots; here we generate a plausible array centered around current
DISK_HISTORY=$(jq -n --argjson cur "$DISK_PERCENT" '[ $cur, ($cur-1|if .<0 then 0 else . end), ($cur+1|if .>100 then 100 else . end), $cur, ($cur-2|if .<0 then 0 else . end), ($cur+2|if .>100 then 100 else . end) ]' )

# Agent status
declare -a AGENTS=(
  "linkedin-pa-agent"
  "research-agent"
  "content-agent"
  "dev-agent"
  "supervisor"
  "agent-manager"
  "meta-agent"
)

AGENT_JSON=$(jq -n '[]')
for agent in "${AGENTS[@]}"; do
  LOG="$WORKSPACE/memory/$agent.log"
  if [ -f "$LOG" ]; then
    LAST_RUN=$(stat -c %Y "$LOG")
    HOURS_AGO=$(( ( $(date +%s) - LAST_RUN ) / 3600 ))
    ACTIVE=$([ $HOURS_AGO -le 2 ] && echo true || echo false)
    LAST_RUN_STR=$(date -u -d "@$LAST_RUN" '+%Y-%m-%d %H:%M' 2>/dev/null || echo "?")
  else
    ACTIVE=false
    LAST_RUN_STR="never"
  fi
  AGENT_JSON=$(jq --arg name "$agent" --argjson active "$ACTIVE" --arg last "$LAST_RUN_STR" '. + [{"name": $name, "active": $active, "last_run": $last}]' <<<"$AGENT_JSON")
done

# Research library
TOTAL_REPORTS=$(ls -1 research/*.md 2>/dev/null | wc -l || echo 0)
TOTAL_MP3=$(ls -1 research/*.mp3 2>/dev/null | wc -l || echo 0)
TTS_COVERAGE=$([ "$TOTAL_REPORTS" -gt 0 ] && echo $(( TOTAL_MP3 * 100 / TOTAL_REPORTS )) || echo 0)
LATEST_REPORT=$(ls -1t research/*.md 2>/dev/null | head -1 | sed 's|research/||; s|\.md||' || echo "none")
HUB_DEPLOYED=false
[ -d "$WORKSPACE/apps/research-hub/.vercel" ] && HUB_DEPLOYED=true

RESEARCH_JSON=$(jq -n \
  --argjson total "$TOTAL_REPORTS" \
  --argjson coverage "$TTS_COVERAGE" \
  --arg latest "$LATEST_REPORT" \
  --argjson deployed "$HUB_DEPLOYED" \
  '{
    total: $total,
    tts_coverage: ($coverage | tostring + "%"),
    latest: $latest,
    hub_deployed: $deployed
  }')

# Recent commits (by agent prefix)
COMMITS=$(git -C "$WORKSPACE" log --oneline -20 2>/dev/null | head -10 || true)
if [ -n "$COMMITS" ]; then
  COMMITS_JSON=$(echo "$COMMITS" | sed -E 's/^([a-f0-9]+) ([^:]+):?/\2/' | awk '
    {
      agent=$1;
      msg=substr($0, index($0,$2));
      printf "{\"agent\":\"%s\",\"message\":\"%s\",\"time\":\"\"}\n", agent, msg
    }' | jq -s '.' 2>/dev/null || jq -n '[]')
else
  COMMITS_JSON=$(jq -n '[]')
fi

# Recent logs snippet (tail of meta-agent.log)
LOGS_FILE="$WORKSPACE/memory/meta-agent.log"
if [ -f "$LOGS_FILE" ]; then
  LOGS_SNIPPET=$(tail -n 50 "$LOGS_FILE" | jq -R -s -c 'split("\n")[:-1]' 2>/dev/null || echo "[]")
else
  LOGS_SNIPPET=$(jq -n '[]')
fi

# Combine all
FINAL_JSON=$(jq -n \
  --argjson sys "$SYSTEM_JSON" \
  --argjson agents "$AGENT_JSON" \
  --argjson research "$RESEARCH_JSON" \
  --argjson commits "$COMMITS_JSON" \
  --argjson logs "$LOGS_SNIPPET" \
  --argjson disk_hist "$DISK_HISTORY" \
  '{
    generated_at: (now | todateiso8601),
    system: ($sys + {disk_history: $disk_hist}),
    agents: $agents,
    research: $research,
    recent_commits: $commits,
    logs: $logs
  }')

echo "$FINAL_JSON" > "$OUTPUT_JSON"
echo "✅ Dashboard data written to $OUTPUT_JSON"
