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

## Recently Completed

- [workspace-builder-20260221-2300] workspace-builder - Fix agent-manager-cron timeout and validate (started: 2026-02-21 23:00 UTC, status: validated)
  - Verification: agent-manager timeout set to 900s; manual run OK; health OK; pushed.

- [workspace-builder-20260221-2100] workspace-builder - Hygiene: archive tasks, cleanup temp files, delete stale branch, enhance docs, validate (started: 2026-02-21 21:00 UTC, status: validated)
  - Verification: health OK; CRON_JOBS.md.bak removed; stale branch idea/create-a-health-check-for deleted; agents/ideas/README.md added; active-tasks.md pruned; memory/2026-02-21.md updated; git clean; all pushed.



