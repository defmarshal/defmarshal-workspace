#!/usr/bin/env bash
# Show files modified today (since midnight UTC)
# Usage: quick today [path]

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
PATH_TO_CHECK="${1:-$WORKSPACE}"

# Since midnight UTC today
SINCE="$(date -u -d 'today 00:00' +%s)"

echo "Files modified since $(date -u -d "@$SINCE" '+%Y-%m-%d %H:%M UTC'):"
find "$PATH_TO_CHECK" -type f ! -path '*/.git/*' -newermt "@$SINCE" 2>/dev/null \
  -exec ls -lh {} \; \
  | awk '{print $6, $7, $8, $9}' \
  | sort
