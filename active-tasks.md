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

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] content-agent - Daily digest (started: 2026-02-17 12:30 UTC, status: validated)
  - Verification: 2026-02-17-daily-digest.md; commit 8f42250; archive 62 files.

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] research-agent - Research brief 12 (started: 2026-02-17 12:33 UTC, status: validated)
  - Verification: 2026-02-17-brief-12.md; commit 585fbd2; archive 34 files.

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] research-agent - Research brief 11 (started: 2026-02-17 12:09 UTC, status: validated)
  - Verification: 2026-02-17-brief-11.md; commit 9eebc73; archive 33 files.

- [isolated] dev-agent - Increase workspace-builder timeout to 1800s after continued timeouts (started: 2026-02-17 12:20 UTC, status: validated)
  - Verification: Payload timeout set to 1800s; next run should complete without error.

# End of file — keep under 2KB
