# Workspace Builder Findings
**Date**: 2026-02-16 (23:00 UTC run)
**Focus**: System reliability, maintenance automation, log rotation, updates workflow

## Current System State

### Disk & Storage
- Total: 45G, Used: 34.5G (77%), Free: 10.5G (healthy)
- Downloads: 10 files, 2.1G (all <30 days)
- Backups: 1 remaining backup tarball (2.2G) in /home/ubuntu
- Agent logs: dev-agent.log (211K), content-agent.log (200K), research-agent.log (181K) — growing over time

### Pending Updates
- 7 packages upgradable via apt (security/bugfix)
- No automated update mechanism; manual `apt upgrade` required

### Service Persistence
- openclaw-gateway runs as user service (systemd --user)
- Without systemd linger, gateway and any subagents stop on user logout/reboot
- This has been mitigated by using cron jobs instead of persistent daemons for periodic tasks
- However, the gateway itself still stops on logout/reboot unless linger enabled
- During outages, cron jobs may queue or skip; overall reliability could improve with linger

### Cron Jobs
- OpenClaw cron: 12 jobs (all documented in CRON_JOBS.md)
- System crontab: only @reboot agent startup hook (no other workspace crons)
- All expected jobs running; no duplicates

### Memory System
- openclaw-memory: 7 files / 44 chunks (clean)
- Provider: Voyage AI with FTS (full-text search) enabled
- Index status: clean (dirty=no)
- Reindex scheduled weekly (Sunday 04:00 Asia/Bangkok)

## Identified Improvements

### High Priority
1. **Enable systemd linger** — one-time sudo action to keep user services alive across logout/reboot. Improves gateway uptime and reduces missed cron runs due to offline state.
2. **Schedule backup cleanup** — add cron job for weekly backup rotation to prevent accumulation of large tarballs. Script exists (`cleanup-backups.sh`), just needs scheduling.
3. **Rotate agent logs** — extend `log-rotate` to include dev-agent.log, content-agent.log, research-agent.log. Prevent unbounded growth. Already have log-rotate cron (weekly Sunday 05:00 Bangkok).
4. **Updates management** — provide safe commands to check and apply system updates. Currently no dedicated quick commands; users must run apt manually.

### Medium Priority
5. **Archive or clean previous builder artifacts** — previous builder left planning files (task_plan.md, findings.md, progress.md) which are now outdated; this new run will overwrite them. Could consider archiving to a builds/ directory after each run for audit trail.
6. **Add memory reindex alert** if dirty flag persists beyond expectation (rate-limit issues). Already have reindex-check command.

### Low Priority
7. **Monitor cron job failures** — currently logs per job but no central alerting.
8. **Optimize Voyage rate-limit handling** — maybe auto-retry with backoff in openclaw-memory? Out of scope.

## Recommendations

### systemd linger
- Run: `sudo loginctl enable-linger ubuntu`
- Verify: `loginctl show-user ubuntu -p Linger`
- Impact: Gateway service persists across logout/reboot; cron jobs continue to run even if user session not active.

### Backup cleanup cron
- Add OpenClaw cron job: weekly Sunday 07:00 Asia/Bangkok
- Payload: agentTurn executing `./quick cleanup-backups --execute --keep 1`
- Rationale: Aligns with other maintenance tasks; runs after downloads cleanup (06:00) and before log-rotate (05:00?) Actually check order: Sunday schedule currently: memory-reindex 04:00, log-rotate 05:00, cleanup-downloads 06:00. So backup cleanup at 07:00 is fine.
- Ensure job doesn't conflict with quiet hours (none now).

### Agent log rotation
- Modify `scripts/log-rotate` (or create separate script) to:
  - Find agent logs in workspace root: dev-agent.log, content-agent.log, research-agent.log
  - If size > 1MB, compress to .gz and truncate original (copytruncate)
  - Keep up to 4 compressed archives per log
- Schedule: already covered by weekly log-rotate cron; just extend the existing script.

### Updates commands
- `scripts/updates-check.sh`: outputs list of upgradable packages (human-readable count and names)
- `scripts/updates-apply.sh`: runs `sudo apt update && sudo apt upgrade -y` with dry-run option default
- Add to quick launcher as subcommands.
- Document that these affect the system globally; use with care.
- Could also schedule automatic updates, but better to keep manual for now.

## Risks & Mitigations

- Linger: minimal risk; just allows user services to start at boot. Already a systemd feature.
- Backup cleanup cron: ensure script uses absolute paths; add logging to memory/backup-cleanup.log.
- Log rotation: copytruncate is safe for processes writing to logs (they continue writing to same file descriptor but file resets to zero; some log loss possible but minimal on weekly rotation. Alternatively send HUP signal to processes? But agents may not handle it. Simpler: copytruncate.
- Updates apply: could break something; always dry-run first, then apply only when ready. Keep manual.

## Open Questions

- Should we also rotate other logs (aria2.log already rotated, gateway logs)? Already done.
- Should we consolidate all maintenance into a single weekly "maintenance window" cron? Possibly but not necessary.

## Follow-up

After implementation, update MEMORY.md with this build's summary. Consider adding a `builds/` directory to archive planning files from each run (with timestamps) to keep workspace root clean while preserving history.
