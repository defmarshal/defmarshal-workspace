# Cron Jobs Documentation

This file documents all scheduled tasks for the workspace, including system cron and OpenClaw cron jobs.

## System Cron (user crontab)

As of 2026‑02‑16, **all recurring workspace tasks have been migrated to OpenClaw cron**. The system crontab now only retains the agent startup hook (and a few unrelated nanobot jobs which are outside this workspace's scope).

### Gateway Watchdog (system crontab)
- **Schedule**: Every hour (`0 * * * *`)
- **Command**: `/home/ubuntu/.openclaw/workspace/scripts/gateway-watchdog.sh`
- **Log**: `gateway-watchdog.log` (rotated by log‑rotate)
- **Description**: Checks if OpenClaw gateway is active; restarts it if down. Runs outside OpenClaw for reliability.

### Agent Startup (Daemon Bootstrap)
- **Schedule**: `@reboot` with 60‑second delay
- **Command**:
  ```bash
  @reboot bash -c "sleep 60 && /home/ubuntu/.openclaw/workspace/start-background-agents.sh"
  ```
- **Log**: `dev-agent.log`, `content-agent.log`, `research-agent.log`, `torrent-bot.log`
- **Description**: Ensures all background agents and daemons (dev, content, research, torrent-bot, aria2) are running after system boot.

## OpenClaw Cron (via `openclaw cron`)

Managed through the OpenClaw Gateway. These run in isolated sessions and announce results to Telegram (id: 952170974). All times in their respective timezones.

**Schedule Enforcement:** Schedules are automatically validated and corrected by the `agent-manager-cron` via `scripts/validate-cron-schedules.sh` every 30 minutes to prevent drift from the documented values. Do not manually edit schedules directly; update this document and let the validation script propagate changes.

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

7. **cleanup-logs-cron**
   - **Schedule**: Weekly on Sunday at 05:30 Asia/Bangkok (`30 5 * * 0`)
   - **Payload**: agentTurn executing `./quick cleanup-logs` and appending to `memory/cleanup-logs.log`
   - **Description**: Rotates large agent logs (>100 MB) and deletes compressed archives older than 30 days. Runs immediate cleanup; retention configurable via script env vars.

8. **dev-agent-cron**
   - **Schedule**: Hourly between 08:00-22:00 Asia/Bangkok (`0 8-22 * * *`)
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/dev-cycle.sh >> dev-agent.log 2>&1'`
   - **Description**: Performs one dev-agent cycle (scan workspace, implement utilities, commit with 'dev:' prefix). Includes retry logic for transient OpenRouter rate limits. Reduced from every 20 min to hourly (token optimization, 2026-02-19).

9. **content-agent-cron**
   - **Schedule**: Hourly between 08:00-22:00 Asia/Bangkok (`0 8-22 * * *`)
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/content-cycle.sh >> content-agent.log 2>&1'`
   - **Description**: Performs one content-agent cycle (create anime summaries, tech writeups, digests). Includes retry logic for transient OpenRouter rate limits. Reduced from every 10 min to hourly (token optimization, 2026-02-19).

10. **research-agent-cron**
   - **Schedule**: Hourly between 08:00-22:00 Asia/Bangkok (`0 8-22 * * *`)
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/research-cycle.sh >> research-agent.log 2>&1'`
   - **Description**: Performs one research-agent cycle (conduct research on anime, banking, tech, AI). Includes retry logic for transient OpenRouter rate limits. Reduced from every 15 min to hourly (token optimization, 2026-02-19).

11. **cleanup-downloads-cron**
    - **Schedule**: Weekly on Sunday at 06:00 Asia/Bangkok (`0 6 * * 0`)
    - **Payload**: agentTurn executing `quick cleanup-downloads --execute --days 30` and appending to `memory/cleanup-downloads.log`
    - **Description**: Automated cleanup of old torrent downloads (retention: 30 days). Runs dry-run by default through the wrapper; cron uses `--execute` to apply.

12. **backup-cleanup-cron**
    - **Schedule**: Weekly on Sunday at 07:00 Asia/Bangkok (`0 7 * * 0`)
    - **Payload**: agentTurn executing `./quick cleanup-backups --execute --keep 1` and appending to `memory/backup-cleanup.log`
    - **Description**: Automated cleanup of old backup tarballs (retention: keep 1). Runs with `--execute` via cron.

13. **cleanup-agent-artifacts-cron**
    - **Schedule**: Weekly on Sunday at 09:30 Asia/Bangkok (`30 9 * * 0`)
    - **Payload**: agentTurn executing `./quick cleanup-agent-artifacts --execute --force` and appending to `memory/cleanup-agent-artifacts-cron.log`
    - **Description**: Automated cleanup of stale agent artifacts (lock files, empty plan files). Runs with `--execute` and `--force` to ensure it operates during quiet hours if needed. Respects quiet hours by default when run manually.

14. **archiver-manager-cron**
    - **Schedule**: Weekly on Sunday at 02:00 UTC (`0 2 * * 0`)
    - **Payload**: agentTurn executing `./agents/archiver-manager.sh >> memory/archiver-manager.log 2>&1'`
    - **Log**: `memory/archiver-manager.log`
    - **Description**: Manages archiving of old content and research files to maintain workspace organization and prevent clutter.

16. **agent-manager-cron**
    - **Schedule**: Every 30 minutes (`*/30 * * * *`) in Asia/Bangkok
    - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/agent-manager.sh --once'`
    - **Log**: `memory/agent-manager.log`
    - **Description**: Monitors and manages other background agents (prevents duplicate runs, cleans stale locks, maintains agent health).

17. **git-janitor-cron**
    - **Schedule**: Every 6 hours (`0 */6 * * *`) in UTC
    - **Payload**: agentTurn executing `./agents/git-janitor-cycle.sh >> memory/git-janitor.log 2>&1'`
    - **Log**: `memory/git-janitor.log`
    - **Description**: Git maintenance cycle (auto-commit when thresholds met, cleanup, push). Handles rate limits and coordinates with agent manager.

18. **agni-cron**
    - **Schedule**: Every 2 hours (`0 */2 * * *`) in UTC
    - **Payload**: agentTurn that runs the Agni brainstorming cycle (spawns Rudra to execute plans). Command: `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/agni-cycle.sh >> agents/agni/agni.log 2>&1'`
    - **Log**: `agents/agni/agni.log`
    - **Description**: Brainstorming agent that generates creative ideas and plans, then spawns Rudra agent to implement them.

19. **vishwakarma-cron**
    - **Schedule**: Every 4 hours (`0 */4 * * *`) in Asia/Bangkok
    - **Payload**: agentTurn that runs the Vishwakarma game development planning cycle (spawns Krishna to build games). Command: `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/vishwakarma-cycle.sh >> agents/vishwakarma/vishwakarma.log 2>&1'`
    - **Log**: `agents/vishwakarma/vishwakarma.log`
    - **Description**: Game development planning agent that designs game projects and spawns Krishna agent to build them.

21. **notifier-cron**
    - **Schedule**: Every 2 hours (`0 */2 * * *`) in UTC
    - **Payload**: agentTurn executing `./agents/notifier-agent.sh >> memory/notifier-agent.log 2>&1'`
    - **Log**: `memory/notifier-agent.log`
    - **Description**: Monitors cron failures, disk usage, gateway status; sends Telegram alerts when thresholds exceeded. Focused on alerting only.

22. **meta-agent-cron**
    - **Schedule**: Every hour (`0 * * * *`) in Asia/Bangkok
    - **Payload**: agentTurn executing `./agents/meta-agent.sh --once`
    - **Log**: `memory/meta-agent.log`
    - **Delivery**: `announce` (summary of actions taken)
    - **Description**: Autonomous planner that observes system health, decides on maintenance/improvement actions, spawns sub‑agents to execute them, validates outcomes, and commits changes with `meta:` prefix. Core of the self‑extending system.

24. **idea-generator-cron**
    - **Schedule**: Every 6 hours (`0 */6 * * *`) in UTC
    - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/idea-generator/idea-generator-cycle.sh >> memory/idea-generator.log 2>&1'`
    - **Log**: `memory/idea-generator.log`
    - **Description**: Autonomous creative brainstorming agent; generates 10 innovative project/improvement ideas each run and writes to `agents/ideas/latest.json`. Idea quality is designed to be fun and practical.

25. **idea-executor-cron**
    - **Schedule**: Every 2 hours (`0 */2 * * *`) in UTC
    - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/idea-executor/idea-executor-cycle.sh >> memory/idea-executor.log 2>&1'`
    - **Log**: `memory/idea-executor.log`
    - **Description**: Executes one pending idea per cycle using simple `exec` commands; updates `agents/ideas/latest.json` with results and status. Runs sequentially, easy to monitor.

26. **evolver-agent-cron**
   - **Schedule**: Every 6 hours (`0 */6 * * *`) in UTC
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/evolver-cycle.sh >> memory/evolver-agent.log 2>&1'`
   - **Log**: `memory/evolver-agent.log`
   - **Description**: Runs the capability-evolver skill in review mode to analyze runtime history and propose self-improvements. Proposals are logged; no automatic application. Set `EVOLVE_STRATEGY=repair-only` by default for safety. Use `--review` to require human approval.

---

**Note**: To modify any job, use `openclaw cron` commands (`list`, `update`, `remove`) or edit the gateway configuration. System cron should not be edited for workspace tasks anymore.

## Inactive Cron Jobs

The following cron jobs are currently **disabled** for token conservation (user request, 2026-02-28). They can be re-enabled with `openclaw cron enable <id>`.

### daily-digest-cron
- **Schedule:** Twice daily at 12:00 and 20:00 Asia/Bangkok (`0 12,20 * * *`)
- **Original description:** Aggregates daily activity into a concise markdown report and sends it to Telegram. Outputs also saved in `reports/` for persistence. Stderr (errors) logged to `memory/daily-digest.log`. Simplified on 2026-02-21 to reduce LLM usage and avoid rate limits (direct exec instead of verbose agent prompt).
- **Status:** Disabled
- **Re-enable:** `openclaw cron enable 5b6a002d`

### supervisor-cron
- **Schedule:** Every 30 minutes (`0,30 * * * *`) in Asia/Bangkok
- **Original description:** Monitors cron job health, gateway status, memory index, disk usage, and APT updates. Sends Telegram alerts when issues detected. Reduced from every 5 min to 30 min (token optimization, 2026-02-19).
- **Status:** Disabled
- **Re-enable:** `openclaw cron enable e2735844`

### meta-supervisor-agent
- **Schedule:** Every hour at minute 5 (`5 * * * *`) in Asia/Bangkok
- **Original description:** Keepalive cron that ensures meta-supervisor daemon is running (spawns if not). Maintains continuous auditing.
- **Status:** Disabled
- **Re-enable:** `openclaw cron enable a1381566`

### linkedin-pa-agent-cron
- **Schedule:** Hourly (`0 * * * *`) in UTC
- **Original description:** Generates research‑oriented LinkedIn content about IBM Planning Analytics. Produces hourly posts with unique timestamps; rotates through 5 content types (technical analysis, trends, benchmarks, architecture, industry perspective). Outputs committed to Git and synced to Obsidian vault. Non‑promotional, focused on knowledge sharing.
- **Status:** Disabled
- **Re-enable:** `openclaw cron enable 7df39652`

## Maintenance Commands

- `quick cleanup-downloads [--days N] [--execute] [--verbose]` – Clean old downloads in `workspace/downloads/`.
- `quick cleanup-backups [--keep N] [--execute] [--verbose]` – Clean old backup tarballs in `/home/ubuntu/`. Keeps most recent N (default 1). Use with care.
- `quick cleanup-agent-artifacts [--execute] [--force]` – Clean stale agent artifacts (lock files, empty plans). Respects quiet hours unless `--force`.

Weekly automation:
- cleanup-downloads-cron (Sunday 06:00)
- backup-cleanup-cron (Sunday 07:00)
- cleanup-agent-artifacts-cron (Sunday 09:30)
