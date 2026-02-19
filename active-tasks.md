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

## Current Active Tasks

- [agent:main:cron:23dad379-21ad-4f7a-8c68-528f98203a33] workspace-builder - Strategic improvements (started: 2026-02-19 17:10 UTC, status: validated)
  - Verification: fixed cron validation script (LOGFILE, edit command); supervisor-cron schedule corrected to */5; all schedules match docs; active-tasks.md 1030B; health OK; memory clean; git clean; no temp files.

<!-- Completed tasks are archived to daily logs (memory/YYYY-MM-DD.md) -->
