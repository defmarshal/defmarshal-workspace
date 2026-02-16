#!/usr/bin/env bash
# Apply system updates (with safety)
# Usage: quick updates-apply [--dry-run|--execute]
# Default: dry-run (shows what would be upgraded)

set -euo pipefail

DRY_RUN=1
if [[ "$1" == "--execute" ]]; then
  DRY_RUN=0
elif [[ "$1" == "--dry-run" ]]; then
  DRY_RUN=1
fi

echo "=== System Update Procedure ==="
echo ""

# Update package lists
echo "→ Updating package index..."
sudo apt update -qq

if (( DRY_RUN )); then
  echo "→ Dry-run mode: showing upgradable packages (no changes will be made)"
  echo ""
  count=$(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)
  if [[ "$count" -eq 0 ]]; then
    echo "✓ All packages up to date."
  else
    echo "Would upgrade $count package(s):"
    apt list --upgradable 2>/dev/null | tail -n +2 | sed 's/^/  /'
  fi
  echo ""
  echo "To actually apply updates, run: quick updates-apply --execute"
else
  echo "→ Applying updates (this may take a while)..."
  echo ""
  sudo apt upgrade -y
  echo ""
  echo "✓ Updates applied. Optionally run: sudo apt autoremove -y"
fi
