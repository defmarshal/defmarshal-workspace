#!/usr/bin/env bash
# Check for pending system updates
# Usage: quick updates-check

set -euo pipefail

echo "Checking for upgradable packages..."
echo ""

# Update package lists (quick, non-interactive)
sudo apt update -qq

# Count upgradable
mapfile -t packages < <(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)

if [[ "${packages[0]}" -eq 0 ]]; then
  echo "✓ All packages are up to date."
  exit 0
fi

echo "⚠️  ${packages[0]} package(s) can be upgraded:"
echo ""
apt list --upgradable 2>/dev/null | tail -n +2 | sed 's/^/  /'
echo ""
echo "To apply updates, run: quick updates-apply [--dry-run]"
echo "Note: Use --execute to actually perform the upgrade."
