#!/usr/bin/env bash
set -euo pipefail

cd /home/ubuntu/.openclaw/workspace

LOGFILE="memory/meta-agent.log"
TO_CHAT_ID="952170974"
OPENCLAWSH="${OPENCLAWSH:-/home/ubuntu/.npm-global/bin/openclaw}"

# Ensure log exists
if [ ! -f "$LOGFILE" ]; then
  echo "Meta-agent log not found: $LOGFILE" >&2
  exit 1
fi

# Get last 20 lines, filter for activity markers
SUMMARY_LINES=$(tail -20 "$LOGFILE" | grep -E '^\[[0-9-]+ [0-9:]+ UTC\] (Spawning|✅|❌|⚠️|Created|Deleted|Updated|Error|Triggering)' | tail -5 || true)

if [ -z "$SUMMARY_LINES" ]; then
  echo "No recent meta-agent activity to summarize"
  exit 0
fi

# Strip timestamps, join with semicolons
SUMMARY=$(echo "$SUMMARY_LINES" | sed -E 's/^\[[0-9-]+ [0-9:]+ UTC\] //' | paste -sd '; ' -)

# Truncate to 300 chars for Telegram
if [ ${#SUMMARY} -gt 300 ]; then
  SUMMARY="${SUMMARY:0:297}..."
fi

# Send via openclaw
MESSAGE="🤖 Meta-agent summary: $SUMMARY"
"$OPENCLAWSH" message send --to "$TO_CHAT_ID" --message "$MESSAGE" --best-effort && echo "Summary sent" || echo "Failed to send summary" >&2
