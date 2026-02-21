#!/usr/bin/env bash
# setup-obsidian-webdav.sh — Configure nginx WebDAV for Obsidian vault

set -euo pipefail

echo "=== Obsidian WebDAV Setup ==="
echo ""

# Check if nginx-extras is installed
if ! dpkg -l nginx-extras &>/dev/null; then
  echo "Installing nginx-extras and dependencies..."
  sudo apt update
  sudo apt install -y nginx-extras apache2-utils certbot python3-certbot-nginx
fi

# Read configuration inputs
read -p "Enter your VPS domain or IP address: " SERVER_NAME
read -p "Enter desired WebDAV username (e.g., obsidian): " WEBDAV_USER
read -s -p "Enter password for $WEBDAV_USER: " PASSWORD
echo ""

# Create password file
sudo mkdir -p /etc/nginx
sudo htpasswd -cb /etc/nginx/obsidian.htpasswd "$WEBDAV_USER" "$PASSWORD"
echo "✓ Password created"

# Create web root for Let's Encrypt
sudo mkdir -p /var/www/certbot

# Deploy nginx config
sudo cp "$(pwd)/scripts/nginx-obsidian.conf" /etc/nginx/sites-available/obsidian-webdav
sudo ln -sf /etc/nginx/sites-available/obsidian-webdav /etc/nginx/sites-enabled/obsidian-webdav
sudo rm -f /etc/nginx/sites-enabled/default  # optional: disable default
echo "✓ Nginx config installed"

# Test nginx config
sudo nginx -t
echo "✓ Nginx config valid"

# Get SSL certificate (Let's Encrypt)
echo ""
echo "Setting up HTTPS with Let's Encrypt..."
# Modify config temporarily to use actual server_name
sudo sed -i "s/server_name _;/server_name $SERVER_NAME;/" /etc/nginx/sites-available/obsidian-webdav

# Run certbot
sudo certbot --nginx -d "$SERVER_NAME" --non-interactive --agree-tos -m "${USER}@${SERVER_NAME}" || {
  echo "⚠ Certbot failed. If you don't have a domain, you can use HTTP for testing."
  echo "  Edit /etc/nginx/sites-available/obsidian-webdav and comment out the SSL server block,"
  echo "  then uncomment the HTTP-only server block at the top."
}

# Reload nginx
sudo systemctl reload nginx
echo "✓ Nginx reloaded"

# Print connection details
echo ""
echo "=== WebDAV Ready! ==="
echo "URL (iOS Obsidian): https://$SERVER_NAME/obsidian"
echo "Username: $WEBDAV_USER"
echo "Password: [hidden]"
echo ""
echo "On iOS Obsidian:"
echo "1. Settings → WebDAV"
echo "2. Add account:"
echo "   - Host: $SERVER_NAME"
echo "   - Path: /obsidian"
echo "   - Username: $WEBDAV_USER"
echo "   - Password: the one you entered"
echo "3. Tap 'Connect' and open the vault"
echo ""
echo "Test with: curl -u $WEBDAV_USER https://$SERVER_NAME/obsidian/"
