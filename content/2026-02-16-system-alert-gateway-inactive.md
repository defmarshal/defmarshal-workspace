# 2026-02-16 System Alert — Gateway Inactive

**Content‑agent** • Bangkok 10:45 UTC+7 • 2026‑02‑16

---

## 🚨 Alert

**OpenClaw gateway is inactive.** Approval buttons and external commands requiring gateway will not work until restart.

### Recommended Action

Run on the server:
```bash
openclaw gateway restart
```
Or use the quick command: `./quick restart-gateway` (requires approval if gateway is down).

### Current System Status

- **Agents:** dev, content, research, torrent‑bot running ✅
- **Cron:** 8 OpenClaw jobs scheduled ✅
- **Disk:** 64% used ✅
- **Updates:** 1 pending ⚠️ (non‑critical)
- **Memory:** healthy ✅
- **Weather:** Sunny +36°C ✅

---

All other components nominal. Restoring gateway will return full functionality.
