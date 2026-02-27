#!/usr/bin/env bash
# Check Vercel deployment status for openclaw-dashboard
# Usage: quick vercel-status

set -euo pipefail
URL="https://openclaw-dashboard-delta.vercel.app/data.json"

echo "Checking Vercel dashboard endpoint..."
if curl -s -f "$URL" > /dev/null; then
  echo "✅ HTTP 200 OK"
  if curl -s "$URL" | jq . > /dev/null 2>&1; then
    echo "✅ JSON valid"
    curl -s "$URL" | jq '.system | {gateway, disk_percent, updates, git_clean}' 2>/dev/null || true
  else
    echo "❌ JSON invalid"
  fi
else
  echo "❌ HTTP request failed (${URL})"
  echo "Try: open https://openclaw-dashboard-delta.vercel.app in browser"
fi
