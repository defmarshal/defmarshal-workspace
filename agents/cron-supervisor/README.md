# Cron Supervisor Agent

Monitors and manages OpenClaw cron jobs, providing health overview and failure alerts.

## Purpose

- Continuously checks all cron job statuses (lastStatus, consecutiveErrors, nextRun)
- Reports health summary every 5 minutes to stdout and syslog
- Helps detect stuck or failing cron jobs early
- Runs 24/7 as a daemon (via `loop.sh`)

## Files

- `agent.json` — Agent definition (allowlists for shell.exec)
- `main.py` — Python monitoring logic
- `loop.sh` — Daemon loop that respawns the agent if missing

## Behavior

- Interval: 5 minutes (configurable in `main.py` via `INTERVAL`)
- Output: Human-readable report printed to stdout (captured by OpenClaw session) and logged to syslog (`logger -t cron-supervisor`)
- No external dependencies beyond `openclaw` CLI and `jq` (installed)

## Sample Report

```
=== Cron Supervisor Report (2026-02-18 02:30:00 UTC) ===

Summary: 12/12 jobs healthy

✓ email-cleaner-cron
    Last: ok | Errors: 0 | Next: 2026-02-18 09:00 UTC | enabled
✓ auto-torrent-cron
    Last: ok | Errors: 0 | Next: 2026-02-19 02:00 ICT | enabled
...
=== End Report ===
```

## Startup

- Included in `start-background-agents.sh` — starts automatically on boot (or after `openclaw gateway restart`)
- Manual start: `./agents/cron-supervisor/loop.sh` (runs in background)

## Notes

- This agent does NOT modify cron jobs; it only monitors and reports.
- To take action on failures, extend `main.py` to call `openclaw cron run --id <job>` or send alerts.
- All cron configuration remains in `~/.openclaw/cron/jobs.json`.
