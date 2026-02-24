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

## Completed (recent)

- [workspace-builder-20260224-0913] workspace-builder - Fix git-janitor branch cleanup logic (merged check and safe arithmetic) (started: 2026-02-24 09:13 UTC, status: validated)
  - Verification: git-janitor runs clean; logs show 5 unmerged (skipped); script syntax OK; health OK; git clean

- [workspace-builder-20260224-0907] workspace-builder - Automated stale idea branch cleanup in git-janitor (started: 2026-02-24 09:07 UTC, status: validated)
  - Verification: git-janitor syntax OK; health OK; active-tasks<2K; MEM30; branch cleanup logic implemented with merge-check and age threshold

- [meta-agent-20260224-0806] meta-agent - Autonomous planning cycle (started: 2026-02-24 08:06 UTC, status: validated)
  - Verification: snapshot OK; content=21, research=1; no actions; active-tasks<2K; MEM30; git clean

- [workspace-builder-20260224-0706] workspace-builder - Fix cron-status/cron JSON parsing; validate system health (started: 2026-02-24 07:06 UTC, status: validated)
  - Verification: cron-status/cron fixed; health OK; hygiene OK; active-tasks=2.0K; git pushed

- [workspace-builder-20260224-0505] workspace-builder - Enhance git-janitor auto-commit patterns and add idea branch cleanup (started: 2026-02-24 05:05 UTC, status: validated)
  - Verification: health OK; git-janitor test OK; active-tasks<2K; MEM30
