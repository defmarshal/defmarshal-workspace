# Meta-Supervisor Agent

**Purpose:** Continuously verify that all scheduled agents are functioning according to their intended roles. Detect silent failures, no‑op runs, and outcome mismatches.

**How it works:**
1. Reads OpenClaw cron job definitions to know which agents exist and their expected schedules
2. For each agent, inspects recent activity:
   - Last run timestamp and status (from `openclaw cron list --json`)
   - Presence of expected output artifacts (reports, logs, git commits, content files)
   - Whether the agent’s last run produced meaningful changes aligned to its purpose
3. Generates a daily summary report and raises alerts for:
   - Agents that haven’t run recently (stale)
   - Agents that ran but produced no output or no meaningful work
   - Agents that produced output not matching their intended function
4. Writes findings to `agents/meta-supervisor/reports/YYYY-MM-DD.md`
5. Optionally sends Telegram notification for critical issues

**Agents monitored and their expected outputs:**

| Agent | Purpose | Expected Artifacts |
|-------|---------|-------------------|
| agni-cron | Brainstorm improvements | Plan file in `agents/agni/plans/` (timestamped after run) |
| rudra (spawned by agni) | Execute plans | Report `agents/rudra/reports/report-<timestamp>.md` and log `agents/rudra/logs/exec-<timestamp>.log` |
| dev-agent-cron | Develop tools/utilities | Git commits with `dev:` prefix; new/changed files in `agents/`, `quick`, scripts |
| content-agent-cron | Publish content | New files in `content/` (daily digest, summaries) |
| research-agent-cron | Produce research reports | New files in `research/` with date prefix |
| workspace-builder | Strategic improvements | Build‑type commits and updated docs |
| supervisor-cron | Health monitoring |Entries in `memory/supervisor.log` and periodic health checks |
| agent-manager-cron | Housekeeping | Cleanup actions, cron validation |
| vishwakarma-cron | Game planning | Plans in `agents/vishwakarma/plans/` |
| krishna (spawned) | Build games | New game directories under `games/` |
| meta-agent-cron | Meta‑tasks (memory, indexing) | Reindex logs, memory status updates |

**Configuration:** Reads `openclaw.json` agents list and cron definitions. Custom thresholds:
- `STALENESS_HOURS`: max hours since last run before considered stale (default 4)
- `MIN_OUTPUT_CHANGES`: minimum number of changed files to consider a run productive (default 1)

**Outputs:** Markdown daily reports saved under `agents/meta-supervisor/reports/YYYY-MM-DD.md` with sections:
- Agent status table (last run, duration, status)
- Alerts and anomalies
- Suggestions for manual review

**Cron schedule:** Runs hourly via OpenClaw cron `meta-supervisor-cron` (to be added).

**Run manually:** `./agents/meta-supervisor/meta-supervisor-cycle.sh`

---

*Built 2026‑02‑20 by mewmew (◕‿◕)♡*
