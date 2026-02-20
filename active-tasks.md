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

- [workspace-builder-20260220-1300] workspace-builder - Workspace hygiene: ignore meta-supervisor artifacts; clean temp; validate; commit (started: 2026-02-20 13:00 UTC, status: validated)
  - Verification: `./quick health` passed; `git status` clean; no untracked files; commit 0768b57 pushed; active-tasks.md <2KB.

