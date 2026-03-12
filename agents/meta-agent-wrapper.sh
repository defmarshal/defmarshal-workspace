#!/usr/bin/env bash
set -euo pipefail

cd /home/ubuntu/.openclaw/workspace
LOGFILE="memory/meta-agent.log"
META_AGENT_SEND_SUMMARY="${META_AGENT_SEND_SUMMARY:-0}"

# Run the real meta-agent
./agents/meta-agent.sh --once

# If summary requested, send Telegram with recent activities
if [ "$META_AGENT_SEND_SUMMARY" = "1" ]; then
  SUMMARY_LINES=$(tail -20 "$LOGFILE" | grep -E '^\[[0-9-]+ [0-9:]+ UTC\] (Spawning|✅|❌|⚠️|Created|Deleted|Updated)' | tail -5)
  if [ -n "$SUMMARY_LINES" ]; then
    SUMMARY=$(echo "$SUMMARY_LINES" | sed -E 's/^\[[0-9-]+ [0-9:]+ UTC\] //' | paste -sd '; ' -)
    [ ${#SUMMARY} -gt 300 ] && SUMMARY="${SUMMARY:0:297}..."
    /home/ubuntu/.npm-global/bin/openclaw message send --to 952170974 --message "🤖 Meta-agent summary: $SUMMARY" --best-effort || true
  fi
fi
