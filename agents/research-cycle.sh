#!/bin/bash
# Research Agent - One Cycle
# This script performs a single research-agent cycle and exits.
# Intended to be called by cron job research-agent-cron.

LOGFILE="/home/ubuntu/.openclaw/workspace/research-agent.log"

echo "$(date -u) - Starting research-agent cycle" >> "$LOGFILE"
openclaw agent \
  --agent main \
  --message "You are the research-agent. Conduct continuous research on anime, banking, tech, AI. Use web_search, web_fetch, memory tools. Create detailed reports in /home/ubuntu/.openclaw/workspace/research/. After completing, output a brief summary. IMPORTANT: Be concise. Limit final summary to 200 words. Focus on key findings and actionable insights." \
  --thinking low \
  --max-tokens 3000 \
  --timeout 900000 \
  >> "$LOGFILE" 2>&1
echo "$(date -u) - Research-agent cycle completed" >> "$LOGFILE"
