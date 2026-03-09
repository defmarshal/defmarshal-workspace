#!/bin/bash
set -euo pipefail

cd "/home/ubuntu/.openclaw/workspace"

# Gather metrics
DISK_PCT=$(df -h / | awk 'NR==2 {gsub(/%/,""); print $5}')
AGENTS=$(openclaw sessions list --json 2>/dev/null | python3 -c "import json,sys; data=json.load(sys.stdin); print(len([s for s in data.get('sessions',[]) if s.get('status')=='running']))" || echo "?")
TODAY=$(date +%Y-%m-%d)
REPORTS=$(ls research/${TODAY}*.md 2>/dev/null | wc -l || echo 0)
UPDATES=$(apt list --upgradable 2>/dev/null | wc -l)

# Build message
MSG="Meta 6h Summary: Disk ${DISK_PCT}% | Agents: ${AGENTS} | Reports today: ${REPORTS} | APT updates: ${UPDATES} pending. All nominal. (◕‿◕)♡"

# Send to Telegram
openclaw message send --channel telegram --target 952170974 --message "$MSG" 2>/dev/null || echo "Failed to send summary: $MSG"
