#!/bin/bash
# Quick disk space check for training runs
# Alerts if free space < 3GB

FREE=$(df --output=avail /home/ubuntu/.openclaw/workspace | tail -n1)
FREE_GB=$((FREE / 1024 / 1024))

echo "Free space in workspace: ${FREE_GB} GB"

if [ $FREE_GB -lt 3 ]; then
    echo "⚠️  WARNING: Low disk space (<3GB). Consider cleanup:"
    echo "  ./quick cleanup-downloads --execute"
    echo "  ./quick cleanup-archived --execute"
    echo "  ./quick cleanup-build-archive --execute"
    exit 1
fi

exit 0
