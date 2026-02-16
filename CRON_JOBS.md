# Cron Jobs Documentation

This file documents all scheduled tasks for the workspace, including system cron and OpenClaw cron jobs.

## System Cron (user crontab)

All jobs run under the `ubuntu` user. Timezone is UTC unless otherwise specified.

### Email Cleaner (Gmail Auto-Archiver)
- **Schedule**: Daily at 09:00 Asia/Bangkok
- **Command**:
  ```bash
  0 9 * * * TZ='Asia/Bangkok' cd /home/ubuntu/.openclaw/workspace && /home/ubuntu/.openclaw/workspace/quick email-clean >> /home/ubuntu/.openclaw/workspace/memory/email-cleaner-cron.log 2>&1
  ```
- **Log**: `memory/email-cleaner-cron.log`
- **Description**: Runs the email-cleaner script in dry-run mode by default. Use `--execute` to apply changes (requires manual trigger).

### Auto Torrent Download (Top Selections)
- **Schedule**: Daily at 02:00 Asia/Bangkok
- **Command**:
  ```bash
  0 2 * * * TZ='Asia/Bangkok' cd /home/ubuntu/.openclaw/workspace && /home/ubuntu/.openclaw/workspace/quick nyaa-top --limit 10 --max-size 2G --add >> /home/ubuntu/.openclaw/workspace/memory/auto-torrent.log 2>&1
  ```
- **Log**: `memory/auto-torrent.log`
- **Description**: Fetches top 10 anime torrents from Sukebei.Nyaa.si under 2GB and adds them to aria2 automatically.

### Content Index Update (Archive Maintainer)
- **Schedule**: Daily at 05:30 Asia/Bangkok
- **Command**:
  ```bash
  30 5 * * * TZ='Asia/Bangkok' cd "/home/ubuntu/.openclaw/workspace" && "/home/ubuntu/.openclaw/workspace/quick" content-index-update >> "/home/ubuntu/.openclaw/workspace/memory/content-index-cron.log" 2>&1
  ```
- **Log**: `memory/content-index-cron.log`
- **Description**: Regenerates `content/INDEX.md` to reflect newly created content files. Ensures the content archive stays browsable and up-to-date.

### Random Torrent Downloader
- **Schedule**: Every 2 hours (`0 */2 * * *`)
- **Command**:
  ```bash
  0 */2 * * * /bin/bash /home/ubuntu/.openclaw/workspace/cron/torrent-downloader.sh
  ```
- **Log**: System log (`logger -t torrent-downloader`) and script output
- **Description**: Picks a random torrent from the top 20 (max 1GB) and adds it to aria2 if not already present. Respects quiet hours (23:00–08:00 Asia/Bangkok) and disk space thresholds.

### Startup Agents (Daemons)
- **Schedule**: `@reboot` with 60-second delay
- **Command**:
  ```bash
  @reboot bash -c "sleep 60 && /home/ubuntu/.openclaw/workspace/start-background-agents.sh"
  ```
- **Log**: Agent-specific logs (`dev-agent.log`, `content-agent.log`, `research-agent.log`)
- **Description**: Ensures all background agents and daemons (aria2, agent loops, torrent-bot) are started after system reboot.

## OpenClaw Cron (via `openclaw cron`)

Managed through the OpenClaw Gateway. These run in isolated sessions.

### Workspace Builder
- **Name**: workspace-builder
- **Schedule**: Every 2 hours (`0 */2 * * *`) in Asia/Bangkok timezone.
- **Payload**: Isolated agent turn with a strategic builder prompt.
- **Model**: `openrouter/stepfun/step-3.5-flash:free`
- **Timeout**: 600 seconds
- **Delivery**: Announces results to Telegram (channel: telegram, to: 952170974)
- **Description**: Autonomous agent that analyzes the workspace, identifies meaningful improvements, implements them, commits & pushes changes, and logs summaries to `memory/workspace-builder.log`. Respects quiet hours (23:00–08:00 UTC+7). This is the only OpenClaw cron job currently.

---

**Note**: To modify any cron job, edit the corresponding crontab (`crontab -e` for system cron) or use `openclaw cron` commands for OpenClaw cron.
