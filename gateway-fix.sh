#!/bin/bash
# Gateway fix — restore clean gateway operation
# This script stops the gateway service, kills stray processes, and restarts fresh.
# Usage: ./gateway-fix.sh

set -euo pipefail

echo "== Gateway Fix Start =="

# 1. Stop systemd service if it's active
if systemctl --user is-active --quiet openclaw-gateway.service; then
  echo "→ Stopping systemd service..."
  systemctl --user stop openclaw-gateway.service || true
  sleep 1
else
  echo "→ Systemd service not active; skipping stop"
fi

# 2. Kill any stray gateway processes
echo "→ Killing stray gateway processes..."
pkill -f openclaw-gateway || true
sleep 1

# 3. Verify no processes remain (give up after a few tries)
for i in 1 2 3; do
  if pgrep -f openclaw-gateway >/dev/null 2>&1; then
    echo "  ⚠ Some processes still alive, waiting..."
    sleep 1
  else
    break
  fi
done

if pgrep -f openclaw-gateway >/dev/null 2>&1; then
  echo "  ⚠ Processes still present; using SIGKILL"
  pkill -9 -f openclaw-gateway || true
  sleep 1
fi

# 4. Start service fresh
echo "→ Starting gateway service..."
systemctl --user start openclaw-gateway.service

# 5. Wait for service to become active (up to 10s)
echo "→ Waiting for service to become active..."
for i in {1..10}; do
  if systemctl --user is-active --quiet openclaw-gateway.service; then
    echo "✓ Service active after ${i}s"
    break
  fi
  sleep 1
done

if ! systemctl --user is-active --quiet openclaw-gateway.service; then
  echo "✗ Service did not become active. Check logs:"
  echo "  journalctl --user -u openclaw-gateway.service -n 50"
  exit 1
fi

# 6. Verify port is listening
echo "→ Checking port 18789..."
if ss -tuln | grep -q ':18789 '; then
  echo "✓ Port 18789 is listening"
else
  echo "✗ Port 18789 not listening. Service may have started but crashed."
  exit 1
fi

echo "✓ Gateway fix complete. Use 'openclaw gateway probe' to verify RPC."

echo "== Gateway Fix Complete =="
