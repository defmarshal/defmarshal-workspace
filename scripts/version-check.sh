#!/usr/bin/env bash
set -euo pipefail
# Check OpenClaw version against latest npm release

WORKSPACE="/home/ubuntu/.openclaw/workspace"

# Get installed version
if command -v openclaw &>/dev/null; then
  INSTALLED=$(openclaw --version 2>&1 | head -1 || echo "unknown")
else
  echo "OpenClaw CLI not found in PATH"
  exit 1
fi

# Get latest version from npm (using npm view; may be slow)
echo "Checking latest version on npm..."
LATEST=$(npm view openclaw version 2>/dev/null || echo "unavailable")

echo "OpenClaw Version Check"
echo "---------------------"
echo "Installed: $INSTALLED"
echo "Latest (npm): $LATEST"

if [ "$LATEST" != "unavailable" ] && [ "$INSTALLED" != "unknown" ]; then
  # Extract version numbers (strip any prefixes)
  INST_VER=$(echo "$INSTALLED" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
  LAT_VER=$(echo "$LATEST" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
  if [ -n "$INST_VER" ] && [ -n "$LAT_VER" ]; then
    if [ "$INST_VER" = "$LAT_VER" ]; then
      echo "Status: ✅ Up to date"
    else
      echo "Status: ⚠️ Update available ($LAT_VER)"
    fi
  else
    echo "Status: ? Could not parse versions"
  fi
else
  echo "Status: ? Could not determine latest"
fi
