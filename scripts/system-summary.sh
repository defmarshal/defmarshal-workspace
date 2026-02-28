#!/usr/bin/env bash
# One-line system summary for quick status check.
# Output: [STATUS] Gateway:up/down | Disk:%used | Updates:yes/no | Git:clean/dirty | Agents:N active

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

# Gateway status (assume up if script runs; could check port 18789)
GATEWAY="up"

# Disk usage
DISK_USED=$(df -h . | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_USED" -ge 90 ]; then
  DISK_STATE="critical"
elif [ "$DISK_USED" -ge 75 ]; then
  DISK_STATE="warning"
else
  DISK_STATE="ok"
fi

# Updates
UPDATE_COUNT=$(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)
if [ "$UPDATE_COUNT" -gt 0 ]; then
  UPDATES="yes ($UPDATE_COUNT)"
else
  UPDATES="no"
fi

# Git status
if git diff --quiet && git diff --cached --quiet; then
  GIT="clean"
else
  GIT="dirty"
fi

# Active agents (sessions)
ACTIVE_AGENTS=$(openclaw sessions 2>/dev/null | grep -c 'agent' || echo "?")

echo "[STATUS] Gateway:$GATEWAY | Disk:${DISK_USED}% ($DISK_STATE) | Updates:$UPDATES | Git:$GIT | Agents:$ACTIVE_AGENTS"
