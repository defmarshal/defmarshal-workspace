#!/usr/bin/env bash
# Gateway Info & Remote Setup Helper
set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"
echo "== OpenClaw Gateway Status =="
if systemctl --user is-active openclaw-gateway.service >/dev/null 2>&1; then
  echo "Status: active"
else
  echo "Status: not running"
fi
PORT=18789
echo "Local URL: http://localhost:$PORT"
if [ -f "$HOME/.openclaw/config.yaml" ]; then
  REMOTE_URL=$(grep -A2 'remote:' "$HOME/.openclaw/config.yaml" | grep 'url:' | sed "s/.*url: *'//;s/'//;s/\"//g" || true)
  [ -n "$REMOTE_URL" ] && echo "Remote URL: $REMOTE_URL" || echo "Remote URL: not set"
else
  echo "Config: $HOME/.openclaw/config.yaml not found"
fi
echo ""
echo "== Remote Access Setup =="
echo "1. Firewall: sudo ufw allow $PORT/tcp"
echo "2. In config.yaml set: gateway.remote.url: \"http://your-ip:$PORT\""
echo "3. Restart: systemctl --user restart openclaw-gateway"
echo "4. Then access: http://your-ip:$PORT"
echo "⚠️  Use HTTPS proxy + auth for internet-facing."
