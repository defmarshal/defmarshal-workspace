#!/usr/bin/env bash
# Daily Digest Generator — aggregates workspace activity for a given UTC date.
# usage: agents/daily-digest.sh [YYYY-MM-DD] (defaults to today UTC)

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

DATE="${1:-$(date -u +%Y-%m-%d)}"
REPORT_DIR="reports"
mkdir -p "$REPORT_DIR"
REPORT_FILE="${REPORT_DIR}/${DATE}-daily-digest.md"

echo "# Daily Digest ${DATE}" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## Content Produced" >> "$REPORT_FILE"
if ls content/${DATE}*.md >/dev/null 2>&1; then
  for f in content/${DATE}*.md; do
    title="$(head -1 "$f" | sed 's/^# //')"
    echo "- ${f}: ${title}" >> "$REPORT_FILE"
  done
else
  echo "- (none)" >> "$REPORT_FILE"
fi >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "## Research Highlights" >> "$REPORT_FILE"
if ls research/${DATE}*.md >/dev/null 2>&1; then
  for f in research/${DATE}*.md; do
    title="$(head -1 "$f" | sed 's/^# //')"
    echo "- ${f}: ${title}" >> "$REPORT_FILE"
  done
else
  echo "- (none)" >> "$REPORT_FILE"
fi >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "## Dev Commits (today)" >> "$REPORT_FILE"
dev_commits="$(git log --since='1 days ago' --pretty=format:'%s' | grep '^dev:' || true)"
if [ -n "$dev_commits" ]; then
  echo "$dev_commits" | sed 's/^/- /' >> "$REPORT_FILE"
else
  echo "- (none)" >> "$REPORT_FILE"
fi >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "## System Health" >> "$REPORT_FILE"
./quick health >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "## Notes" >> "$REPORT_FILE"
echo "- Generated at $(date -u)" >> "$REPORT_FILE"

# Output to stdout as well
cat "$REPORT_FILE"
