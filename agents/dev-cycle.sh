#!/bin/bash
# Dev Agent - One Cycle
# This script performs a single dev-agent cycle and exits.
# Intended to be called by cron job dev-agent-cron.

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOGFILE="$WORKSPACE/memory/dev-agent.log"

echo "$(date -u) - Starting dev-agent cycle" >> "$LOGFILE"
set +e
openclaw agent \
  --agent main \
  --message "You are the dev-agent. Continuous development of tools, automations, and infrastructure. Scan the workspace for improvements. Implement small utilities, fix deprecations, test, commit with 'dev:' prefix, push to GitHub. Log actions to dev-agent.log. Respect quiet hours (23:00-08:00 Asia/Bangkok). After completing, output a brief summary." \
  --thinking low \
  --timeout 600000 \
  >> "$LOGFILE" 2>&1
exit_code=$?
set -e
echo "$(date -u) - Dev-agent cycle exited with code $exit_code" >> "$LOGFILE"
exit $exit_code
