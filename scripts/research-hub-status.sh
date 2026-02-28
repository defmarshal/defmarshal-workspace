#!/usr/bin/env bash
set -euo pipefail
# Check Research Hub deployment status (local + remote)

WORKSPACE="/home/ubuntu/.openclaw/workspace"
PUBLIC_DIR="$WORKSPACE/apps/research-hub/public/research"

echo "Research Hub Status"
echo "-------------------"

# 1. Check local public directory exists
if [ -d "$PUBLIC_DIR" ]; then
  echo "✅ Local public directory: $PUBLIC_DIR"
else
  echo "❌ Local public directory missing: $PUBLIC_DIR"
  exit 1
fi

# 2. Count files
REPORTS=$(ls -1 "$PUBLIC_DIR"/*.md 2>/dev/null | grep -v 'INDEX.md' | wc -l)
AUDIO=$(ls -1 "$PUBLIC_DIR"/*.mp3 2>/dev/null | wc -l)
echo "📊 Reports: $REPORTS | Audio files: $AUDIO"

# 3. Check INDEX.md freshness
if [ -f "$PUBLIC_DIR/INDEX.md" ]; then
  INDEX_TIME=$(stat -c %Y "$PUBLIC_DIR/INDEX.md" 2>/dev/null)
  NOW=$(date +%s)
  AGE_H=$(( (NOW - INDEX_TIME) / 3600 ))
  if [ $AGE_H -lt 1 ]; then
    echo "✅ INDEX.md fresh (updated within last hour)"
  else
    echo "⚠️  INDEX.md age: ${AGE_H}h (consider refreshing with: quick research-index-update)"
  fi
else
  echo "❌ INDEX.md not found"
fi

# 4. Check gateway route (if Research Hub is served via gateway)
echo
echo "Checking OpenClaw gateway route for Research Hub..."
if openclaw gateway status >/dev/null 2>&1; then
  echo "✅ Gateway is running"
  # Note: Research Hub is typically served from apps/research-hub/public via the gateway
  echo "  Expected endpoint: https://<host>:18789/apps/research-hub/"
else
  echo "❌ Gateway not responding"
fi

# 5. Suggest next actions
echo
echo "Next steps:"
echo "  - View locally: ls $PUBLIC_DIR"
echo "  - Refresh index: ./quick research-index-update"
echo "  - Check hub: openclaw gateway status"
echo "  - Deploy to Vercel: ./quick research-hub-deploy (if configured)"
