#!/usr/bin/env bash
# Show distribution of LinkedIn PA content types

WORKSPACE="/home/ubuntu/.openclaw/workspace"
CONTENT_DIR="$WORKSPACE/content"

echo "LinkedIn PA Content Distribution"
echo "--------------------------------"

if ! command -v jq &>/dev/null; then
  echo "⚠️  jq not installed; install with: sudo apt-get install -y jq"
  exit 1
fi

# Count by content type from filenames
# Filename pattern: YYYY-MM-DD-HHMM-linkedin-pa-post.md
# We'll extract the timestamp and map to content type via the agent's log or infer from file count per hour

# Get all LinkedIn PA posts from today and yesterday
POSTS=$(ls -1 "$CONTENT_DIR"/*-linkedin-pa-post.md 2>/dev/null | sort)

if [ -z "$POSTS" ]; then
  echo "No LinkedIn PA posts found."
  exit 0
fi

# Count total
TOTAL=$(echo "$POSTS" | wc -l)
echo "Total posts: $TOTAL"
echo

# Since content type isn't in filename, we can approximate distribution by hour of day
# The agent cycles hourly; we can map hour -> content type from the agent's rotation
# But for a quick utility, we'll just show posts per hour to see cadence

echo "Posts by hour (UTC):"
echo "$POSTS" | sed -n 's/.*-\([0-9]\{4\}\)-linkedin-pa-post\.md/\1/p' | cut -c1-2 | sort | uniq -c | sort -rn | while read -r count hour; do
  printf "%02d:00  %3d posts\n" $((10#$hour)) "$count"
done

echo
echo "For detailed content types, check individual post files or the agent log."
