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

### Daily Memory Summarization
- **Schedule**: Daily at 22:30 Asia/Bangkok (22:30 local)
- **Command**:
  ```bash
  30 22 * * * TZ='Asia/Bangkok' /home/ubuntu/.openclaw/workspace/summarize-day >> /home/ubuntu/.openclaw/workspace/memory/daily-summary-cron.log 2>&1
  ```
- **Log**: `memory/daily-summary-cron.log`
- **Description**: Generates a categorized daily summary from the day's memory entries and appends to `memory/YYYY-MM-DD.md`.

### Traffic Report (Weekly)
- **Schedule**: Weekly on Sunday at 22:00 UTC (Monday 05:00 Jakarta, Monday 22:00 UTC+7? Actually 22:00 UTC is Monday 05:00 Jakarta). This runs Sunday evenings UTC.
- **Command**:
  ```bash
  0 22 * * 0 /usr/bin/python3 /home/ubuntu/.nanobot/workspace/weekly_traffic_report.py >> /home/ubuntu/.nanobot/workspace/weekly_cron.log 2>&1
  ```
- **Log**: `/home/ubuntu/.nanobot/workspace/weekly_cron.log`
- **Description**: Generates weekly traffic analysis report.

### Traffic Analysis (Daily)
- **Schedule**: Daily at 05:00 UTC (12:00 Asia/Jakarta? Actually 05:00 UTC is 12:00 Jakarta)
- **Command**:
  ```bash
  0 5 * * * cd /home/ubuntu/.nanobot/workspace && /usr/bin/python3 /home/ubuntu/.nanobot/workspace/traffic_analysis_script.py >> /home/ubuntu/.nanobot/workspace/traffic_cron.log 2>&1
  ```
- **Log**: `/home/ubuntu/.nanobot/workspace/traffic_cron.log`

### Traffic Report (bash)
- **Schedule**: Daily at 22:00 UTC (05:00 Asia/Jakarta next day)
- **Command**:
  ```bash
  0 22 * * * bash /home/ubuntu/.openclaw/workspace/traffic_report.sh
  ```
- **Description**: Shell script for traffic reporting; likely sends to Telegram.

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
