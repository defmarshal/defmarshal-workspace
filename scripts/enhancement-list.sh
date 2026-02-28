#!/usr/bin/env bash
set -euo pipefail
# enhancement-list.sh — show enhancement queue

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

echo "Enhancement Queue:"
echo "------------------"
if ! find enhancements -name '*.json' 2>/dev/null | grep -q .; then
  echo "No proposals."
  exit 0
fi

find enhancements -name '*.json' 2>/dev/null | while read -r f; do
  TITLE=$(jq -r '.title // "?"' "$f" 2>/dev/null || echo "?")
  STATUS=$(jq -r '.status // "?"' "$f" 2>/dev/null || echo "?")
  PRI=$(jq -r '.priority // "?"' "$f" 2>/dev/null || echo "?")
  CREATED=$(jq -r '.created_at // ""' "$f" 2>/dev/null || echo "")
  echo "- $f | status=$STATUS | pri=$PRI | $TITLE ($CREATED)"
done
