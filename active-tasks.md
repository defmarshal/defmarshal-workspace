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

- [daemon] torrent-bot (running)
- [build] workspace-builder - Archive/prune active-tasks; enforce 2KB limit; validate system (started: 2026-02-18 05:00 UTC, status: validated)
  - Verification: active-tasks.md size 1112 bytes (≤2KB); memory/2026-02-18.md updated with archival; system health OK; git push succeeded.

## Completed (Feb 17)

- Multiple builds completed and archived to memory/2026-02-17.md.

# End of file — keep under 2KB
