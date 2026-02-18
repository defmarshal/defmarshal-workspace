#!/usr/bin/env bash
# Migrate from separate torrent-bot daemon + cron downloader to unified torrent-manager daemon

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

echo "Starting torrent-system migration..."

# 1. Ensure new script is executable
chmod +x agents/torrent-manager/loop.sh

# 2. Stop old daemon (torrent-bot loop)
echo "Stopping old torrent-bot daemon..."
pkill -f agents/torrent-bot/loop.sh || true
sleep 1

# 3. Start new torrent-manager daemon (background)
echo "Starting torrent-manager daemon..."
nohup agents/torrent-manager/loop.sh >> memory/torrent-manager.log 2>&1 &
sleep 2

# 4. Remove random-torrent-downloader cron job
echo "Removing old cron job..."
openclaw cron remove random-torrent-downloader || true

# 5. Update active-tasks.md (replace entry)
echo "Updating active-tasks.md..."
# Replace the torrent-bot line with torrent-manager (preserving other entries)
sed -i '/^\[daemon\] torrent-bot/c\- [daemon] torrent-manager (running)' active-tasks.md || true

echo "Migration complete."
echo "Verify with: ./quick daemons"
echo "Logs: tail -f memory/torrent-manager.log"
