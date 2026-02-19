# Cron Jobs Documentation

This file documents all scheduled tasks for the workspace, including system cron and OpenClaw cron jobs.

## System Cron (user crontab)

As of 2026‑02‑16, **all recurring workspace tasks have been migrated to OpenClaw cron**. The system crontab now only retains the agent startup hook (and a few unrelated nanobot jobs which are outside this workspace's scope).

### Agent Startup (Daemon Bootstrap)
### Gateway Watchdog (system crontab)
- **Schedule**: Every hour (`0 * * * *`)
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

2. **auto-torrent-cron**
   - **Schedule**: Daily at 02:00 Asia/Bangkok
   - **Payload**: agentTurn running `./quick nyaa-top --limit 10 --max-size 2G --add`
   - **Log**: `memory/auto-torrent.log`
   - **Description**: Fetches top 10 anime torrents from Sukebei.Nyaa.si under 2GB and adds them to aria2 automatically.

3. **random-torrent-downloader**
   - **Schedule**: Every 2 hours (`0 */2 * * *`) in UTC
   - **Payload**: agentTurn executing `/bin/bash /home/ubuntu/.openclaw/workspace/cron/torrent-downloader.sh`
   - **Log**: System logger (`logger -t torrent-downloader`)
   - **Description**: Picks a random torrent from top 20 (max 1GB) and adds if not already present. Also checks disk thresholds to avoid overfilling.

4. **content-index-update-cron**
   - **Schedule**: Daily at 05:30 Asia/Bangkok
   - **Payload**: agentTurn running `./quick content-index-update` and appending to `memory/content-index-cron.log`
   - **Description**: Regenerates `content/INDEX.md` to reflect new content files.

5. **memory-reindex-cron**
   - **Schedule**: Weekly on Sunday at 04:00 Asia/Bangkok (`0 4 * * 0`)
   - **Payload**: agentTurn executing `./quick memory-index` and appending to `memory/memory-reindex.log`
   - **Description**: Reindex memory files to clear the Voyage AI "dirty" flag and maintain search performance. Addresses rate-limit delays by periodic reindexing.

6. **log-rotate-cron**
   - **Schedule**: Weekly on Sunday at 05:00 Asia/Bangkok (`0 5 * * 0`)
   - **Payload**: agentTurn executing `./quick log-rotate` and appending to `memory/log-rotate.log`
   - **Description**: Rotates aria2.log when it exceeds 100 MB, keeping up to 4 compressed archives. Prevents uncontrolled log growth.

7. **dev-agent-cron**
   - **Schedule**: Hourly between 08:00-22:00 Asia/Bangkok (`0 8-22 * * *`)
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/dev-cycle.sh >> dev-agent.log 2>&1'`
   - **Description**: Performs one dev-agent cycle (scan workspace, implement utilities, commit with 'dev:' prefix). Reduced from every 20 min to hourly (token optimization, 2026-02-19).

8. **content-agent-cron**
   - **Schedule**: Hourly between 08:00-22:00 Asia/Bangkok (`0 8-22 * * *`)
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/content-cycle.sh >> content-agent.log 2>&1'`
   - **Description**: Performs one content-agent cycle (create anime summaries, tech writeups, digests). Reduced from every 10 min to hourly (token optimization, 2026-02-19).

9. **research-agent-cron**
   - **Schedule**: Hourly between 08:00-22:00 Asia/Bangkok (`0 8-22 * * *`)
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/research-cycle.sh >> research-agent.log 2>&1'`
   - **Description**: Performs one research-agent cycle (conduct research on anime, banking, tech, AI). Reduced from every 15 min to hourly (token optimization, 2026-02-19).

10. **cleanup-downloads-cron**
    - **Schedule**: Weekly on Sunday at 06:00 Asia/Bangkok (`0 6 * * 0`)
    - **Payload**: agentTurn executing `quick cleanup-downloads --execute --days 30` and appending to `memory/cleanup-downloads.log`
    - **Description**: Automated cleanup of old torrent downloads (retention: 30 days). Runs dry-run by default through the wrapper; cron uses `--execute` to apply.

11. **backup-cleanup-cron**
    - **Schedule**: Weekly on Sunday at 07:00 Asia/Bangkok (`0 7 * * 0`)
    - **Payload**: agentTurn executing `./quick cleanup-backups --execute --keep 1` and appending to `memory/backup-cleanup.log`
    - **Description**: Automated cleanup of old backup tarballs (retention: keep 1). Runs with `--execute` via cron.

12. **cleanup-agent-artifacts-cron**
    - **Schedule**: Weekly on Sunday at 09:30 Asia/Bangkok (`30 9 * * 0`)
    - **Payload**: agentTurn executing `./quick cleanup-agent-artifacts --execute --force` and appending to `memory/cleanup-agent-artifacts-cron.log`
    - **Description**: Automated cleanup of stale agent artifacts (lock files, empty plan files). Runs with `--execute` and `--force` to ensure it operates during quiet hours if needed. Respects quiet hours by default when run manually.

13. **archiver-manager-cron**
    - **Schedule**: Weekly on Sunday at 02:00 UTC (`0 2 * * 0`)
    - **Payload**: agentTurn executing `./agents/archiver-manager.sh >> memory/archiver-manager.log 2>&1'`
    - **Log**: `memory/archiver-manager.log`
    - **Description**: Manages archiving of old content and research files to maintain workspace organization and prevent clutter.

14. **daily-digest-cron**
    - **Schedule**: Twice daily at 12:00 and 20:00 Asia/Bangkok (`0 12,20 * * *`)
    - **Payload**: agentTurn that runs a daily digest agent (message prompts it to gather content/research highlights, dev commits, health, and write `reports/YYYY-MM-DD-daily-digest.md` then announce to Telegram)
    - **Description**: Aggregates daily activity into a concise markdown report and sends it to Telegram. Outputs also saved in `reports/` for persistence. Individual agent announcements are suppressed; this is the sole daily summary.

15. **agent-manager-cron**
    - **Schedule**: Every 30 minutes (`*/30 * * * *`) in Asia/Bangkok
    - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/agent-manager.sh --once'`
    - **Log**: `memory/agent-manager.log`
    - **Description**: Monitors and manages other background agents (prevents duplicate runs, cleans stale locks, maintains agent health).

16. **git-janitor-cron**
    - **Schedule**: Every 6 hours (`0 */6 * * *`) in UTC
    - **Payload**: agentTurn executing `./agents/git-janitor-cycle.sh >> memory/git-janitor.log 2>&1'`
    - **Log**: `memory/git-janitor.log`
    - **Description**: Git maintenance cycle (auto-commit when thresholds met, cleanup, push). Handles rate limits and coordinates with agent manager.

17. **agni-cron**
    - **Schedule**: Every 2 hours (`0 */2 * * *`) in UTC
    - **Payload**: agentTurn that runs the Agni brainstorming cycle (spawns Rudra to execute plans). Command: `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/agni-cycle.sh >> agents/agni/agni.log 2>&1'`
    - **Log**: `agents/agni/agni.log`
    - **Description**: Brainstorming agent that generates creative ideas and plans, then spawns Rudra agent to implement them.

18. **vishwakarma-cron**
    - **Schedule**: Every 4 hours (`0 */4 * * *`) in Asia/Bangkok
    - **Payload**: agentTurn that runs the Vishwakarma game development planning cycle (spawns Krishna to build games). Command: `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/vishwakarma-cycle.sh >> agents/vishwakarma/vishwakarma.log 2>&1'`
    - **Log**: `agents/vishwakarma/vishwakarma.log`
    - **Description**: Game development planning agent that designs game projects and spawns Krishna agent to build them.

19. **supervisor-cron**
    - **Schedule**: Every 30 minutes (`0,30 * * * *`) in Asia/Bangkok
    - **Payload**: agentTurn executing `./agents/supervisor.sh`
    - **Log**: `memory/supervisor.log`
    - **Delivery**: `announce` (only when alerts)
    - **Description**: Monitors cron job health, gateway status, memory index, disk usage, and APT updates. Sends Telegram alerts when issues detected. Reduced from every 5 min to 30 min (token optimization, 2026-02-19).

20. **notifier-cron**
    - **Schedule**: Every 2 hours (`0 */2 * * *`) in UTC
    - **Payload**: agentTurn executing `./agents/notifier-agent.sh >> memory/notifier-agent.log 2>&1'`
    - **Log**: `memory/notifier-agent.log`
    - **Description**: Monitors cron failures, disk usage, gateway status; sends Telegram alerts when thresholds exceeded. Focused on alerting only.

21. **meta-agent-cron**
    - **Schedule**: Every hour (`0 * * * *`) in Asia/Bangkok
    - **Payload**: agentTurn executing `./agents/meta-agent.sh --once`
    - **Log**: `memory/meta-agent.log`
    - **Delivery**: `announce` (summary of actions taken)
    - **Description**: Autonomous planner that observes system health, decides on maintenance/improvement actions, spawns sub‑agents to execute them, validates outcomes, and commits changes with `meta:` prefix. Core of the self‑extending system.

---

**Note**: To modify any job, use `openclaw cron` commands (`list`, `update`, `remove`) or edit the gateway configuration. System cron should not be edited for workspace tasks anymore.

## Maintenance Commands

- `quick cleanup-downloads [--days N] [--execute] [--verbose]` – Clean old downloads in `workspace/downloads/`.
- `quick cleanup-backups [--keep N] [--execute] [--verbose]` – Clean old backup tarballs in `/home/ubuntu/`. Keeps most recent N (default 1). Use with care.
- `quick cleanup-agent-artifacts [--execute] [--force]` – Clean stale agent artifacts (lock files, empty plans). Respects quiet hours unless `--force`.

Weekly automation:
- cleanup-downloads-cron (Sunday 06:00)
- backup-cleanup-cron (Sunday 07:00)
- cleanup-agent-artifacts-cron (Sunday 09:30)
