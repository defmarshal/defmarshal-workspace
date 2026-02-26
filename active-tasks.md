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

- [workspace-builder-20260226-0305] workspace-builder - Enhance validate-constraints, add show-validation-checks, update planning docs (started: 2026-02-26 03:05 UTC, status: validated)
  - Verification: active-tasks 1903b (<2KB), MEM30, git clean, all constraints satisfied; reindex age check added; quick alias added; troubleshooting documented

- [workspace-builder-20260226-0507] workspace-builder - Cleanup stale idea branches, fix validate-constraints APT parsing, remove obsolete proposed cron job from CRON_JOBS.md (started: 2026-02-26 05:07 UTC, status: validated)
  - Verification: Deleted 6 idea branches; APT parsing fixed; CRON_JOBS.md updated; active-tasks 1902b (<2KB), MEM30, git clean, health green, constraints satisfied

- [workspace-builder-20260226-0708] workspace-builder - Push pending commits, enforce constraints, document session (started: 2026-02-26 07:08 UTC, status: validated)
  - Verification: active-tasks 1643b (<2KB), MEM30, git clean after push, all constraints validated; 2 commits pushed (content daily digest, dev memory-reindex-if-stale); planning docs created (task_plan, findings, progress)
