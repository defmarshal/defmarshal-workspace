#!/bin/bash
# Heartbeat for def – sends a formatted check‑in to Telegram

cd /home/ubuntu/.openclaw/workspace

# Time formatting
NOW_UTC=$(date -u +"%H:%M")
DATE_STR=$(date -u +"%b %d, %Y")

# Start building message
MSG="🟢 Heartbeat Check ($NOW_UTC UTC, $DATE_STR)\n"

# Gateway status
if openclaw gateway status >/dev/null 2>&1; then
  MSG+="✅ Gateway running\n"
else
  MSG+="❌ Gateway down\n"
fi

# Disk usage
DISK_USED=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
DISK_FREE=$(df -h / | awk 'NR==2 {print $4}')
MSG+="💾 Disk ${DISK_USED} full (${DISK_FREE} free)\n"

# Updates
UPDATES=$(apt list --upgradable 2>/dev/null | wc -l)
if [ "$UPDATES" -gt 0 ]; then
  MSG+="⚠️ Updates: $UPDATES pending\n"
else
  MSG+="✅ Updates: 0 pending\n"
fi

# Git changes (in workspace)
GIT_CHANGES=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$GIT_CHANGES" -gt 0 ]; then
  MSG+="✅ Git: $GIT_CHANGES changes\n"
else
  MSG+="✅ Git: clean\n"
fi

# Agents status (quick check)
AGENT_COUNT=$(openclaw agents list 2>/dev/null | grep -c "status.*online" || echo "0")
if [ "$AGENT_COUNT" -gt 0 ]; then
  MSG+="✅ Agents: $AGENT_COUNT online\n"
else
  MSG+="✅ Agents: idle\n"
fi

# Nearest holiday
NEAREST_HOLIDAY=$(quick holidays 2>/dev/null | head -1 | sed 's/^/🎉 /')
if [ -n "$NEAREST_HOLIDAY" ]; then
  MSG+="$NEAREST_HOLIDAY\n"
fi

MSG+="\nAll clear! (◕‿◕)♡"

# Send to Telegram via OpenClaw
echo -e "$MSG" | openclaw message send --channel telegram --target 952170974 --message "$(cat)" 2>/dev/null || echo "Failed to send heartbeat"
