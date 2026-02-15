#!/usr/bin/env bash
# Setup passwordless sudo for OpenClaw agent
# Run: sudo ./setup-sudo.sh

set -euo pipefail

USER="${SUDO_USER:-$(whoami)}"
BACKUP_DIR="/etc/sudoers.backup"
TIMESTAMP=$(date +%F-%H%M%S)

echo "Setting up passwordless sudo for user: $USER"
echo "This will add a NOPASSWD entry to /etc/sudoers.d/"

# Confirm
read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Aborted."
  exit 1
fi

# Backup existing sudoers files
echo "Backing up sudoers..."
sudo cp /etc/sudoers "${BACKUP_DIR}/sudoers.${TIMESTAMP}" 2>/dev/null || true
sudo cp -r /etc/sudoers.d "${BACKUP_DIR}/sudoers.d.${TIMESTAMP}" 2>/dev/null || true

# Create sudoers.d drop-in
CONF_FILE="/etc/sudoers.d/99-openclaw-nopasswd"
echo "Creating ${CONF_FILE}..."
sudo tee "$CONF_FILE" > /dev/null <<EOF
# OpenClaw agent passwordless sudo (added $(date))
${USER} ALL=(ALL) NOPASSWD: ALL
EOF

# Set proper permissions
sudo chmod 440 "$CONF_FILE"

# Validate syntax
echo "Validating sudoers syntax..."
sudo visudo -c
if [ $? -eq 0 ]; then
  echo "✓ Sudoers syntax OK"
else
  echo "✗ Syntax error! Rolling back..."
  sudo rm -f "$CONF_FILE"
  exit 1
fi

# Test
echo "Testing passwordless sudo..."
if sudo -l >/dev/null 2>&1; then
  echo "✓ Passwordless sudo working for $USER!"
else
  echo "✗ Test failed. You may still need to enter password."
  exit 1
fi

echo "Setup complete! You can now use 'elevated: true' in OpenClaw exec commands."
