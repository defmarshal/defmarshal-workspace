#!/usr/bin/env bash
# Check that today's daily digest is up-to-date with actual content

WORKSPACE="/home/ubuntu/.openclaw/workspace"
CONTENT_DIR="$WORKSPACE/content"
DATE=$(date -u +%Y-%m-%d)
DIGEST="$CONTENT_DIR/$DATE-daily-digest.md"

echo "Daily Digest Consistency Check"
echo "-----------------------------"

if [ ! -f "$DIGEST" ]; then
  echo "❌ Digest file not found: $DIGEST"
  exit 1
fi

# Count LinkedIn PA posts for today in filesystem
ACTUAL_POSTS=$(ls -1 "$CONTENT_DIR/$DATE"*-linkedin-pa-post.md 2>/dev/null | wc -l)

# Extract listed count from digest (look for "LinkedIn PA posts today: N")
LISTED_COUNT=$(grep -E 'LinkedIn PA posts today:' "$DIGEST" | head -1 | grep -oE '[0-9]+' || echo "0")

# Count research reports added today (look for lines like "- **Research library:** 189 reports")
# We'll just check if the research library count in digest matches actual by checking if a new report was added today
RESEARCH_LIB_LINE=$(grep -E 'Research library: [0-9]+ reports' "$DIGEST" | head -1)
if [ -n "$RESEARCH_LIB_LINE" ]; then
  echo "✅ Digest notes research library: $RESEARCH_LIB_LINE"
else
  echo "⚠️  No research library summary found in digest"
fi

echo
echo "LinkedIn PA posts:"
echo "  Actual files:  $ACTUAL_POSTS"
echo "  Listed in digest: $LISTED_COUNT"

if [ "$ACTUAL_POSTS" -eq "$LISTED_COUNT" ]; then
  echo "✅ Digest count matches actual posts."
else
  echo "❌ Mismatch! Digest may be stale."
  echo "   Suggest running: ./quick update-daily-digest (or let content-agent cron handle it)"
fi

# Check if digest was modified recently
DIGEST_MTIME=$(stat -c %Y "$DIGEST" 2>/dev/null)
NOW=$(date +%s)
AGE_MIN=$(( (NOW - DIGEST_MTIME) / 60 ))
if [ $AGE_MIN -lt 60 ]; then
  echo "✅ Digest is fresh (modified $AGE_MIN minutes ago)"
else
  echo "⚠️  Digest is $AGE_MIN minutes old — may need update"
fi
