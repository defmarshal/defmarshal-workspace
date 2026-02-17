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

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] content-agent - Pre‑digest status 4 (started: 2026-02-17 10:21 UTC, status: validated)
  - Verification: 2026-02-17-pre-digest-4.md; commit ac9b3c7; archive 52 files.

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] research-agent - Research brief 7 (started: 2026-02-17 10:31 UTC, status: validated)
  - Verification: 2026-02-17-brief-7.md; commit d58a150; archive 28 files.

# End of file — keep under 2KB
