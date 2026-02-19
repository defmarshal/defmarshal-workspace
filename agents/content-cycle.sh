#!/bin/bash
# Content Agent - One Cycle (with retry)
# This script performs a single content-agent cycle with retry on transient errors.

LOGFILE="/home/ubuntu/.openclaw/workspace/content-agent.log"

MAX_RETRIES=3
INITIAL_DELAY=30  # seconds

echo "$(date -u) - Starting content-agent cycle" >> "$LOGFILE"

attempt=1
while [ $attempt -le $MAX_RETRIES ]; do
  echo "$(date -u) - Attempt $attempt/$MAX_RETRIES" >> "$LOGFILE"
  
  # Run the agent and capture output
  output=$(openclaw agent \
    --agent main \
    --message "You are the content-agent. Create anime summaries, tech writeups, or daily digests. Check for pending tasks. If none, generate a short daily digest. Log outputs to /home/ubuntu/.openclaw/workspace/content/. After completing, output a brief summary." \
    --thinking low \
    --timeout 600000 2>&1)
  
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

echo "$(date -u) - Content-agent cycle completed (exit $exit_code)" >> "$LOGFILE"
exit $exit_code
