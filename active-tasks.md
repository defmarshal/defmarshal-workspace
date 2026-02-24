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

*(none — all agents validated/cleaned)*

- [workspace-builder-20260224-0505] workspace-builder - Enhance git-janitor auto-commit patterns and add idea branch cleanup (started: 2026-02-24 05:05 UTC, status: validated)
  - Verification: health OK; git-janitor test OK; active-tasks<2K; MEM30

- [meta-agent-20260224-0509] meta-agent - Autonomous planning cycle (started: 2026-02-24 05:09 UTC, status: validated)
  - Verification: snapshot OK; content=13, research=1; no actions; active-tasks<2K; MEM30

- [meta-agent-20260224-0322] meta-agent - Autonomous planning cycle (started: 2026-02-24 03:22 UTC, status: validated)
  - Verification: snapshot OK; content=9, research=1; no actions; active-tasks<2K; MEM30

- [workspace-builder-20260224-0306] workspace-builder - Fixed validate-cron-schedules.sh JSON parsing (started: 2026-02-24 03:06 UTC, status: validated)
  - Verification: quick cron-schedules exits 0; active-tasks<2K; MEM30

- [workspace-builder-20260224-0107] workspace-builder - Fixed JSON parsing in quick commands (agent-status, cron*), CRLF false positive (started: 2026-02-24 01:07 UTC, status: validated)
  - Verification: agent-status/cron-fixes, CRLF fix; active-tasks<2K; MEM30

- [workspace-builder-20260223-2300] workspace-builder - Prune active-tasks ≤2KB (started: 2026-02-23 23:00 UTC, status: validated)
  - Verification: OK; 1622b; MEM30; git clean
