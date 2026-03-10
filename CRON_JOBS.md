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

2. **workspace-builder**
   - **Schedule**: Every 2 hours (`0 */2 * * *`) in Asia/Bangkok
   - **Payload**: agentTurn with strategic builder prompt
   - **Model**: `stepfun/step-3.5-flash:free`
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
   - **Model**: `qwen/qwen3-coder:free`
   - **Description**: Performs one dev-agent cycle (scan workspace, implement utilities, commit with 'dev:' prefix). Includes retry logic for transient OpenRouter rate limits. Reduced from every 20 min to hourly (token optimization, 2026-02-19).

9. **content-agent-cron**
   - **Schedule**: Hourly between 08:00-22:00 Asia/Bangkok (`0 8-22 * * *`)
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/content-cycle.sh >> content-agent.log 2>&1'`
   - **Model**: `meta-llama/llama-3.3-70b-instruct:free`
   - **Description**: Performs one content-agent cycle (create anime summaries, tech writeups, digests). Includes retry logic for transient OpenRouter rate limits. Reduced from every 10 min to hourly (token optimization, 2026-02-19).

10. **research-agent-cron**
   - **Schedule**: Hourly between 08:00-22:00 Asia/Bangkok (`0 8-22 * * *`)
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/research-cycle.sh >> research-agent.log 2>&1'`
   - **Model**: `qwen/qwen3-coder:free`
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
    - **Schedule**: Every 2 hours (`0 */2 * * *`) in UTC
    - **Implementation**: System crontab (`crontab -l`) running `./agents/meta-agent.sh --once`
    - **Log**: `memory/meta-agent.log`
    - **Delivery**: None (previously Telegram announcements; suppressed to avoid OpenRouter rate limits)
    - **Description**: Autonomous planner that observes system health, decides on maintenance/improvement actions, spawns sub‑agents to execute them, validates outcomes, and commits changes with `meta:` prefix. Core of the self‑extending system.
    - **Notes**: Migrated from `agentTurn` to system cron on 2026-03-10 to eliminate unnecessary OpenRouter API usage. Child agent spawns use `openclaw agent` with rate limit backoff (`spawn_agent_safe`).

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

27. **email-categorizer-cron**
   - **Schedule**: Every hour (`0 * * * *`) in UTC (stagger 5m)
   - **Payload**: agentTurn executing `cd /home/ubuntu/.openclaw/workspace && BATCH_SIZE=50 PAGES_PER_RUN=4 python3 agents/email_sweep.py`
   - **Log**: `memory/email-categorizer.log`
   - **Description**: Sweeps unread emails via Maton API, applies labels based on sender mapping, marks as read. Processes up to 50 messages per page for up to 4 pages per run. Maintains state in `memory/email-categorizer.state`. No Telegram notifications (delivery: none).
   - **Status**: Enabled (running)

28. **dashboard-data-updater**
   - **Schedule**: Every 5 minutes (`*/5 * * * *`) in Asia/Bangkok
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./scripts/generate-dashboard-data.sh >> memory/dashboard-data.log 2>&1'`
   - **Log**: `memory/dashboard-data.log`
   - **Description**: Refreshes `apps/dashboard/data.json` with latest system stats, agent sessions, recent commits, cron jobs, heartbeat state, and supervisor log tail. Provides real-time data for the web dashboard.
   - **Status**: Enabled (switched to bash script 2026-03-02; Python version deprecated)

29. **mewchat-evolver-cron**
   - **Schedule**: Every 6 hours (`0 */6 * * *`) in UTC
   - **Payload**: agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/mewchat-evolver.sh >> memory/mewchat-evolver.log 2>&1'`
   - **Log**: `memory/mewchat-evolver.log`
   - **Description**: Autonomous agent that continuously improves the MewChat web app (UX, performance, features, code quality). Runs every 6 hours; each cycle performs one focused improvement, commits, and logs.

30. **meta-supervisor-agent**
   - **Schedule:** Every hour at minute 5 (`5 * * * *`) in Asia/Bangkok
   - **Payload:** agentTurn that ensures the meta-supervisor daemon is running. Command: `bash -c 'cd /home/ubuntu/.openclaw/workspace && nohup agents/meta-supervisor/meta-supervisor-daemon.sh > agents/meta-supervisor/meta-supervisor.nohup 2>&1'`
   - **Description:** Keepalive cron that spawns the meta-supervisor daemon if not running, ensuring continuous auditing of agent outcomes.
   - **Agent:** default

31. **log-rotate-system-cron** (System Crontab)
   - **Schedule:** Daily at 02:00 (`0 2 * * *`) in system timezone (UTC)
   - **Command:** `/home/ubuntu/.openclaw/workspace/scripts/rotate-logs.sh`
   - **Log:** `memory/rotate-logs.log`
   - **Description:** Rotates and compresses memory logs. Compresses files >10MB or older than 1 day to `memory/archive/`, keeping last 1000 lines uncompressed. Uses flock to avoid conflicts with writing processes. Safe for live systems.

32. **linkedin-pa-agent-cron**
   - **Schedule:** Hourly (`0 * * * *`) in UTC (stagger 5m)
   - **Payload:** agentTurn executing `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/linkedin-pa-agent.sh >> memory/linkedin-pa-agent.log 2>&1'`
   - **Model:** `qwen/qwen3-coder:free`
   - **Log:** `memory/linkedin-pa-agent.log`
   - **Description:** Generates research‑oriented LinkedIn content about IBM Planning Analytics. Produces hourly posts with unique timestamps; rotates through 6 content types (market-positioning, technical-performance, comparative-analysis, implementation-decoder, roadmap-brief, developer-tips). Outputs committed to Git and synced to Obsidian vault. Non‑promotional, focused on knowledge sharing. Uses direct OpenRouter API to avoid cron hangs.

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



## Maintenance Commands

- `quick cleanup-downloads [--days N] [--execute] [--verbose]` – Clean old downloads in `workspace/downloads/`.
- `quick cleanup-backups [--keep N] [--execute] [--verbose]` – Clean old backup tarballs in `/home/ubuntu/`. Keeps most recent N (default 1). Use with care.
- `quick cleanup-agent-artifacts [--execute] [--force]` – Clean stale agent artifacts (lock files, empty plans). Respects quiet hours unless `--force`.

Weekly automation:
- cleanup-downloads-cron (Sunday 06:00)
- backup-cleanup-cron (Sunday 07:00)
- cleanup-agent-artifacts-cron (Sunday 09:30)

### telegram-slash-handler
- **Schedule:** Every 2 minutes
- **Job ID:** e26c12bd-635a-48cf-bc8d-1707bc4ffd59
- **Description:** Polls the main Telegram session for slash commands (/status, /health, /downloads, /cron, /disk, /help) and responds with output from `./quick` commands. Script: `agents/slash-handler.sh`. State tracked in `memory/.slash-handler-state.json`.
- **Status:** Enabled

### youtube-digest-daily
- **Schedule:** Daily 02:00 UTC (= 09:00 Asia/Bangkok)
- **Job ID:** c6976c90-df08-4ac2-997a-a4a53be6c23c
- **Description:** Fetches YouTube subscriptions via OAuth, checks for new uploads in the last 24h, generates a markdown digest with content previews/transcripts, and sends it to Telegram. Script: `scripts/youtube-digest.sh`. Credentials: `config/youtube-credentials.json` (gitignored). Run `scripts/youtube-oauth-setup.sh` to configure OAuth.
- **Status:** Enabled (will skip gracefully if credentials not yet set up)
