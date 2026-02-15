#!/usr/bin/env bash
# Test passwordless sudo configuration for OpenClaw
# Usage: ./sudo-test.sh

set -euo pipefail

echo "Testing passwordless sudo..."

# Test 1: Can we run sudo without password?
if sudo -n true 2>/dev/null; then
  echo "✓ sudo true succeeded (no password needed)"
else
  echo "✗ sudo true failed (password required or NOPASSWD not set)"
  exit 1
fi

# Test 2: List sudo privileges
echo "Your sudo privileges:"
sudo -l

# Test 3: Run a harmless elevated command
echo "Running elevated command: apt list --upgradable (count only)"
sudo apt list --upgradable 2>/dev/null | wc -l

echo "All tests passed! You can use 'elevated: true' in OpenClaw exec commands."
