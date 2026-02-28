#!/usr/bin/env bash
set -euo pipefail
# Show latest commit per agent prefix (dev:, research:, content:, etc.)

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

echo "Latest Commit by Agent Prefix"
echo "---------------------------"

# Define prefixes to track
prefixes=("dev" "research" "content" "linkedin" "meta" "supervisor" "agent-manager" "idea" "builder")

for prefix in "${prefixes[@]}"; do
  # Get most recent commit with this prefix
  commit=$(git log --oneline --grep="^$prefix:" -1 2>/dev/null)
  if [ -n "$commit" ]; then
    hash=$(echo "$commit" | awk '{print $1}')
    msg=$(echo "$commit" | cut -d' ' -f2-)
    echo "$prefix: $hash — $msg"
  else
    echo "$prefix: No recent commit"
  fi
done
