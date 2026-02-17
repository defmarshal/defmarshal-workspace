# Cron Jobs Documentation

This file documents all scheduled tasks for the workspace, including system cron and OpenClaw cron jobs.

## System Cron (user crontab)

As of 2026‑02‑16, **all recurring workspace tasks have been migrated to OpenClaw cron**. The system crontab now only retains the agent startup hook (and a few unrelated nanobot jobs which are outside this workspace's scope).

### Agent Startup (Daemon Bootstrap)
### Gateway Watchdog (system crontab)
- **Schedule**: Every 5 minutes (`*/5 * * * *`)
- **Command**: `/home/ubuntu/.openclaw/workspace/scripts/gateway-watchdog.sh`
- **Log**: `gateway-watchdog.log` (rotated by log‑rotate)
- **Description**: Checks if OpenClaw gateway is active; restarts it if down. Runs outside OpenClaw for reliability.

---
- **Schedule**: `@reboot` with 60‑second delay
- **Command**:
  ```bash
  @reboot bash -c "sleep 60 && /home/ubuntu/.openclaw/workspace/start-background-agents.sh"
  ```
- **Log**: `dev-agent.log`, `content-agent.log`, `research-agent.log`, `torrent-bot.log`
- **Description**: Ensures all background agents and daemons (dev, content, research, torrent-bot, aria2) are running after system boot.

## OpenClaw Cron (via `openclaw cron`)

Managed through the OpenClaw Gateway. These run in isolated sessions and announce results to Telegram (id: 952170974). All times in their respective timezones.

### Current OpenClaw Cron Jobs

1. **workspace-builder**
   - **Schedule**: Every 2 hours (`0 */2 * * *`) in Asia/Bangkok
   - **Payload**: agentTurn with strategic builder prompt
   - **Model**: `openrouter/stepfun/step-3.5-flash:free`
   - **Timeout**: 600 seconds
   - **Description**: Analyzes workspace, implements improvements, validates, commits with `build:` prefix. Runs 24/7.

2. **email-cleaner-cron**
   - **Schedule**: Daily at 09:00 Asia/Bangkok
   - **Payload**: agentTurn instructing execution of `./quick email-clean` (dry‑run by default)
   - **Log**: `memory/email-cleaner-cron.log`
   - **Description**: Archives promotional emails and applies labels. Uses dry‑run unless `--execute` passed (manual override).

3. **auto-torrent-cron**
   - **Schedule**: Daily at 02:00 Asia/Bangkok
   - **Payload**: agentTurn running `./quick nyaa-top --limit 10 --max-size 2G --add`
   - **Log**: `memory/auto-torrent.log`
   - **Description**: Fetches top 10 anime torrents from Sukebei.Nyaa.si under 2GB and adds them to aria2 automatically.

4. **random-torrent-downloader**
   - **Schedule**: Every 2 hours (`0 */2 * * *`) in UTC
   - **Payload**: agentTurn executing `/bin/bash /home/ubuntu/.openclaw/workspace/cron/torrent-downloader.sh`
   - **Log**: System logger (`logger -t torrent-downloader`)
   - **Description**: Picks a random torrent from top 20 (max 1GB) and adds if not already present. Also checks disk thresholds to avoid overfilling.

5. **traffic-report-cron**
   - **Schedule**: Daily at 22:00 UTC
   - **Payload**: agentTurn executing `bash /home/ubuntu/.openclaw/workspace/traffic_report.sh`
   - **Description**: Generates daily traffic report (likely sends to Telegram). No dedicated log file; output captured in agent session.

6. **content-index-update-cron**
   - **Schedule**: Daily at 05:30 Asia/Bangkok
   - **Payload**: agentTurn running `./quick content-index-update` and appending to `memory/content-index-cron.log`
   - **Description**: Regenerates `content/INDEX.md` to reflect new content files.

7. **memory-reindex-cron**
   - **Schedule**: Weekly on Sunday at 04:00 Asia/Bangkok (`0 4 * * 0`)
   - **Payload**: agentTurn executing `./quick memory-index` and appending to `memory/memory-reindex.log`
   - **Description**: Reindex memory files to clear the Voyage AI "dirty" flag and maintain search performance. Addresses rate-limit delays by periodic reindexing.

8. **log-rotate-cron**
   - **Schedule**: Weekly on Sunday at 05:00 Asia/Bangkok (`0 5 * * 0`)
   - **Payload**: agentTurn executing `./quick log-rotate` and appending to `memory/log-rotate.log`
   - **Description**: Rotates aria2.log when it exceeds 100 MB, keeping up to 4 compressed archives. Prevents uncontrolled log growth.

9. **dev-agent-cron**
   - **Schedule**: Every 20 minutes between 08:00-22:00 Asia/Bangkok (`0,20,40 8-22 * * *`)
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/dev-cycle.sh >> dev-agent.log 2>&1'`
   - **Description**: Performs one dev-agent cycle (scan workspace, implement utilities, commit with 'dev:' prefix). Migrated from persistent daemon to cron on 2026-02-16.

10. **content-agent-cron**
    - **Schedule**: Every 10 minutes between 08:00-22:00 Asia/Bangkok (`0,10,20,30,40,50 8-22 * * *`)
    - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/content-cycle.sh >> content-agent.log 2>&1'`
    - **Description**: Performs one content-agent cycle (create anime summaries, tech writeups, digests). Migrated from persistent daemon to cron on 2026-02-16.

11. **research-agent-cron**
    - **Schedule**: Every 15 minutes between 08:00-22:00 Asia/Bangkok (`0,15,30,45 8-22 * * *`)
    - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/research-cycle.sh >> research-agent.log 2>&1'`
    - **Description**: Performs one research-agent cycle (conduct research on anime, banking, tech, AI). Migrated from persistent daemon to cron on 2026-02-16.

12. **cleanup-downloads-cron**
    - **Schedule**: Weekly on Sunday at 06:00 Asia/Bangkok (`0 6 * * 0`)
    - **Payload**: agentTurn executing `quick cleanup-downloads --execute --days 30` and appending to `memory/cleanup-downloads.log`
    - **Description**: Automated cleanup of old torrent downloads (retention: 30 days). Runs dry-run by default through the wrapper; cron uses `--execute` to apply.

13. **backup-cleanup-cron**
    - **Schedule**: Weekly on Sunday at 07:00 Asia/Bangkok (`0 7 * * 0`)
    - **Payload**: agentTurn executing `./quick cleanup-backups --execute --keep 1` and appending to `memory/backup-cleanup.log`
    - **Description**: Automated cleanup of old backup tarballs (retention: keep 1). Runs with `--execute` via cron.

---

**Note**: To modify any job, use `openclaw cron` commands (`list`, `update`, `remove`) or edit the gateway configuration. System cron should not be edited for workspace tasks anymore.

## Maintenance Commands

- `quick cleanup-downloads [--days N] [--execute] [--verbose]` – Clean old downloads in `workspace/downloads/`.
- `quick cleanup-backups [--keep N] [--execute] [--verbose]` – Clean old backup tarballs in `/home/ubuntu/`. Keeps most recent N (default 1). Use with care.

Backup cleanup is scheduled weekly via **backup-cleanup-cron** (Sunday 07:00 Asia/Bangkok). Manual runs still available.
