#!/usr/bin/env bash
# Check for pending system updates (APT). Use --execute to actually apply.
# Default is dry-run with summary.

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

# Check if we're on Ubuntu/Debian
if ! command -v apt-get &>/dev/null; then
  echo "⚠️  APT not found; this script is for Debian/Ubuntu systems."
  exit 0
fi

echo "Checking for pending APT updates..."
UPDATE_COUNT=$(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)

if [ "$UPDATE_COUNT" -eq 0 ]; then
  echo "✅ No pending updates."
  exit 0
fi

echo "⚠️  $UPDATE_COUNT package(s) can be upgraded:"
apt list --upgradable 2>/dev/null | tail -n +2 | head -20 || true
if [ "$UPDATE_COUNT" -gt 20 ]; then
  echo "... and $((UPDATE_COUNT - 20)) more"
fi

if [ "${1:-}" = "--execute" ]; then
  echo
  read -p "Apply all updates now? (yes/no) " CONFIRM
  if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted."
    exit 0
  fi
  echo "Applying updates..."
  sudo apt-get update -y
  sudo apt-get upgrade -y
  echo "Updates applied. Rebooting is not required unless kernel was updated."
else
  echo
  echo "To apply: $WORKSPACE/quick updates-apply --execute"
fi
