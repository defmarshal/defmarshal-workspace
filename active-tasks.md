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

- [workspace-builder-20260223-0945] workspace-builder - Idea generator quality improvements and executor validation (started: 2026-02-23 09:08 UTC, status: validated)
  - Verification: health OK (disk 66%, gateway healthy, memory clean); generator: deduplication + substantive steps (printf); executor test: first idea succeeded (ins=4, valid); no stale branches; planning docs updated; git clean after commit; active-tasks.md size 1728 bytes

- [workspace-builder-20260223-0700] workspace-builder - Workspace hygiene: delete stale idea branch, fix MEMORY.md date (started: 2026-02-23 07:00 UTC, status: validated)
  - Verification: health OK; git clean after commit; stale branch `idea/build-a-quick-command-that` deleted; MEMORY.md 34 lines; active-tasks.md <2KB; planning files updated and pushed

- [workspace-builder-20260223-0500] workspace-builder - Strategic analysis and bugfix (started: 2026-02-23 05:00 UTC, status: validated)
  - Verification: health OK; git clean after commit; MEMORY.md updated (34 lines); active-tasks.md <2KB