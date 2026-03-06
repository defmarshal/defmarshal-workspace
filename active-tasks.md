# Active Tasks Registry

**Last updated**: 2026-03-06 06:25 UTC

## ✅ Core System Active (06:23 UTC)

**OpenClaw Cron Enabled**: 8 essential jobs
- telegram-slash-handler (e26c12bd) – every 2 min
- agent-manager-cron (5b617517) – every 30 min
- meta-supervisor-agent (65f0d1f3) – hourly at :05
- meta-agent-cron (3291b8d1) – hourly
- dev-agent-cron (e345525c) – hourly 8–22 Asia/Bangkok
- content-agent-cron (f69140f6) – hourly 8–22 Asia/Bangkok
- research-agent-cron (aadf040b) – hourly 8–22 Asia/Bangkok
- git-janitor-cron (a27a9b33) – every 6h UTC

**Agents Running**:
- meta-supervisor-daemon (PID 1303872) – Continuous auditor (restarted 08:08 UTC)

**System Cron**: Cleared (0 entries) – all workspace tasks now in OpenClaw cron

---

## Deleted Permanently (2026-03-06)

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

**Marked for delete**: These should be removed to reduce config clutter.

---

## Backups

- Cron config backup: `backups/cron-disable-backup-2026-03-06.md`
- System crontab backup: `backups/crontab.full.bak.2026-03-06`
- Full review: `backups/cron-review-2026-03-06.md`

---

## Notes

- Auto-reenable scheduler cancelled (PID 1278888)
- Core system running lean; no optional noise
- To delete optional jobs: `openclaw cron remove <id>`
- **2026-03-06 fixes**: Cleared stuck meta-agent-cron session (08:04); restarted meta-supervisor daemon (08:08); memory main store reindex in progress (session calm-basil).

