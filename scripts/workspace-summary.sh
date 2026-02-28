#!/usr/bin/env bash
# workspace-summary.sh — One-page daily status overview
# Prints: system health, research stats, content stats, git activity, agent status
#
# Usage: quick workspace-summary [--json]

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

JSON_MODE=false
[[ "${1:-}" == "--json" ]] && JSON_MODE=true

# ── Helpers ────────────────────────────────────────────────────────────────────
ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
today() { date -u +%Y-%m-%d; }
now_utc7() { TZ="Asia/Bangkok" date +"%H:%M ICT"; }

# ── System health ──────────────────────────────────────────────────────────────
disk_pct=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
disk_free=$(df -h / | tail -1 | awk '{print $4}')
load=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | tr -d ',')
mem_used=$(free -m | awk '/^Mem:/ {printf "%.0f%%", $3/$2*100}')

# ── Gateway health ─────────────────────────────────────────────────────────────
gw_status="unknown"
if curl -sf http://localhost:18789/health >/dev/null 2>&1; then
  gw_status="ok"
else
  gw_status="down"
fi

# ── Research stats ─────────────────────────────────────────────────────────────
today_date=$(today)
total_reports=$(ls -1 research/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.md 2>/dev/null | wc -l)
today_reports=$(ls -1 "research/${today_date}"-*.md 2>/dev/null | wc -l)

# ── Content stats ──────────────────────────────────────────────────────────────
today_content=$(ls -1 "content/${today_date}"-*.md 2>/dev/null | wc -l)
total_content=$(ls -1 content/*.md 2>/dev/null | wc -l)

# ── Git stats ──────────────────────────────────────────────────────────────────
today_commits=$(git log --oneline --since="$(today) 00:00:00" 2>/dev/null | wc -l)
last_commit=$(git log --oneline -1 2>/dev/null | cut -c1-60)
last_commit_ts=$(git log -1 --format="%cr" 2>/dev/null)

# ── Agent status ───────────────────────────────────────────────────────────────
meta_pid=""
meta_running="no"
if pgrep -f "meta-supervisor" >/dev/null 2>&1; then
  meta_pid=$(pgrep -f "meta-supervisor" | head -1)
  meta_running="yes (PID ${meta_pid})"
fi

# ── Dev log last entry ─────────────────────────────────────────────────────────
last_dev=$(grep "Completed cycle\|Completed" memory/dev-agent.log 2>/dev/null | tail -1 | cut -c1-80)

if [[ "$JSON_MODE" == "true" ]]; then
  cat <<EOF
{
  "timestamp": "$(ts)",
  "local_time": "$(now_utc7)",
  "system": {
    "disk_pct": $disk_pct,
    "disk_free": "$disk_free",
    "load": "$load",
    "mem_used": "$mem_used",
    "gateway": "$gw_status"
  },
  "research": {
    "total": $total_reports,
    "today": $today_reports
  },
  "content": {
    "total": $total_content,
    "today": $today_content
  },
  "git": {
    "today_commits": $today_commits,
    "last_commit": "$last_commit",
    "last_commit_age": "$last_commit_ts"
  },
  "agents": {
    "meta_supervisor": "$meta_running"
  }
}
EOF
else
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║          Workspace Summary — $(ts)          ║"
  echo "╚══════════════════════════════════════════════════════╝"
  echo ""
  echo "⏰ Local time : $(now_utc7)"
  echo ""
  echo "── System Health ─────────────────────────────────────"
  echo "  Disk        : ${disk_pct}% used (${disk_free} free)"
  echo "  Load        : ${load}"
  echo "  Memory      : ${mem_used}"
  echo "  Gateway     : ${gw_status}"
  echo ""
  echo "── Research ──────────────────────────────────────────"
  echo "  Total       : ${total_reports} reports"
  echo "  Today       : ${today_reports} new reports"
  echo ""
  echo "── Content ───────────────────────────────────────────"
  echo "  Total       : ${total_content} content files"
  echo "  Today       : ${today_content} new pieces"
  echo ""
  echo "── Git Activity ──────────────────────────────────────"
  echo "  Today       : ${today_commits} commits"
  echo "  Last commit : ${last_commit}"
  echo "  Age         : ${last_commit_ts}"
  echo ""
  echo "── Agents ────────────────────────────────────────────"
  echo "  meta-supervisor : ${meta_running}"
  [[ -n "$last_dev" ]] && echo "  Last dev    : ${last_dev}"
  echo ""
fi
