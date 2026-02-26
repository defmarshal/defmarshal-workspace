#!/usr/bin/env bash
# enhancement-propose.sh — propose an enhancement to be automated
# Usage: enhancement-propose "Title" "Description" [priority 1-5] [script]

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

if [ $# -lt 3 ]; then
  echo "Usage: $0 \"Title\" \"Description\" priority [script]"
  echo "Example: $0 \"Add dashboard widget\" \"Show recent commits\" 4 scripts/add-dashboard-widget.sh"
  exit 1
fi

TITLE="$1"
DESCRIPTION="$2"
PRIORITY="$3"
SCRIPT="${4:-}"

mkdir -p enhancements

SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '-' | sed 's/^-//;s/-$//')
TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
FILE="enhancements/${SLUG}-${TIMESTAMP}.json"

if [ -z "$SCRIPT" ] || [ ! -f "$SCRIPT" ]; then
  echo "ERROR: Script path required and must exist: $SCRIPT"
  exit 1
fi

jq -n \
  --arg title "$TITLE" \
  --arg desc "$DESCRIPTION" \
  --arg pri "$PRIORITY" \
  --arg script "$SCRIPT" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '{
    title: $title,
    description: $desc,
    priority: ($pri|tonumber),
    script: $script,
    status: "proposed",
    created_at: $ts,
    updated_at: $ts
  }' > "$FILE"

echo "Proposed enhancement: $FILE"
echo "To check status: quick enhancement-list"
