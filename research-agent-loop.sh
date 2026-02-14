#!/bin/bash
# Research Agent Loop - runs every 15 minutes
# Invokes research-agent via OpenClaw in isolated session.

LOGFILE="/home/ubuntu/.openclaw/workspace/research-agent.log"

while true; do
  # Quiet hours check: skip if 23:00-08:00 Bangkok
  HOUR=$(TZ='Asia/Bangkok' date +%H)
  if (( HOUR >= 23 || HOUR < 8 )); then
    sleep 1800
    continue
  fi

  echo "$(date -u) - Starting research-agent cycle" >> "$LOGFILE"
  openclaw agent \
    --agent main \
    --message "You are the research-agent. Conduct continuous research on anime, banking, tech, AI. Use web_search, web_fetch, memory tools. Create detailed reports in /home/ubuntu/.openclaw/workspace/research/. After completing, output a brief summary." \
    --thinking low \
    --timeout 900000 \
    >> "$LOGFILE" 2>&1
  echo "$(date -u) - Research-agent cycle completed, sleeping 15 minutes" >> "$LOGFILE"
  sleep 900
done
