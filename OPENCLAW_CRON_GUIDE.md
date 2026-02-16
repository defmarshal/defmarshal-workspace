# OpenClaw Cron System — Comprehensive Guide

**Last updated**: 2026-02-16  
**Maintainer**: dev-agent  
**Scope**: All scheduled automation for the workspace

---

## 1. Overview

OpenClaw cron is the **primary scheduling system** for recurring workspace tasks. It replaces traditional system crontab with agent jobs that run in isolated OpenClaw sessions. Jobs are managed via `openclaw cron` CLI and stored in OpenClaw's internal database (`~/.openclaw/cron/`).

### Key Features

- **Isolated execution**: Each job runs in its own agent session with separate memory and workspace
- **Telegram announcements**: Job results are sent to the configured Telegram channel (id: 952170974)
- **Quiet hours awareness**: Jobs can respect the 23:00–08:00 Asia/Bangkok quiet window
- **Per-job logs**: Each job can append to a log file for auditability
- **Model selection**: Jobs can specify which LLM model to use (default: `openrouter/stepfun/step-3.5-flash:free`)

---

## 2. Job Catalog

### 2.1 Core Agent Jobs (Migrated from Daemons)

These jobs replaced persistent `*-agent-loop.sh` daemons on 2026‑02‑16. They run the same agent logic but as one‑shot executions on a schedule.

#### dev-agent-cron

- **Purpose**: Continuous development — scan workspace, implement utilities, fix deprecations, test, commit with `dev:` prefix
- **Schedule**: Every 20 minutes between 08:00–22:00 Asia/Bangkok  
  Cron: `0,20,40 8-22 * * *`
- **Payload**: `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/dev-cycle.sh >> dev-agent.log 2>&1'`
- **Log**: `dev-agent.log` (appended)
- **Model**: default
- **Timeout**: 600 seconds
- **Notes**: Respects quiet hours in agent code; produces commits with `dev:` prefix

#### content-agent-cron

- **Purpose**: Create anime summaries, tech writeups, daily digests
- **Schedule**: Every 10 minutes between 08:00–22:00 Asia/Bangkok  
  Cron: `0,10,20,30,40,50 8-22 * * *`
- **Payload**: `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/content-cycle.sh >> content-agent.log 2>&1'`
- **Log**: `content-agent.log` (appended)
- **Model**: default
- **Timeout**: 600 seconds
- **Notes**: Generates files in `content/`; updates `content/INDEX.md`

#### research-agent-cron

- **Purpose**: Conduct continuous research on anime, banking, tech, AI
- **Schedule**: Every 15 minutes between 08:00–22:00 Asia/Bangkok  
  Cron: `0,15,30,45 8-22 * * *`
- **Payload**: `bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/research-cycle.sh >> research-agent.log 2>&1'`
- **Log**: `research-agent.log` (appended)
- **Model**: default
- **Timeout**: 900 seconds
- **Notes**: Produces detailed reports in `research/`; updates `research/INDEX.md`

---

### 2.2 Maintenance & Utility Jobs

#### workspace-builder

- **Purpose**: Autonomous workspace improvement — analyze, implement, validate, commit with `build:` prefix
- **Schedule**: Every 2 hours (`0 */2 * * *`) in Asia/Bangkok
- **Payload**: agentTurn with strategic builder prompt (internal)
- **Model**: `openrouter/stepfun/step-3.5-flash:free`
- **Timeout**: 600 seconds
- **Log**: No dedicated log; output captured in agent session
- **Notes**: Uses planning-with-files; respects quiet hours

#### email-cleaner-cron

- **Purpose**: Auto-clean Gmail — archive promotional emails, apply labels
- **Schedule**: Daily at 09:00 Asia/Bangkok
- **Payload**: agentTurn executing `./quick email-clean` (dry‑run by default)
- **Log**: `memory/email-cleaner-cron.log`
- **Notes**: Add `--execute` flag to apply changes; manual override possible

#### auto-torrent-cron

- **Purpose**: Fetch top anime torrents and add to aria2 automatically
- **Schedule**: Daily at 02:00 Asia/Bangkok
- **Payload**: agentTurn running `./quick nyaa-top --limit 10 --max-size 2G --add`
- **Log**: `memory/auto-torrent.log`
- **Notes**: Uses Sukebei.Nyaa.si; filters by size; respects quiet hours

#### random-torrent-downloader

- **Purpose**: Randomly pick a torrent from top 20 (max 1GB) and download
- **Schedule**: Every 2 hours (`0 */2 * * *`) in UTC
- **Payload**: agentTurn executing `/bin/bash /home/ubuntu/.openclaw/workspace/cron/torrent-downloader.sh`
- **Log**: System logger (`logger -t torrent-downloader`)
- **Notes**: Respects quiet hours (23:00–08:00 Bangkok) and disk thresholds

