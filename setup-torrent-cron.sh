#!/usr/bin/env bash
# Setup automatic torrent downloads via nyaa-top cron
# This script adds a daily cron job to fetch top anime torrents and add to aria2.

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "== Setting up torrent auto-download cron =="

# Define the cron line (runs daily at 02:00 Bangkok time)
CRON_LINE="0 2 * * * TZ='Asia/Bangkok' cd \"$WORKSPACE\" && \"$WORKSPACE/quick\" nyaa-top --limit 10 --max-size 2G --add >> \"$WORKSPACE/memory/auto-torrent.log\" 2>&1"

# Check if already present in crontab
if crontab -l 2>/dev/null | grep -F "nyaa-top.*auto-torrent" > /dev/null; then
  echo "✓ Torrent cron already installed."
else
  # Add to crontab
  (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
  echo "✓ Added torrent cron to crontab."
  echo "  -> Will run daily at 02:00 Asia/Bangkok"
fi

# Update CRON_JOBS.md documentation (append if missing)
if ! grep -q "Auto Torrent Download" "$WORKSPACE/CRON_JOBS.md"; then
  cat >> "$WORKSPACE/CRON_JOBS.md" <<'EOF'

### Auto Torrent Download (System Cron)
- **Schedule**: Daily at 02:00 Asia/Bangkok
- **Command**:
  ```bash
  0 2 * * * TZ='Asia/Bangkok' cd /home/ubuntu/.openclaw/workspace && /home/ubuntu/.openclaw/workspace/quick nyaa-top --limit 10 --max-size 2G --add >> /home/ubuntu/.openclaw/workspace/memory/auto-torrent.log 2>&1
  ```
- **Log**: `memory/auto-torrent.log`
- **Description**: Fetches top 10 anime torrents from Sukebei.Nyaa.si under 2GB and adds them to aria2 automatically.
EOF
  echo "✓ Updated CRON_JOBS.md."
else
  echo "✓ CRON_JOBS.md already contains Auto Torrent Download section."
fi

echo "== Setup complete =="
echo "Next: verify with 'crontab -l' and check 'memory/auto-torrent.log' after next run."
