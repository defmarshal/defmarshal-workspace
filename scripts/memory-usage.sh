#!/usr/bin/env bash
set -euo pipefail
# Show system memory and disk usage

echo "System Memory & Disk Usage"
echo "--------------------------"

# RAM usage (Linux)
if command -v free &>/dev/null; then
  free -h | awk '/^Mem:/ {print "RAM: " $3 "/" $2 " (" $7 " free)"}'
else
  echo "RAM: (free command not available)"
fi

# Swap usage
if command -v free &>/dev/null; then
  free -h | awk '/^Swap:/ {print "Swap: " $3 "/" $2 " (" $7 " free)"}'
fi

# Disk usage for workspace
WORKSPACE="/home/ubuntu/.openclaw/workspace"
echo "Workspace disk: $(df -h "$WORKSPACE" | awk 'NR==2 {print $5 " used (" $3 "/" $2 ")"}')"

# Top 3 largest directories in workspace
echo
echo "Top 3 workspace dirs by size:"
du -sh "$WORKSPACE"/* 2>/dev/null | sort -hr | head -3 | sed 's/^/  /'
