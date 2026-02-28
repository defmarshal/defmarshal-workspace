#!/usr/bin/env bash
# Show top committers/prefixes by commit count
# Usage: quick top-commits [N]

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

N="${1:-10}"
SINCE="${2:-1 month ago}"

echo "╔══════════════════════════════════════════════╗"
echo "║     Top Commits by Prefix — Last Month       ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Count commits by prefix (first word before colon)
git log --oneline --since="$SINCE" --format="%s" 2>/dev/null \
  | grep -oP '^[a-z][a-z-]*(?=[:!])' \
  | sort | uniq -c | sort -rn \
  | head -n "$N" \
  | awk '{printf "  %-6s  %s\n", $1, $2}'

echo ""
TOTAL=$(git log --oneline --since="$SINCE" | wc -l)
echo "  Total commits in last month: $TOTAL"
echo ""

# Today's commits
TODAY=$(git log --oneline --since="midnight" | wc -l)
echo "  Today's commits: $TODAY"
git log --oneline --since="midnight" | head -8 | sed 's/^/    /'
