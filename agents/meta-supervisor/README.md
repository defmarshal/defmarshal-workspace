# Meta-Supervisor Agent

**Purpose:** Continuously verify that all scheduled agents are functioning according to their intended roles. Detect silent failures, no‑op runs, and outcome mismatches.

**Operation:** Runs as a daemon (`meta-supervisor-daemon.sh`) with an internal hourly loop. A keepalive cron (`meta-supervisor-agent`) starts it on boot and hourly to ensure it’s always running.

**How it works:**
1. Reads OpenClaw cron job definitions to know which agents exist and their expected schedules.
2. For each agent, inspects recent activity:
   - Last run timestamp and status (from `openclaw cron list --json`)
   - Presence of expected output artifacts (reports, logs, git commits, content files)
   - Whether the agent’s last run produced meaningful changes aligned to its purpose.
3. Generates a markdown daily report at `agents/meta-supervisor/reports/YYYY-MM-DD.md` with:
   - Agent status table (last run, duration, status)
   - Alerts and anomalies
   - Summary counts

**Agents monitored and their expected outputs:**

| Agent | Purpose | Expected Artifacts |
|-------|---------|-------------------|
| agni-cron | Brainstorm improvements | Plan file in `agents/agni/plans/` |
| rudra (spawned by agni) | Execute plans | Report `agents/rudra/reports/report-<timestamp>.md` and log `agents/rudra/logs/exec-<timestamp>.log` |
| dev-agent-cron | Develop tools/utilities | Git commits with `dev:` prefix; new/changed files |
| content-agent-cron | Publish content | New files in `content/` (daily digest, summaries) |
| research-agent-cron | Produce research reports | New files in `research/` with date prefix |
| workspace-builder | Strategic improvements | Build‑type commits and updated docs |
| supervisor-cron | Health monitoring | Entries in `memory/supervisor.log` |
| agent-manager-cron | Housekeeping | Cleanup actions, cron validation |
| vishwakarma-cron | Game planning | Plans in `agents/vishwakarma/plans/` |
| krishna (spawned) | Build games | New game directories under `games/` |
| meta-agent-cron | Meta‑tasks | Reindex logs, memory status updates |
| daily-digest-cron | Daily summary | `reports/<date>-daily-digest.md` |
| content-index-update-cron | Content index | `content/INDEX.md` refresh |
| git-janitor-cron | Auto‑commit/push | Git commits without manual intervention |
| memory-reindex-cron | Memory reindex | Reindex logs |
| log-rotate-cron | Rotate logs | Archived logs |
| cleanup-downloads-cron | Prune downloads | Removed old files |
| backup-cleanup-cron | Clean backups | Pruned old tarballs |
| auto-torrent-cron | Add anime torrents | New torrents added |
| cleanup-agent-artifacts-cron | Clean artifacts | Removed stale agent files |
| archiver-manager-cron | Manage archives | Created/rotated archives |

**Configuration:**
- `INTERVAL_MINUTES`: sleep between cycles (default 60)
- `STALENESS_HOURS`: max hours since last run before considered stale (default 4)
- Set via environment variables if needed.

**Outputs:**
- Logs: `agents/meta-supervisor/logs/meta-supervisor-daemon-YYYY-MM-DD_HHMM.log`
- PID: `agents/meta-supervisor/.meta-supervisor.pid`
- Reports: `agents/meta-supervisor/reports/report-YYYY-MM-DD.md` (updated each cycle)

**Cron jobs:**
- `meta-supervisor-agent` (runs at minute 5 of every hour) → spawns daemon if not running.
- The daemon itself runs the audit cycle every `INTERVAL_MINUTES`.

**Manual control:**
- Start: `nohup agents/meta-supervisor/meta-supervisor-daemon.sh > agents/meta-supervisor/meta-supervisor.nohup 2>&1 &`
- Stop: `kill $(cat agents/meta-supervisor/.meta-supervisor.pid)`
- Status: `ps -p $(cat agents/meta-supervisor/.meta-supervisor.pid)`

---

*Built 2026‑02‑20 by mewmew (◕‿◕)♡*