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

## Running

- [meta-supervisor-daemon] meta-supervisor - Continuous agent outcome auditor (started: 2026-02-28 02:00 UTC, status: running)
  - Verification: daemon process PID 1121739; log shows cycle started; sleeping until next interval
- [23dad379-21ad-4f7a-8c68-528f98203a33] workspace-builder - Routine maintenance (started: 2026-03-01 05:14 UTC, status: validated)
  - Verification: active-tasks 1275b (<2KB), MEM 31 lines, health green, reindex 1d fresh, git clean & pushed (f2aade1c), planning docs committed, daily logs updated, no temp files, branch hygiene ✅, downloads 31 files 7.6GB, constraints all ✅
