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

- [meta-supervisor-daemon] meta-supervisor - Continuous agent outcome auditor (started: 2026-02-24 10:12 UTC, status: running)
  - Verification: daemon process PID 3376045; nohup log active; cycle completed

## Completed (recent)

- [workspace-builder-20260224-0913] workspace-builder - Fix git-janitor branch cleanup logic (merged check and safe arithmetic) (started: 2026-02-24 09:13 UTC, status: validated)
  - Verification: active-tasks<2K, MEM30, health OK, git clean

- [workspace-builder-20260224-0907] workspace-builder - Automated stale idea branch cleanup in git-janitor (started: 2026-02-24 09:07 UTC, status: validated)
  - Verification: active-tasks<2K, MEM30, health OK, branch cleanup OK

- [meta-agent-20260224-0806] meta-agent - Autonomous planning cycle (started: 2026-02-24 08:06 UTC, status: validated)
  - Verification: active-tasks<2K, MEM30, health OK, git clean, no actions


- [workspace-builder-20260224-1113] workspace-builder - Workspace hygiene: push daily digest, delete 5 stale idea branches, prune active-tasks (started: 2026-02-24 11:06 UTC, status: validated)
  - Verification: active-tasks=1531b, MEM30, health OK, git clean, no temp files, idea branches cleared
