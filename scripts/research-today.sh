#!/usr/bin/env bash
# research-today.sh — list today's research reports with titles and sizes
# Usage: scripts/research-today.sh [YYYY-MM-DD]
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

DATE="${1:-$(date -u +%Y-%m-%d)}"
COUNT=0

echo "Research reports for ${DATE}:"
echo ""
for f in research/${DATE}*.md; do
  [[ -f "$f" ]] || { echo "  (none)"; exit 0; }
  [[ "$(basename "$f")" == "INDEX.md" ]] && continue
  title=$(head -1 "$f" | sed 's/^# //')
  size=$(du -h "$f" | cut -f1)
  COUNT=$((COUNT + 1))
  echo "  ${COUNT}. [${size}] ${title}"
  echo "     → ${f}"
done

echo ""
echo "${COUNT} report(s) on ${DATE}."
