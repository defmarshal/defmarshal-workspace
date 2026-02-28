#!/usr/bin/env bash
set -euo pipefail
# Show disk usage summary of the workspace

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "Workspace Disk Usage (top 10 entries)"
echo "-------------------------------------"
du -sh "$WORKSPACE"/* 2>/dev/null | sort -hr | head -10
echo
echo "Total workspace size:"
du -sh "$WORKSPACE"