#### traffic-report-cron

- **Purpose**: Generate daily traffic report
- **Schedule**: Daily at 22:00 UTC
- **Payload**: agentTurn executing `bash /home/ubuntu/.openclaw/workspace/traffic_report.sh`
- **Log**: None dedicated; output in agent session
- **Notes**: Likely sends to Telegram

#### content-index-update-cron

- **Purpose**: Regenerate `content/INDEX.md` to reflect current content files
- **Schedule**: Daily at 05:30 Asia/Bangkok
- **Payload**: agentTurn running `./quick content-index-update` and appending to `memory/content-index-cron.log`
- **Log**: `memory/content-index-cron.log`
- **Notes**: Keeps content archive index current

#### memory-reindex-cron

- **Purpose**: Reindex memory files to clear Voyage AI "dirty" flag and maintain search performance
- **Schedule**: Weekly on Sunday at 04:00 Asia/Bangkok (`0 4 * * 0`)
- **Payload**: agentTurn executing `./quick memory-index` and appending to `memory/memory-reindex.log`
- **Log**: `memory/memory-reindex.log`
- **Notes**: Addresses rate‑limit delays; partial success is okay

#### log-rotate-cron

- **Purpose**: Rotate `aria2.log` when >100 MB, keep up to 4 compressed archives
- **Schedule**: Weekly on Sunday at 05:00 Asia/Bangkok (`0 5 * * 0`)
- **Payload**: agentTurn executing `./quick log-rotate` and appending to `memory/log-rotate.log`
- **Log**: `memory/log-rotate.log`
- **Notes**: Prevents uncontrolled log growth

---

## 3. Managing OpenClaw Cron Jobs

### List Jobs

```bash
openclaw cron list
```

For JSON output (useful for scripts):

```bash
openclaw cron list --json | python3 -m json.tool
```

### View Job Details

```bash
openclaw cron list --json | jq '.[] | select(.name=="dev-agent-cron")'
```

### Update a Job

You can modify schedule, payload, or enabled state:

```bash
openclaw cron update --job dev-agent-cron --schedule '0,30 9-23 * * *'
```

Or change the payload (command):

```bash
openclaw cron update --job email-cleaner-cron --payload 'quick email-clean --execute'
```

### Enable / Disable

```bash
openclaw cron update --job auto-torrent-cron --enabled false  # disable
openclaw cron update --job auto-torrent-cron --enabled true   # enable
```

### Remove a Job

```bash
openclaw cron remove --job traffic-report-cron
```

**Caution**: Removing a job stops it permanently. Keep a backup of the configuration.

### Run a Job Manually (Immediate)

```bash
openclaw cron run --job memory-reindex-cron
```

Useful for testing or forcing an immediate run.

---

## 4. Job Configuration Reference

### Payload Types

- **agentTurn**: Run an agent cycle with a custom message or command. This is what we use for all jobs.
- **systemEvent**: Inject a text event into the main session (used for reminders/notifications).

### Schedule Formats

- **Cron expression**: `* * * * *` (minute hour day month weekday)
- **Every**: `{"kind":"every","everyMs":3600000}` (interval in milliseconds)
- **At**: `{"kind":"at","at":"2026-02-17T09:00:00Z"}` (one‑shot)

We use cron expressions exclusively for clarity.

### Timezones

- Schedules specify a timezone (Asia/Bangkok or UTC as shown).
- OpenClaw cron respects timezone when computing next run.
- **Best practice**: Use the local timezone (Asia/Bangkok) for workspace‑centric tasks; UTC for system‑wide coordination.

---

## 5. Logging & Observability

Each job can write to a log file via its payload. We organize logs in two places:

1. **Memory‑indexed logs**: `memory/*.log` — these are captured by the memory system and searchable
2. **Workspace logs**: `dev-agent.log`, `content-agent.log`, `research-agent.log` — agent‑specific output

### View Job Logs

```bash
# Memory‑indexed logs
ls -ltr memory/*.log

# Tail a specific log
tail -f memory/email-cleaner-cron.log

# Agent logs
tail -f dev-agent.log
```

### Check Job History

OpenClaw cron stores run history. Use:

```bash
openclaw cron runs --job dev-agent-cron --limit 10
```

(Requires OpenClaw CLI support; may need `--json`)

---

## 6. Quiet Hours Integration

All agent jobs (dev, content, research) include logic to **skip execution** if current time is within quiet hours (23:00–08:00 Asia/Bangkok). This is implemented in the agent loop scripts (`agents/*-cycle.sh`) by checking the time before spawning the agent session.

Additionally, `random-torrent-downloader` and `auto-torrent-cron` also respect quiet hours via their wrapper scripts.

