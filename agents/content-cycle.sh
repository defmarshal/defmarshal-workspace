#!/bin/bash
# Content Agent - One Cycle
# This script performs a single content-agent cycle and exits.
# Intended to be called by cron job content-agent-cron.

LOGFILE="/home/ubuntu/.openclaw/workspace/content-agent.log"

echo "$(date -u) - Starting content-agent cycle" >> "$LOGFILE"
openclaw agent \
  --agent main \
  --message "You are the content-agent. Create anime summaries, tech writeups, or daily digests. Check for pending tasks. If none, generate a short daily digest. Log outputs to /home/ubuntu/.openclaw/workspace/content/. After completing, output a brief summary." \
  --thinking low \
  --timeout 600000 \
  >> "$LOGFILE" 2>&1
echo "$(date -u) - Content-agent cycle completed" >> "$LOGFILE"
