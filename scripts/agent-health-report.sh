#!/usr/bin/env bash
# scripts/agent-health-report.sh — Concise health report for all key agents
# Shows: last run time, error count (last 50 lines), and status indicator
# Usage: ./scripts/agent-health-report.sh [--json]
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"
JSON_MODE=false
[[ "${1:-}" == "--json" ]] && JSON_MODE=true

# ─── helpers ────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

log_last_run() {
  local log="$1"
  [ -f "$log" ] || { echo "never"; return; }
  # Try to extract a timestamp from the last meaningful line
  local last
  last=$(grep -m1 "" "$log" 2>/dev/null | tail -1) || true
  # Get file modification time as fallback
  stat -c "%y" "$log" 2>/dev/null | cut -d'.' -f1 | sed 's/ / /'
}

log_last_line() {
  local log="$1"
  [ -f "$log" ] || { echo "(no log)"; return; }
  tail -1 "$log" 2>/dev/null | cut -c1-80 || echo "(empty)"
}

error_count() {
  local log="$1"
  [ -f "$log" ] || { echo "0"; return; }
  local count
  count=$(tail -50 "$log" 2>/dev/null | grep -ciE "error|Error|ERROR|failed|FAILED|fatal|FATAL" 2>/dev/null) || count=0
  # Ensure single integer
  echo "${count//[^0-9]/0}" | head -1
}

hours_since() {
  local log="$1"
  [ -f "$log" ] || { echo 9999; return; }
  local mtime now diff
  mtime=$(stat -c "%Y" "$log" 2>/dev/null || echo 0)
  now=$(date +%s)
  diff=$(( (now - mtime) / 3600 ))
  echo "$diff"
}

# ─── agent definitions ───────────────────────────────────────────────────────
declare -A AGENTS=(
  [meta-supervisor]="$(ls -t $WORKSPACE/agents/meta-supervisor/logs/*.log 2>/dev/null | head -1)"
  [meta-agent]="memory/meta-agent.log"
  [agent-manager]="memory/agent-manager.log"
  [dev-agent]="memory/dev-agent.log"
  [content-agent]="memory/content-agent.log"
  [research-agent]="memory/research-agent.log"
  [linkedin-pa-agent]="memory/linkedin-pa-agent.log"
  [idea-generator]="memory/idea-generator.log"
  [idea-executor]="memory/idea-executor.log"
  [git-janitor]="memory/git-janitor.log"
  [notifier-agent]="memory/notifier-agent.log"
  [archiver-manager]="memory/archiver-manager.log"
  [cron-supervisor]="memory/cron-supervisor.log"
  [daily-digest]="memory/daily-digest.log"
)

AGENT_ORDER=(
  meta-supervisor agent-manager meta-agent
  dev-agent research-agent content-agent linkedin-pa-agent
  idea-generator idea-executor git-janitor
  notifier-agent archiver-manager cron-supervisor daily-digest
)

# ─── JSON output ─────────────────────────────────────────────────────────────
if $JSON_MODE; then
  echo "{"
  echo "  \"generated\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
  echo "  \"agents\": {"
  first=true
  for agent in "${AGENT_ORDER[@]}"; do
    log="${AGENTS[$agent]}"
    hrs=$(hours_since "$log")
    errs=$(error_count "$log")
    last_line=$(log_last_line "$log" | sed 's/"/\\"/g')
    $first || echo "    ,"
    first=false
    printf '    "%s": {"hours_since_update": %s, "recent_errors": %s, "last_line": "%s"}\n' \
      "$agent" "$hrs" "$errs" "$last_line"
  done
  echo "  }"
  echo "}"
  exit 0
fi

# ─── Pretty output ────────────────────────────────────────────────────────────
NOW=$(date -u '+%Y-%m-%d %H:%M UTC')
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║       Agent Health Report — ${NOW}       ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

printf "%-24s %-12s %-8s %s\n" "AGENT" "LAST UPDATE" "ERRORS" "STATUS"
printf "%-24s %-12s %-8s %s\n" "────────────────────────" "───────────" "───────" "──────────────────────────────"

for agent in "${AGENT_ORDER[@]}"; do
  log="${AGENTS[$agent]}"
  hrs=$(hours_since "$log")
  errs=$(error_count "$log")

  # Status indicator
  if [ ! -f "$log" ]; then
    status="${YELLOW}⚠ no log${NC}"
    hrs_display="never"
  elif [ "$hrs" -gt 24 ]; then
    status="${YELLOW}⚠ stale (${hrs}h)${NC}"
    hrs_display="${hrs}h ago"
  elif [ "$errs" -gt 5 ]; then
    status="${RED}✗ errors (${errs})${NC}"
    hrs_display="${hrs}h ago"
  elif [ "$errs" -gt 0 ]; then
    status="${YELLOW}~ ok (${errs} errs)${NC}"
    hrs_display="${hrs}h ago"
  else
    status="${GREEN}✓ healthy${NC}"
    hrs_display="${hrs}h ago"
  fi

  printf "%-24s %-12s %-8s " "$agent" "$hrs_display" "$errs"
  echo -e "$status"
done

echo ""
# ─── Gateway status ──────────────────────────────────────────────────────────
echo -n "Gateway: "
if openclaw gateway status &>/dev/null 2>&1; then
  echo -e "${GREEN}✓ running${NC}"
else
  echo -e "${RED}✗ offline${NC}"
fi

# ─── Git status ──────────────────────────────────────────────────────────────
DIRTY=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$DIRTY" -eq 0 ]; then
  echo -e "Git:     ${GREEN}✓ clean${NC}"
else
  echo -e "Git:     ${YELLOW}~ ${DIRTY} uncommitted files${NC}"
fi

# ─── Disk usage ──────────────────────────────────────────────────────────────
DISK=$(df -h / | tail -1 | awk '{print $5}')
DISK_PCT=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_PCT" -ge 85 ]; then
  echo -e "Disk:    ${RED}✗ ${DISK} used — critical!${NC}"
elif [ "$DISK_PCT" -ge 75 ]; then
  echo -e "Disk:    ${YELLOW}~ ${DISK} used${NC}"
else
  echo -e "Disk:    ${GREEN}✓ ${DISK} used${NC}"
fi

echo ""
echo -e "${CYAN}Use --json for machine-readable output.${NC}"
