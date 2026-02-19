#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/notifier-agent.log"
mkdir -p memory

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"
}

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
