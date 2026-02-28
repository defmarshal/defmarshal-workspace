#!/usr/bin/env bash
# Research Agent - One Cycle (with retry + auto TTS)
# This script performs a single research-agent cycle with retry on transient errors,
# then generates TTS audio for any new research reports.

LOGFILE="/home/ubuntu/.openclaw/workspace/research-agent.log"
WORKSPACE="/home/ubuntu/.openclaw/workspace"
TTS_SCRIPT="$WORKSPACE/scripts/tts-research.sh"

echo "$(date -u) - Starting research-agent cycle" >> "$LOGFILE"

MAX_RETRIES=3
INITIAL_DELAY=30

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

  break
done

echo "$(date -u) - Research-agent cycle completed (exit $exit_code)" >> "$LOGFILE"

# Generate TTS for any new reports (those without existing .mp3)
if [ -f "$TTS_SCRIPT" ]; then
  echo "$(date -u) - Starting TTS generation for new reports" >> "$LOGFILE"
  # Find all research markdown files that don't have a corresponding MP3
  new_count=0
  for md in research/*.md; do
    [ -f "$md" ] || continue
    mp3="${md%.md}.mp3"
    if [ ! -f "$mp3" ]; then
      new_count=$((new_count+1))
      echo "$(date -u) - Generating TTS for: $(basename "$md")" >> "$LOGFILE"
      "$TTS_SCRIPT" "$md" >> "$LOGFILE" 2>&1 || echo "$(date -u) - TTS failed for: $(basename "$md")" >> "$LOGFILE"
      # Small delay to avoid rate limiting
      sleep 5
    fi
  done
  echo "$(date -u) - TTS generation complete (processed $new_count new reports)" >> "$LOGFILE"

  # Auto-deploy Research Hub if new audio was generated
  if [ $new_count -gt 0 ]; then
    echo "$(date -u) - New reports detected, deploying Research Hub..." >> "$LOGFILE"
    if [ -x "$WORKSPACE/scripts/deploy-research-hub.sh" ]; then
      "$WORKSPACE/scripts/deploy-research-hub.sh" >> "$LOGFILE" 2>&1 || echo "$(date -u) - Deploy failed (continuing)" >> "$LOGFILE"
    else
      echo "$(date -u) - deploy-research-hub.sh not found, skipping deploy" >> "$LOGFILE"
    fi

    # Note: Auto‑tweet is handled by Zapier via RSS feed (https://research-hub-flame.vercel.app/feed)
    # No need to run tweet script locally.
  else
    echo "$(date -u) - No new reports, skipping deploy" >> "$LOGFILE"
  fi
else
  echo "$(date -u) - TTS script not found at $TTS_SCRIPT, skipping audio generation and deploy" >> "$LOGFILE"
fi

exit $exit_code
