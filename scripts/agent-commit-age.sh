#!/usr/bin/env bash
# Show age of most recent commits by agent prefix (dev:, research:, content:, etc.)

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "Agent Commit Age (last commit per prefix)"
echo "----------------------------------------"

# Get recent commits (last 100) with hash, author date, and subject
# Format: %h %ad %s
mapfile -t lines < <(git -C "$WORKSPACE" log --oneline -100 2>/dev/null)

declare -A latest

for line in "${lines[@]}"; do
  # Split: hash is first word, rest is subject
  hash=$(echo "$line" | awk '{print $1}')
  subject=$(echo "$line" | cut -d' ' -f2-)
  # Extract prefix from subject (e.g., "dev:", "research:", "content:")
  if echo "$subject" | grep -qE '^(dev|research|content|linkedin|meta|supervisor|agent-manager|idea|builder):'; then
    prefix=$(echo "$subject" | awk '{print $1}' | sed 's/://')
    # Only keep the first (most recent) occurrence of each prefix
    if [ -z "${latest[$prefix]}" ]; then
      latest[$prefix]="$hash $line"
    fi
  fi
done

# Print results
for prefix in dev research content linkedin meta supervisor agent-manager idea builder; do
  if [ -n "${latest[$prefix]}" ]; then
    IFS=' ' read -r hash full_line <<< "${latest[$prefix]}"
    # Extract age and subject from full_line: hash is first, then rest
    rest=$(echo "$full_line" | cut -d' ' -f2-)
    printf "%-12s %s (%s)\n" "$prefix:" "$rest" "$hash"
  else
    printf "%-12s No recent commit\n" "$prefix:"
  fi
done

echo
echo "Note: Based on last 100 commits. If an agent hasn't committed recently, it may be idle or cycles are producing no new content."
