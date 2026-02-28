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

- [workspace-builder-23dad379] workspace-builder - Enforce constraints, commit planning docs, validate system (started: 2026-02-28 23:01 UTC, status: running)
  - Verification: pending final validation

- [meta-supervisor-daemon] meta-supervisor - Continuous agent outcome auditor (started: 2026-02-28 02:00 UTC, status: running)
  - Verification: daemon process PID 1121739; log shows cycle started; sleeping until next interval
