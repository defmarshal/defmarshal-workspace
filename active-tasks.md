# Active Tasks Registry

This file tracks all currently running agents, their session keys, goals, and status. Used for "close the loop" verification and avoiding duplicate work.

**Rules:**
- Max size: 2KB (keep concise)
- Read at start of EVERY session
- Update immediately when spawning or killing agents
- Include session key, goal, started timestamp, and verification status

## Format

```
- [sessionKey] <agent-name> - <goal> (started: <time>, status: <running/validated/failed>)
  - Verification: <curl/test/check command outputs>
```

<!-- Completed tasks are archived to daily logs (memory/YYYY-MM-DD.md) -->

## Currently Running

- [23dad379-21ad-4f7a-8c68-528f98203a33] workspace-builder - Documentation cleanup and system validation (started: 2026-02-20 05:00 UTC, status: validated)
  - Verification: health OK (Disk 43%, Gateway healthy, Memory clean), cron-status OK, markdown syntax intact, all changes pushed.
