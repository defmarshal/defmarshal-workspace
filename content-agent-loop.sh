#!/bin/bash
# Content Agent Loop - runs every 10 minutes
# Invokes content-agent via OpenClaw in isolated session.

LOGFILE="/home/ubuntu/.openclaw/workspace/content-agent.log"

while true; do
  # Quiet hours check: skip if 23:00-08:00 Bangkok
  HOUR=$(TZ='Asia/Bangkok' date +%H)
  if (( HOUR >= 23 || HOUR < 8 )); then
    sleep 1800
    continue
  fi

  echo "$(date -u) - Starting content-agent cycle" >> "$LOGFILE"
  openclaw agent \
    --agent main \
    --message "You are the content-agent. Create anime summaries, tech writeups, or daily digests. Check for pending tasks. If none, generate a short daily digest. Log outputs to /home/ubuntu/.openclaw/workspace/content/. After completing, output a brief summary." \
    --thinking low \
    --timeout 600000 \
    >> "$LOGFILE" 2>&1
  echo "$(date -u) - Content-agent cycle completed, sleeping 10 minutes" >> "$LOGFILE"
  sleep 600
done
