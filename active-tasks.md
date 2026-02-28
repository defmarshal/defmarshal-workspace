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

- [workspace-builder-20260228-0306] workspace-builder - Strategic maintenance - prune active-tasks, memory reindex, branch hygiene, doc updates (started: 2026-02-28 03:06 UTC, status: validated)
  - Verification: active-tasks 1272b (<2KB), MEM29, ✅ health green, memory reindexed, ✅ branch hygiene, TOOLS updated; commit a4d6d3c1 pushed; all constraints green except git (dirty pre-commit, now clean); no temp files ✅
