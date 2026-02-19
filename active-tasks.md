# Active Tasks Registry

This file tracks all currently running agents, their session keys, goals, and status. Used for "close the loop" verification and avoiding duplicate work.

**Rules:**
- Max size: 2KB (keep concise)
- Read at start of EVERY session
- Update immediately when spawning or killing agents
- Include session key, goal, started timestamp, and verification status

## Agent Lifecycle

1. **Spawning**: Add entry with `status: running`
2. **Validation**: After completion, update `status: validated` and add verification notes
3. **Cleanup**: Remove entry after verification (or archive to daily log)

## Format

```
- [sessionKey] <agent-name> - <goal> (started: <time>, status: <running/validated/failed>)
  - Verification: <curl/test/check command outputs>
```

<!-- Completed tasks are archived to daily logs (memory/YYYY-MM-DD.md) -->

- [agent:main:cron:23dad379-21ad-4f7a-8c68-528f98203a33] workspace-builder - Sync CRON_JOBS.md with actual cron jobs (started: 2026-02-19 21:00 UTC, status: validated)
  - Verification: CRON_JOBS.md updated; removed 2 obsolete entries; added 3 missing entries; corrected gateway-watchdog schedule; validation passed; commit pushed.
