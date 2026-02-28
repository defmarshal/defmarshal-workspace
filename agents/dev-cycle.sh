#!/usr/bin/env bash
# Dev Agent - One Cycle (with retry)
# This script performs a single dev-agent cycle with retry on transient errors.

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOGFILE="$WORKSPACE/memory/dev-agent.log"

echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC") - Starting dev-agent cycle" >> "$LOGFILE"

MAX_RETRIES=3
INITIAL_DELAY=30  # seconds

attempt=1
while [ $attempt -le $MAX_RETRIES ]; do
  echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC") - Attempt $attempt/$MAX_RETRIES" >> "$LOGFILE"

  # Run the agent and capture output
  output=$(openclaw agent \
    --agent main \
    --message "You are the dev-agent. Continuous development of tools, automations, and infrastructure. Scan the workspace for improvements. Implement small utilities, fix deprecations, test, commit with 'dev:' prefix, push to GitHub. Log actions to dev-agent.log. (Quiet hours removed; agents run 24/7.) After completing, output a brief summary." \
    --thinking low \
    --timeout 1200000 2>&1)

  exit_code=$?
  echo "$output" >> "$LOGFILE"

  # Check for transient auth/rate-limit errors
  if echo "$output" | grep -qi "No available auth profile\|rate limit\|cooldown\|unavailable"; then
    if [ $attempt -lt $MAX_RETRIES ]; then
      delay=$((INITIAL_DELAY * (2 ** (attempt - 1))))
      echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC") - Transient error detected, retrying in ${delay}s..." >> "$LOGFILE"
      sleep $delay
      attempt=$((attempt + 1))
      continue
    else
      echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC") - Max retries reached, giving up." >> "$LOGFILE"
      exit 1
    fi
  fi

  # If we got here, the agent finished (success or non-retryable error)
  break
done

echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC") - Dev-agent cycle completed (exit $exit_code)" >> "$LOGFILE"
exit $exit_code
