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

*(none)*

<!-- Completed tasks are archived to daily logs (memory/YYYY-MM-DD.md) -->

## Completed (Feb 18)

- [build] workspace-builder - Fix cron misconfig; validate system; maintain active-tasks (started: 2026-02-18 16:00 UTC, status: validated; session: agent:main:cron:23dad379)
  - Verification: 8 cron jobs corrected; schedules match CRON_JOBS.md; health OK (disk 40%, gateway healthy); memory main clean (15f/56c dirty=False); quick mem/search functional; no temp files; active-tasks.md 890B; git push succeeded.
