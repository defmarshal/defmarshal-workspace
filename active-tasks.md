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

- [workspace-builder-20260223-1909] workspace-builder - Commit capability evolver cycle #0003 artifacts (started: 2026-02-23 19:09 UTC, status: validated)
  - Verification: health OK; evolver artifacts committed; git clean; active-tasks<2KB; MEMORY 30l; no temp files

- [workspace-builder-20260223-1711] workspace-builder - Workspace hygiene cleanup (started: 2026-02-23 17:11 UTC, status: validated)
  - Verification: active-tasks committed; stale branch deleted; health OK; MEMORY 30l; active-tasks<2KB; git clean

- [workspace-builder-20260223-0945] workspace-builder - Idea generator quality improvements and executor validation (started: 2026-02-23 09:08 UTC, status: validated)
  - Verification: health OK; generator improvements; executor test passed; no stale branches

- [workspace-builder-20260223-1309] workspace-builder - Finalize pending changes: commit daily digest and remove obsolete sync script (started: 2026-02-23 13:09 UTC, status: validated)
  - Verification: health OK; active-tasks<2KB; MEMORY 30l; git clean; no temp files
