#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/notifier-agent.log"
mkdir -p memory

log() {
  echo "$(date -u +%Y-%m-%d\ %H:%M:%S) UTC - $*" >> "$LOGFILE"
}

log "Notifier starting"

# Fetch cron status once (with timeout to prevent hangs)
CRON_JSON=$(timeout 15 openclaw cron list --json 2>/dev/null) || CRON_JSON=""

if [ -n "$CRON_JSON" ]; then
  # Check for cron job failures (>2 consecutive errors)
  FAILURES=$(echo "$CRON_JSON" | jq -r '.jobs[] | select(.state.consecutiveErrors>2) | "- \(.name): \(.state.consecutiveErrors) errors"' | paste -sd '\n' -)
  if [ -n "$FAILURES" ]; then
    openclaw message send --channel telegram --to 952170974 --text "🚨 *OpenClaw Alert*\nCron job failures:\n$FAILURES" 2>/dev/null || true
  fi
fi

# Check disk usage (with timeout)
USAGE=$(timeout 5 df -h . | awk 'NR==2 {gsub(/%/,""); print $5}') || USAGE=0
if [ "$USAGE" -ge 85 ]; then
  openclaw message send --channel telegram --to 952170974 --text "🚨 Disk usage critical: ${USAGE}%" 2>/dev/null || true
fi

# Check gateway status (with timeout)
if ! timeout 5 openclaw gateway status &>/dev/null; then
  openclaw message send --channel telegram --to 952170974 --text "🚨 OpenClaw gateway is down!" 2>/dev/null || true
fi

log "Notifier completed"
