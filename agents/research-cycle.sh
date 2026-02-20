#!/bin/bash
# Research Agent - One Cycle (with retry)
# This script performs a single research-agent cycle with retry on transient errors.

LOGFILE="/home/ubuntu/.openclaw/workspace/research-agent.log"

echo "$(date -u) - Starting research-agent cycle" >> "$LOGFILE"

MAX_RETRIES=3
INITIAL_DELAY=30  # seconds

attempt=1
while [ $attempt -le $MAX_RETRIES ]; do
  echo "$(date -u) - Attempt $attempt/$MAX_RETRIES" >> "$LOGFILE"

  # Run the agent and capture output
  output=$(openclaw agent \
    --agent main \
    --message "You are the research-agent. Conduct continuous research on anime, banking, tech, AI. Use web_search, web_fetch, memory tools. Create detailed reports in /home/ubuntu/.openclaw/workspace/research/. After completing, output a brief summary." \
    --thinking low \
    --timeout 900000 2>&1)

  exit_code=$?
  echo "$output" >> "$LOGFILE"

  # Check for transient auth/rate-limit errors
  if echo "$output" | grep -qi "No available auth profile\|rate limit\|cooldown\|unavailable"; then
    if [ $attempt -lt $MAX_RETRIES ]; then
      delay=$((INITIAL_DELAY * (2 ** (attempt - 1))))
      echo "$(date -u) - Transient error detected, retrying in ${delay}s..." >> "$LOGFILE"
      sleep $delay
      attempt=$((attempt + 1))
      continue
    else
      echo "$(date -u) - Max retries reached, giving up." >> "$LOGFILE"
      exit 1
    fi
  fi

  # If we got here, the agent finished (success or non-retryable error)
  break
done

echo "$(date -u) - Research-agent cycle completed (exit $exit_code)" >> "$LOGFILE"
exit $exit_code
