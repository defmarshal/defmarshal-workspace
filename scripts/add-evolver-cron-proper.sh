#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

if openclaw cron list --json 2>/dev/null | jq -r '.jobs[] | select(.name=="evolver-agent-cron") | .id' | grep -q .; then
  echo "Evolver cron job already exists"
  exit 0
fi

# Build the message carefully using printf to avoid shell interpretation
MESSAGE="Execute evolver: bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/evolver-cycle.sh >> memory/evolver-agent.log 2>&1'"

openclaw cron add \
  --name "evolver-agent-cron" \
  --cron "0 */6 * * *" \
  --tz "UTC" \
  --message "$MESSAGE" \
  --session isolated \
  --no-deliver

if [ $? -eq 0 ]; then
  echo "Successfully added evolver-agent-cron"
else
  echo "Failed to add cron job"
  exit 1
fi
