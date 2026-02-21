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

- [workspace-builder-20260221-0300] workspace-builder - Idea executor validation + monthly digest feature (started: 2026-02-21 03:00 UTC, status: validated)
  - Verification: idea executor validation added; monthly digest created and tested; health OK; no temp files.

- [workspace-builder-20260221-0100] workspace-builder - Meta-agent fix validation and debounce improvement (started: 2026-02-21 01:00 UTC, status: validated)
  - Verification: meta-agent --once completed; ./quick health OK; git clean; active-tasks.md <2KB; meta-agent fix commit 9519b2e present and pushed; debounce logic implemented and tested.

- [meta-agent-20260220-2313] meta-agent - One-shot evaluation; system stable (started: 2026-02-20 23:13 UTC, status: validated)
  - Verification: git status clean; meta-agent log shows no actions taken; health snapshot: disk=49%, apt=0, content_today=6, research_today=8.


