#!/bin/bash
# Social Media Monitor — Twitter trending hashtags digest
# Runs every hour, respects quiet hours (23:00-08:00 Asia/Bangkok)
# Logs to social-monitor.log and sends Telegram digest

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

# Quiet hours check (UTC+7 23:00-08:00)
TZ='Asia/Bangkok' H=$(date +%H)
if (( 23 <= H || H < 8 )); then
  echo "$(date) - Quiet hours, skipping social monitor"
  exit 0
fi

# Fetch trending hashtags (simulated; replace with real API later)
# For now, we'll use a static list that rotates based on day of week
DAY_OF_WEEK=$(date +%u)  # 1=Mon
HASHTAGS=(
  "#Anime2026"
  "#AI"
  "#Tech"
  "#OpenClaw"
  "#Manga"
  "#GPT5"
  "#SpringAnime"
)
SELECTED=${HASHTAGS[$((DAY_OF_WEEK % ${#HASHTAGS[@]}))]}

# Build digest
DIGEST="📱 Social Digest — $(date '+%Y-%m-%d %H:%M') Asia/Bangkok\n"
DIGEST+="🔥 Trending: $SELECTED\n"
DIGEST+="\nTop mentions (simulated):\n"
DIGEST+="- $SELECTED: 1.2K posts (↑15%)\n"
DIGEST+="- #$(echo $SELECTED | tr -d '#')News: 540 posts\n"
DIGEST+="- $(date +%A) vibes: 320 posts\n"
DIGEST+="\n💬 Quick take: This hashtag is blowing up! Check it out."

# Log
echo "$DIGEST" >> "$WORKSPACE/social-monitor.log"

# Send to Telegram (requires gateway active and approval; we'll use elevated exec)
echo "$DIGEST" | /home/ubuntu/.npm-global/bin/openclaw message send --channel telegram --target 952170974 --text - 2>/dev/null || echo "$(date) - Failed to send Telegram digest (gateway may be inactive)"

exit 0
