# Active Tasks Registry

This file tracks all currently running agents, their session keys, goals, and status. Used for "close the loop" verification and avoiding duplicate work.

**Rules:**
- Max size: 2KB (keep concise)
- Read at start of EVERY session
- Update immediately when spawning or killing agents
- Include session key, goal, started timestamp, and verification status

## Agent Lifecycle

1. **Spawning**: Add entry with `status: running`
2. **Validation**: After completion, update `status: validated` and add verification notes
3. **Cleanup**: Remove entry after verification (or archive to daily log)

## Format

```markdown
- [sessionKey] <agent-name> - <goal> (started: <time>, status: <running/validated/failed>)
  - Verification: <curl/test/check command outputs>
```

## Current Active Tasks

- [main] dev-agent - Continuous improvements; meta-agent crash fix (started: 2026-02-18 12:00 UTC, status: running)
  - Verification: meta-agent.sh patched; bash -n passes; basic test runs


## Completed (Feb 17)

- Multiple builds completed and archived to memory/2026-02-17.md.

## Completed (Feb 18)

- [build] workspace-builder - Fix quick launcher syntax; validate meta-agent refactor; enforce policies (started: 2026-02-18 07:00 UTC, status: validated)
  - Verification: quick health OK; meta-agent.sh syntax OK; memory search functional; active-tasks.md pruned to 970 bytes; git push succeeded.

# End of file — keep under 2KB
