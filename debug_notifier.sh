#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace
echo "Test start $(date -u)"
echo "Running cron list..."
timeout 15 openclaw cron list --json > /dev/null && echo "cron list done"
echo "Running gateway status..."
timeout 15 openclaw gateway status > /dev/null && echo "gateway done"
echo "Test end $(date -u)"