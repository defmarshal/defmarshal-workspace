#!/bin/bash
# Gateway fix — restore clean gateway operation
# This script force kills any gateway processes, removes identity tokens, restarts service, and waits for RPC readiness.
# Usage: ./gateway-fix.sh

set -euo pipefail

echo "== Gateway Fix Start =="

# 0. Force kill all gateway processes
echo "→ Killing all gateway processes (SIGKILL)..."
pkill -9 -f openclaw-gateway || true
sleep 1

# 1. Remove identity directory (both CLI and gateway tokens)
IDENTITY_DIR="${HOME}/.openclaw/identity"
if [ -d "$IDENTITY_DIR" ]; then
  echo "→ Removing identity directory: $IDENTITY_DIR"
  rm -rf "$IDENTITY_DIR"
else
  echo "→ No identity directory found"
fi

# 2. Stop systemd service if active (ignore errors)
if systemctl --user is-active --quiet openclaw-gateway.service; then
  echo "→ Stopping systemd service..."
  systemctl --user stop openclaw-gateway.service || true
  sleep 1
fi

# 3. Start the gateway service
echo "→ Starting openclaw-gateway service..."
systemctl --user start openclaw-gateway.service

# 4. Wait for port 18789 to be listening
echo "→ Waiting for gateway to listen on port 18789..."
for i in {1..30}; do
  if ss -ltn | grep -q ':18789 '; then
    echo "  ✓ Gateway listening on port 18789"
    break
  else
    sleep 1
  fi
done

# 5. Wait for RPC readiness (openclaw gateway status succeeds)
echo "→ Waiting for RPC to become ready (this may take a few seconds)..."
for i in {1..30}; do
  if openclaw gateway status >/dev/null 2>&1; then
    echo "  ✓ Gateway RPC is ready"
    break
  else
    sleep 1
  fi
done

# 6. Final status
echo "== Gateway Fix Complete =="
echo "Verification:"
openclaw gateway status || echo "  ⚠ Final status check failed"
