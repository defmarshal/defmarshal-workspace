#!/usr/bin/env bash
# today-summary.sh — one-liner production summary for today UTC
# Shows: research reports, content pieces, dev commits, disk
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

TODAY=$(date -u +%Y-%m-%d)

research_count=$(ls research/${TODAY}*.md 2>/dev/null | grep -v INDEX | wc -l)
content_count=$(ls content/${TODAY}*.md 2>/dev/null | wc -l)
dev_commits=$(git log --oneline --since="${TODAY}T00:00:00Z" --format="%s" 2>/dev/null | grep -c "^dev:" || true)
disk_pct=$(df / | awk 'NR==2{print $5}')
total_research=$(grep "^## 2026 Reports" research/INDEX.md 2>/dev/null | grep -oE '\(([0-9]+) total\)' | grep -oE '[0-9]+' | head -1 || echo "?")

echo "📊 Today (${TODAY} UTC): ${research_count} research reports | ${content_count} content pieces | ${dev_commits} dev commits | disk ${disk_pct} | archive: ${total_research} total"
