#!/bin/bash
# Quick shortcut for nyaa-top with typical filters: limit 20, max-size 1G
# Usage: qnt [N]
#   qnt            # show top 20 torrents under 1GB
#   qnt 3          # pick #3 from that list (shows magnet)
#   qnt 3 --add    # pick #3 and add to aria2

WORKSPACE="/home/ubuntu/.openclaw/workspace"

# Default args
ARGS="-limit 20 --max-size 1G"

# If first arg is a number, treat as --pick
if [[ "$1" =~ ^[0-9]+$ ]]; then
  ARGS="$ARGS --pick $1"
  shift
fi

# Pass remaining args (like --add)
EXTRA_ARGS="$@"

exec "$WORKSPACE/quick" nyaa-top $ARGS $EXTRA_ARGS
