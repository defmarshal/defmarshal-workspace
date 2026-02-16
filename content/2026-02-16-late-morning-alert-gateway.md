# 2026-02-16 Late Morning Alert — Gateway Inactive

**Content‑agent** • Bangkok 10:55 UTC+7 • 2026‑02‑16

---

## 🚨 Gateway Status

**OpenClaw gateway is inactive.** This affects:
- Approval buttons for external commands
- Telegram interactions that require gateway
- Cron jobs that rely on gateway (though isolated sessions may still run)

### Recovery

Run on server:
```bash
openclaw gateway restart
```
Or use `./quick restart-gateway` (requires approval; may need manual if gateway down).

---

## ✅ Other Systems

- **Agents:** dev, content, research, torrent‑bot running
- **Cron:** 8 OpenClaw jobs scheduled
- **Disk:** 64% | **Updates:** 1 pending (non‑critical)
- **Memory:** healthy
- **Weather:** Sunny +36°C

All non‑gateway components stable.
