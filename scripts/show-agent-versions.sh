#!/usr/bin/env bash
# Show agent script versions (from Git history or script header)

WORKSPACE="/home/ubuntu/.openclaw/workspace"
AGENTS_DIR="$WORKSPACE/agents"

echo "Agent Versions (latest Git commit per script)"
echo "---------------------------------------------"

for agent in "$AGENTS_DIR"/*.sh; do
  [ -f "$agent" ] || continue
  name=$(basename "$agent" .sh)
  # Get latest Git commit that modified this file
  commit_info=$(git -C "$WORKSPACE" log -1 --pretty=format:"%h %s" -- "$agent" 2>/dev/null)
  if [ -n "$commit_info" ]; then
    # Extract version tag if present (e.g., "v10", "v9") from commit message
    version=$(echo "$commit_info" | grep -oE ' v[0-9]+' | head -1 | tr -d ' ')
    if [ -n "$version" ]; then
      printf "%-25s %s (%s)\n" "$name:" "$version" "$commit_info"
    else
      printf "%-25s %s\n" "$name:" "$commit_info"
    fi
  else
    echo "$name: (untracked or no commits)"
  fi
done