**Important**: Quiet hours check is **local to the script**. If you modify a payload to bypass these scripts, you could violate quiet hours. Keep the wrappers intact.

---

## 7. Migration History

| Date | Change |
|------|--------|
| 2026‑02‑16 | Migrated dev‑agent, content‑agent, research‑agent from persistent daemons to OpenClaw cron (jobs 9‑11). Updated `start-background-agents.sh` to no longer launch daemons. |
| 2026‑02‑16 | Converted 5 system cron jobs to OpenClaw cron: email‑cleaner, auto‑torrent, random‑torrent, traffic‑report, content‑index‑update, memory‑reindex, log‑rotate (jobs 2‑8). System crontab now only has `@reboot` starter. |

---

## 8. Troubleshooting

### Job Not Running

1. Check if job is enabled: `openclaw cron list --json | jq '.[] | select(.name=="jobname") | .enabled'`
2. Verify schedule: `openclaw cron list --json | jq '.[] | select(.name=="jobname") | .schedule'`
3. Look at recent runs: `openclaw cron runs --job jobname --limit 5`
4. Check agent logs: `tail -n 50 dev-agent.log` etc.

### Job Failing Repeatedly

- Inspect the job's dedicated log (if any) in `memory/`
- Check system resources (disk, memory)
- Run the payload manually to reproduce:  
  `bash -c 'cd /workspace && ./agents/dev-cycle.sh'`
- Look for errors in the agent logs

### Overlapping Runs

If a job takes longer than its interval, you may get concurrent instances. We mitigate this by:
- Keeping intervals > expected runtime (dev 20 min, content 10 min, research 15 min)
- Using lockfiles in scripts if needed (future enhancement)

To force‑kill a runaway job:
```bash
openclaw sessions list --json | jq -r '.[] | select(.label|contains("dev-agent-cron")) | .key' | xargs -r openclaw sessions kill --sessionKey
```

---

## 9. Backup & Recovery

OpenClaw cron configuration is stored in:
```
~/.openclaw/cron/
```

**Backup procedure**:
```bash
tar czf openclaw-cron-backup-$(date +%F).tar.gz ~/.openclaw/cron/
```

**Restore**:
```bash
# Stop OpenClaw gateway
systemctl --user stop openclaw-gateway.service
# Replace cron directory
rm -rf ~/.openclaw/cron
tar xzf openclaw-cron-backup-YYYY-MM-DD.tar.gz -C ~/.openclaw/
# Restart gateway
systemctl --user start openclaw-gateway.service
```

**Note**: Job logs are **not** stored in `~/.openclaw/cron/`; they reside in workspace files (`memory/*.log`, `*-agent.log`). Back up those separately if needed.

---

## 10. Best Practices

1. **Use wrapper scripts** (`agents/*-cycle.sh`) for complex logic; keep payload simple
2. **Log to workspace** (append to files) for long‑term auditability
3. **Respect quiet hours** — always check time before doing noisy work
4. **Set appropriate timeouts** — 600s for dev/content, 900s for research
5. **Monitor logs regularly** — at least weekly via `quick agent-logs` or `quick health`
6. **Document changes** — update this file whenever adding, modifying, or removing jobs
7. **Test manually** — use `openclaw cron run --job <name>` after changes

---

## 11. Quick Reference Table

| Job Name | Schedule (Bangkok) | Log | Timeout |
|----------|-------------------|-----|---------|
| dev-agent-cron | 0,20,40 8-22 * * * | dev-agent.log | 600s |
| content-agent-cron | 0,10,20,30,40,50 8-22 * * * | content-agent.log | 600s |
| research-agent-cron | 0,15,30,45 8-22 * * * | research-agent.log | 900s |
| workspace-builder | 0 */2 * * * | (session) | 600s |
| email-cleaner-cron | 0 9 * * * | memory/email-cleaner-cron.log | 600s |
| auto-torrent-cron | 0 2 * * * | memory/auto-torrent.log | 600s |
| random-torrent-downloader | 0 */2 * * * (UTC) | system logger | 600s |
| traffic-report-cron | 0 22 * * * (UTC) | (session) | 600s |
| content-index-update-cron | 30 5 * * * | memory/content-index-cron.log | 600s |
| memory-reindex-cron | 0 4 * * 0 | memory/memory-reindex.log | 600s |
| log-rotate-cron | 0 5 * * 0 | memory/log-rotate.log | 600s |

---

## 12. Future Enhancements

- [ ] Add per‑job success/failure metrics to a dashboard
- [ ] Implement automatic backoff on repeated failures
- [ ] Create a `quick cron-status` command summarizing last run times and durations
- [ ] Add email/SMS alerting for critical job failures
- [ ] Archive old logs automatically with rotation policy

---

*Maintained by dev-agent. Update this document when cron configuration changes.* (◕‿◕)♡
