#!/usr/bin/env bash
set -euo pipefail
# Fix vault permissions for nginx WebDAV

VAULT_DIR="/home/ubuntu/obsidian-vault"
NGINX_USER="www-data"

if [ ! -d "$VAULT_DIR" ]; then
  echo "ERROR: Vault not found at $VAULT_DIR"
  exit 1
fi

echo "Setting permissions on $VAULT_DIR for nginx (user: $NGINX_USER)..."
sudo chown -R "$USER:$NGINX_USER" "$VAULT_DIR"
sudo chmod -R 775 "$VAULT_DIR"
sudo find "$VAULT_DIR" -type d -exec chmod 775 {} \;
sudo find "$VAULT_DIR" -type f -exec chmod 664 {} \;

echo "✓ Permissions set. Nginx can read/write."
echo ""
echo "Test: sudo -u $NGINX_USER test -r $VAULT_DIR/README.md && echo 'nginx can read'"
