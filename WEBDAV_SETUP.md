# Obsidian WebDAV Setup — Complete Guide

Connect your iOS Obsidian app directly to the VPS vault via WebDAV (no computer needed).

---

## 📋 **Prerequisites**

- **VPS** with Ubuntu (already have)
- **Domain name** pointing to your VPS (e.g., `yourdomain.com`) OR use the VPS IP directly (less user-friendly on iOS)
- **Ports 80 and 443** open in firewall
- **Vault exists** at `/home/ubuntu/obsidian-vault` (we have this)

---

## 🚀 **Quick Setup (Run All Steps)**

### 1. SSH into your VPS and run:

```bash
cd /home/ubuntu/.openclaw/workspace
./scripts/setup-obsidian-webdav.sh
```

The script will:
- Install nginx-extras, certbot
- Ask for domain/IP, username, password
- Create nginx config
- Obtain SSL certificate (if domain provided)
- Reload nginx

### 2. If something fails or you want to re‑run:

```bash
# Check nginx status
sudo systemctl status nginx

# View logs
sudo tail -f /var/log/nginx/error.log

# Test WebDAV endpoint
curl -u USERNAME https://your-domain/obsidian/README.md
```

---

## 📱 **iOS Obsidian Connection**

1. Open **Obsidian** app on iPhone/iPad
2. Tap **Settings** (gear icon) → **"WebDAV"**
3. Tap **"Add account"**
4. Fill in:
   - **Host:** `your-domain.com` (or VPS IP)
   - **Path:** `/obsidian`
   - **Username:** the one you set in setup script
   - **Password:** the one you set
   - **Use SSL:** ON (recommended)
5. Tap **"Connect"** → should show vault contents
6. Tap **"Open vault"** → it becomes available in Obsidian

---

## 🔐 **Security Notes**

- Basic auth is **simple but not brute‑force proof**. Consider:
  - Using a **strong password**
  - Enabling **fail2ban** on nginx to block brute force attempts
  - Restricting access by IP (if you have static IP)
- For production use, consider **client certificate auth** or a reverse proxy with more advanced auth.

---

## 🧪 **Test from Command Line**

```bash
# List vault contents (should show notes)
curl -u USERNAME https://your-domain/obsidian/ | html2text  # if html2text installed

# Download a file
curl -u USERNAME -O https://your-domain/obsidian/Daily/2026-02-21.md

# Upload a test file
echo "# Test" > test.md
curl -u USERNAME -T test.md https://your-domain/obsidian/test.md
```

---

## 🛠️ **Troubleshooting**

**Problem:** `403 Forbidden` or `401 Unauthorized`
- Check username/password in iOS settings
- Verify password file: `sudo cat /etc/nginx/obsidian.htpasswd`
- Ensure vault is readable by nginx: `sudo -u www-data ls /home/ubuntu/obsidian-vault`

**Problem:** SSL certificate error
- If using self‑signed or test cert, you may need to allow insecure connections in Obsidian (Settings → WebDAV → "Allow insecure connections")
- Better: use Let's Encrypt (script should have done this if domain provided)

**Problem:** Changes not appearing on iOS
- WebDAV is stateful; try pulling down to refresh in Obsidian
- Check if nginx is proxying correctly: `sudo nginx -t`
- Look at nginx logs: `sudo tail -f /var/log/nginx/access.log`

**Problem:** Upload fails (405 Method Not Allowed)
- Ensure `dav_methods` includes PUT in nginx config
- Verify nginx-extras is installed (not nginx-light)

---

## 🔄 **Keep Vault Updated**

Continue running `quick obsidian-sync` on the VPS to update the vault with OpenClaw research. WebDAV serves the latest files instantly.

If you edit notes on iOS, they **write directly to the VPS** via WebDAV. No separate sync needed!

---

## 📂 **Folder Structure on iOS**

When you connect via WebDAV, Obsidian will show the exact same structure as on the VPS:

```
/obsidian/
├── Daily/
│   └── 2026-02-21.md
├── Research/
│   └── 2026-02/
│       └── ...
├── Dashboards/
│   └── Overview.md
└── ...
```

---

## 🎯 **That's It!**

Once WebDAV is set up and configured in iOS Obsidian, you have **direct read/write access** to your VPS vault from your phone. No computer, no extra sync services, just your VPS serving the files.

**Cost:** $0 (just your existing VPS)

---

**Run the setup script now?** I can execute it on your VPS if you provide:
- Domain or IP address
- Desired username
- Password

Or you can run it yourself; just let me know if you hit any issues. (◕‿◕)♡
