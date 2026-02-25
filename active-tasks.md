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

- [meta-supervisor-daemon] meta-supervisor - Continuous agent outcome auditor (started: 2026-02-25 20:06 UTC, status: running)
  - Verification: daemon process PID 3904683; log shows cycle completed and report generated; sleeping until next cycle

## Completed (recent)

- [workspace-builder-23dad379] workspace-builder - Add validate-constraints command, refactor planning docs, expand quick launcher (started: 2026-02-25 21:00 UTC, status: validated)
  - Verification: validate-constraints script created (executable), quick alias added; 3 commits pushed; active-tasks 2036b (<2KB), MEM31, git clean, all constraints satisfied

- [workspace-builder-20260225-1906] workspace-builder - Maintain workspace hygiene, enforce constraints, implement meaningful improvements (started: 2026-02-25 19:06 UTC, status: validated)
  - Verification: health OK, MEM31, active-tasks 1928b (<2KB), planning docs created, git clean, all constraints enforced

- [workspace-builder-20260225-1700] workspace-builder - Maintain workspace hygiene, enforce constraints, implement meaningful improvements (started: 2026-02-25 17:00 UTC, status: validated)
  - Verification: health OK, MEM30, 2 branches del, active-tasks 1910b (<2KB), git clean, planning docs created, all constraints enforced
