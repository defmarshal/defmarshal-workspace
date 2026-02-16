#!/bin/bash
# Workspace Validation — comprehensive health check
# Usage: ./workspace-validate.sh

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"

# Colors for output (optional)
RED=''
GREEN=''
YELLOW=''
NC=''  # No Color
if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  NC='\033[0m'
fi

# Helper: print status
status_ok() { echo -e "${GREEN}✓${NC} $1"; }
status_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
status_err() { echo -e "${RED}✗${NC} $1"; }

echo "== Workspace Validation =="
echo ""

# 1. Disk space
DISK_PCT=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_PCT" -ge 90 ]; then
  status_err "Disk usage ${DISK_PCT}% (CRITICAL)"
elif [ "$DISK_PCT" -ge 80 ]; then
  status_warn "Disk usage ${DISK_PCT}% (warning)"
else
  status_ok "Disk usage ${DISK_PCT}%"
fi

# 2. System updates
UPDATES=$(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)
if [ "$UPDATES" -gt 10 ]; then
  status_err "$UPDATES packages upgradable (high)"
elif [ "$UPDATES" -gt 0 ]; then
  status_warn "$UPDATES packages upgradable"
else
  status_ok "System up to date"
fi

# 3. Git status
cd "$WORKSPACE"
if git status --porcelain | grep -q .; then
  CHANGED=$(git status --porcelain | wc -l)
  status_warn "$CHANGED file(s) changed in workspace"
else
  status_ok "Git working tree clean"
fi

# 4. Memory system
MEM_OUTPUT=$(openclaw memory status --json 2>/dev/null || echo '[]')
if echo "$MEM_OUTPUT" | jq -e '.[0].status' >/dev/null 2>&1; then
  FILES=$(echo "$MEM_OUTPUT" | jq -r '.[0].status.files')
  CHUNKS=$(echo "$MEM_OUTPUT" | jq -r '.[0].status.chunks')
  DIRTY=$(echo "$MEM_OUTPUT" | jq -r '.[0].status.dirty')
  DIRTY_STATE="clean"
  [ "$DIRTY" = "true" ] && DIRTY_STATE="dirty"
  PROVIDER=$(echo "$MEM_OUTPUT" | jq -r '.[0].status.provider // "unknown"')
  status_ok "Memory: ${FILES}f/${CHUNKS}c (${DIRTY_STATE}) ${PROVIDER}"
else
  status_err "Memory system unavailable"
fi

# 5. Reindex log age
REINDEX_LOG="$WORKSPACE/memory/memory-reindex.log"
if [ -f "$REINDEX_LOG" ]; then
  AGE_DAYS=$(( ( $(date +%s) - $(stat -c %Y "$REINDEX_LOG") ) / 86400 ))
  if [ "$AGE_DAYS" -lt 7 ]; then
    status_ok "Reindex: ${AGE_DAYS}d ago"
  elif [ "$AGE_DAYS" -lt 30 ]; then
    status_warn "Reindex: ${AGE_DAYS}d ago (stale)"
  else
    status_err "Reindex: ${AGE_DAYS}d ago (very stale)"
  fi
else
  status_warn "Reindex: never"
fi

# 6. Gateway status
GW_SERVICE=$(systemctl --user is-active openclaw-gateway.service 2>/dev/null || echo "inactive")
GW_PORT=$(ss -tuln 2>/dev/null | grep -c ':18789 ' || echo 0)

if [ "$GW_SERVICE" = "active" ] && [ "$GW_PORT" -gt 0 ]; then
  if timeout 2 openclaw gateway probe >/dev/null 2>&1; then
    status_ok "Gateway: healthy"
  else
    status_warn "Gateway: service up but RPC unreachable"
  fi
else
  status_err "Gateway: down (service: $GW_SERVICE, port: $GW_PORT lines)"
fi

# 7. Agent cron jobs (count expected)
EXPECTED_JOBS=11
ACTUAL_JOBS=$(openclaw cron list --json 2>/dev/null | jq 'length' 2>/dev/null || echo "0")
if [ "$ACTUAL_JOBS" -eq "$EXPECTED_JOBS" ]; then
  status_ok "Cron jobs: $ACTUAL_JOBS (expected $EXPECTED_JOBS)"
elif [ "$ACTUAL_JOBS" -gt 0 ]; then
  status_warn "Cron jobs: $ACTUAL_JOBS (expected $EXPECTED_JOBS)"
else
  status_err "Cron jobs: none (gateway may be down)"
fi

# 8. Log file sizes (warn if large)
ARIA2_LOG="$WORKSPACE/aria2.log"
if [ -f "$ARIA2_LOG" ]; then
  SIZE_MB=$(( $(stat -c %s "$ARIA2_LOG") / 1024 / 1024 ))
  if [ "$SIZE_MB" -gt 100 ]; then
    status_warn "aria2.log is ${SIZE_MB}MB (should be rotated)"
  else
    status_ok "aria2.log size ${SIZE_MB}MB"
  fi
fi

# 9. Recent agent activity (check logs modified in last 24h)
RECENT_LOGS=0
for log in "$WORKSPACE"/*-agent.log; do
  [ -e "$log" ] || continue
  if [ "$(find "$log" -mmin -1440 2>/dev/null)" ]; then
    RECENT_LOGS=$((RECENT_LOGS+1))
  fi
done
if [ "$RECENT_LOGS" -ge 3 ]; then
  status_ok "Agent logs recent (${RECENT_LOGS} updated in 24h)"
else
  status_warn "Agent logs stale (only ${RECENT_LOGS} updated in 24h)"
fi

# 10. Quiet hours check
TZ='Asia/Bangkok' CURRENT_HOUR=$(date +%H)
if (( 23 <= 10#$CURRENT_HOUR || 10#$CURRENT_HOUR < 8 )); then
  status_warn "Quiet hours active (Bangkok $CURRENT_HOUR:00)"
else
  status_ok "Active hours (Bangkok $CURRENT_HOUR:00)"
fi

echo ""
echo "Validation complete. Review warnings above."
echo "Use 'quick gateway-status' and 'quick health' for more details."
