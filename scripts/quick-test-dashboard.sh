#!/usr/bin/env bash
# Test dashboard data availability and schema
# Usage: quick test-dashboard

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
DATA="$WORKSPACE/apps/dashboard/data.json"

if [ ! -f "$DATA" ]; then
  echo "❌ data.json not found at $DATA"
  exit 1
fi

echo "✅ data.json exists"
echo "📊 Content:"
jq '{gateway, disk_percent, agents: (.agents | length), research: .research.total, commits: (.recent_commits | length)}' "$DATA" 2>/dev/null || {
  echo "❌ Invalid JSON"
  exit 1
}

echo "🔗 Live endpoint check:"
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://openclaw-dashboard-delta.vercel.app/data.json || echo "❌ curl failed"

echo "✅ Dashboard data test passed"
