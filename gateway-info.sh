#!/usr/bin/env bash
# Gateway Info & Remote Setup Helper
# Uses openclaw gateway status --json for accurate data.
set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

echo "== OpenClaw Gateway Status =="

STATUS_JSON=$(openclaw gateway status --json 2>/dev/null) || STATUS_JSON=""

if [ -z "$STATUS_JSON" ]; then
  echo "Status: unavailable (cannot get gateway status)"
else
  # Parse with jq (should be installed)
  if command -v jq >/dev/null 2>&1; then
    SERVICE_STATUS=$(echo "$STATUS_JSON" | jq -r '.service.runtime.state // "unknown"')
    echo "Service: $SERVICE_STATUS"
    PORT=$(echo "$STATUS_JSON" | jq -r '.gateway.port // 18789')
    BIND_HOST=$(echo "$STATUS_JSON" | jq -r '.gateway.bindHost // "127.0.0.1"')
    echo "Bind: $BIND_HOST"
    echo "Local URL: http://$BIND_HOST:$PORT"
    REMOTE_URL=$(echo "$STATUS_JSON" | jq -r '.gateway.remoteUrl // empty')
    if [ -n "$REMOTE_URL" ] && [ "$REMOTE_URL" != "null" ]; then
      echo "Remote URL: $REMOTE_URL"
    else
      echo "Remote URL: not set"
    fi
    RPC_OK=$(echo "$STATUS_JSON" | jq -r '.rpc.ok // false')
    if [ "$RPC_OK" = "true" ]; then
      echo "RPC: reachable"
    else
      echo "RPC: unreachable"
    fi
  else
    echo "jq not available; raw JSON:"
    echo "$STATUS_JSON" | python3 -m json.tool 2>/dev/null || echo "$STATUS_JSON"
  fi
fi

echo ""
echo "== Remote Access Setup =="
echo "1. Ensure firewall allows port 18789 (sudo ufw allow 18789/tcp)"
echo "2. Set gateway.remote.url in your config to your public URL (e.g. https://your-ip:18789)"
echo "3. Restart: openclaw gateway restart"
echo "4. For internet-facing, use HTTPS proxy + authentication."
echo "5. For remote clients, set gateway.remote.url and ensure reachable."
