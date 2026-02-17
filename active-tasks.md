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

## Completed (for this session)

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] content-agent - Late morning 7 (started: 2026-02-17 12:23 UTC, status: validated)
  - Verification: 2026-02-17-late-morning-7.md; commit 55c0e76; archive 61 files.

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] research-agent - Research brief 11 (started: 2026-02-17 12:09 UTC, status: validated)
  - Verification: 2026-02-17-brief-11.md; commit 9eebc73; archive 33 files.

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] research-agent - Research brief 10 (started: 2026-02-17 11:33 UTC, status: validated)
  - Verification: 2026-02-17-brief-10.md; commit 883b35c; archive 32 files.

- [isolated] dev-agent - Add archive-sizes command (started: 2026-02-17 11:40 UTC, status: validated)
  - Verification: quick archive-sizes works; commit 3bdcb10; sizes: content 720K, research 840K, memory 100K.

- [isolated] dev-agent - Increase workspace-builder timeout to 1800s after continued timeouts (started: 2026-02-17 12:20 UTC, status: validated)
  - Verification: Payload timeout set to 1800s; next run should complete without error.

# End of file — keep under 2KB
