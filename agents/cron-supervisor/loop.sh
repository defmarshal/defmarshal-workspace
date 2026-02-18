#!/usr/bin/env bash
# Cron Supervisor daemon loop — keeps the agent running 24/7

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

while true; do
  # Spawn agent if no running session with label cron-supervisor
  if ! openclaw sessions list --json 2>/dev/null | grep -q '"label":"cron-supervisor"'; then
    echo "[$(TZ=Asia/Bangkok date +'%Y-%m-%d %H:%M')] Starting cron-supervisor..."
    openclaw agents spawn \
      --agentId cron-supervisor \
      --label cron-supervisor \
      --task "Cron job monitoring and health reporting" \
      --thinking "low" \
      --timeoutSeconds 3600 \
      --runTimeoutSeconds 0 \
      --cleanup keep
  fi
  sleep 30
done
