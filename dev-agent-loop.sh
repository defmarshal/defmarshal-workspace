#!/bin/bash
# Dev Agent Loop - runs every 20 minutes
# This script invokes the OpenClaw agent as dev-agent repeatedly.

LOGFILE="/home/ubuntu/.openclaw/workspace/dev-agent.log"

while true; do
  echo "$(date -u) - Starting dev-agent cycle" >> "$LOGFILE"
  # Invoke dev-agent via openclaw CLI with a fresh session each cycle
  openclaw agent \
    --agent main \
    --message "You are the dev-agent. Continuous development of tools, automations, and infrastructure. Scan the workspace for improvements. Implement small utilities, fix deprecations, test, commit with 'dev:' prefix, push to GitHub. Log actions to dev-agent.log. Respect quiet hours (23:00-08:00 Asia/Bangkok). After completing, output a brief summary." \
    --thinking low \
    --timeout 600000 \
    >> "$LOGFILE" 2>&1
  echo "$(date -u) - Dev-agent cycle completed, sleeping 20 minutes" >> "$LOGFILE"
  sleep 1200
done
