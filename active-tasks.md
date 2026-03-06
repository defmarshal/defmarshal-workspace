# Active Tasks Registry

**Last updated**: 2026-03-06 08:28 UTC

## ✅ Core System Active (06:23 UTC)

**OpenClaw Cron Enabled**: 8 essential jobs
- telegram-slash-handler (e26c12bd) – every 2 min
- agent-manager-cron (5b617517) – every 30 min
- meta-agent-cron (3291b8d1) – hourly
- dev-agent-cron (e345525c) – hourly 8–22 Asia/Bangkok
- content-agent-cron (f69140f6) – hourly 8–22 Asia/Bangkok
- research-agent-cron (aadf040b) – hourly 8–22 Asia/Bangkok
- git-janitor-cron (a27a9b33) – every 6h UTC

**Note:** `meta-supervisor-agent` cron removed; daemon stopped.

---

## 🗑️ Removed (2026-03-06)

- meta-supervisor-agent (65f0d1f3) – keepalive cron removed
- meta-supervisor daemon – killed; backup saved
- workspace-builder (23dad379) – redundant
- auto-torrent-cron (483e96ab) – redundant
- notifier-cron (3cbadb80) – alerting off
- idea-generator-cron (9112eca8) – low ROI
- idea-executor-cron (86722825) – low ROI

---

## Disabled (Optional/Experimental)

- mewchat-evolver-cron (5d3597fc)
- game-enhancer-cron (4e9eb829)
- cleanup-agent-artifacts-cron (6e07b8d1)
- daily-digest-cron (16af6af1)
- youtube-digest-daily (c6976c90) – **marked for delete**
- content-index-update-cron (dada350a) – **marked for delete**
- log-rotate-cron (c6bca31f) – **marked for delete**
- memory-reindex-cron (b84b1f5c)
- cleanup-downloads-cron (fb670b4f) – **marked for delete**
- backup-cleanup-cron (d5c6f526)
- archiver-manager-cron (db19ad80)
- time-capsule-weekly (6e4f5697)
- agni-cron (23788edb)
- vishwakarma-cron (6e5621c3)
- evolver-agent-cron (6a1b4266)
- random-torrent-downloader (aadf040b) – disabled (not core)

**Marked for delete**: Will be removed to reduce config clutter.

---

## Backups

- Cron config: `backups/cron-disable-backup-2026-03-06.md`
- System crontab: `backups/crontab.full.bak.2026-03-06`
- Meta-supervisor: `backups/meta-supervisor-backup-2026-03-06_0926/`
- Full review: `backups/cron-review-2026-03-06.md`

---

## Status

- **Meta-supervisor**: Stopped and removed. No more daemon. No more audit reports.
- **System messages**: If "System Status" continues, source is external (gateway/system).
- **Core cron**: 8 essential jobs running (telegram-slash, agent-manager, meta-agent, dev, content, research, git-janitor, random-torrent disabled).

**Next:** Monitor Telegram. If status pings persist, investigate gateway/system sources.

### Removed (2026-03-06 08:45 UTC)

**cron-supervisor agent** — suspected source of periodic "System Status" Telegram broadcasts.
- Removed from openclaw.json agents.list
- Should silence the status pings if it was the culprit.
