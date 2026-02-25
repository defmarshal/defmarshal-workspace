#!/usr/bin/env bash
# Show Git commit activity summary by agent prefix

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

DAYS=7

echo "Git Commit Activity (last $DAYS days)"
echo "-------------------------------------"

git log "--since=$DAYS days ago" --oneline 2>/dev/null | while read -r line; do
  # Extract the second word (the prefix like "dev:", "content:", etc.)
  prefix=$(echo "$line" | awk '{print $2}' | sed 's/://')
  # Only count known prefixes
  case "$prefix" in
    dev|research|content|linkedin|meta|supervisor|agent-manager|idea|builder|build)
      echo "$prefix"
      ;;
  esac
done | sort | uniq -c | sort -rn | while read -r count prefix; do
  printf "%-12s %3d commits\n" "$prefix:" "$count"
done

echo
echo "Note: Only includes commits with recognized agent prefixes."
