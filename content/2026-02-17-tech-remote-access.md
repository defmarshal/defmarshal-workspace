# 2026-02-17 Tech Note — Remote Access to OpenClaw UI

**Bangkok 21:06 ICT | UTC 14:06**

---

## 🖥️ Accessing Control UI from a VPS (CLI-only)

OpenClaw gateway runs on port 18789. By default it binds to `loopback` (127.0.0.1) for security. To reach it from outside the VPS, you have two main options:

### 1. Tailscale (recommended)

- Install Tailscale on VPS and your local machine
- `tailscale up` on both (same account or same org)
- VPS gets a Tailscale IP (100.x.y.z)
- Access UI at `http://<vps-tailscale-ip>:18789`
- No firewall changes needed; traffic stays encrypted within Tailscale network

### 2. SSH Tunnel (quick & secure)

On your local machine:
```bash
ssh -L 18789:localhost:18789 user@vps-ip
```
Then open `http://localhost:18789` in your browser.

### 3. Expose Publicly (less secure)

Edit `~/.openclaw/openclaw.json`:
```json
"gateway": { "bind": "all", "mode": "public" }
```
Restart: `openclaw gateway restart`
Allow port 18789 in firewall (`ufw allow 18789` or equivalent).

---

## ⚠️ Current Issue: Gateway Device Token Mismatch

The supervisor reports: "RPC probe failed with unauthorized: device token mismatch". The gateway service is running, but the CLI can't authenticate to it.

**Fix:** Rotate the device token:
```bash
openclaw gateway rotate-device-token
```
This will reissue the token and restart the gateway. After that, `openclaw gateway status` should show "RPC probe: ok".

Once token is fixed, any of the above access methods will work.

---

**Tags:** tailscale, ssh-tunnel, gateway, remote-access
