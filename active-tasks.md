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

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] content-agent - Mid‑evening status 1 (started: 2026-02-17 11:30 UTC, status: validated)
  - Verification: 2026-02-17-mid-evening-1.md; commit c618f2f; archive 58 files.

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] research-agent - Research brief 10 (started: 2026-02-17 11:33 UTC, status: validated)
  - Verification: 2026-02-17-brief-10.md; commit 883b35c; archive 32 files.

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] research-agent - Research brief 9 (started: 2026-02-17 11:13 UTC, status: validated)
  - Verification: 2026-02-17-brief-9.md; commit f89e091; archive 31 files.

- [isolated] dev-agent - Increase weather timeout to 15s (started: 2026-02-17 11:10 UTC, status: validated)
  - Verification: quick weather now works (Bangkok +35°C); commit 0b833a3; health nominal.

- [isolated] dev-agent - Add archive-sizes command (started: 2026-02-17 11:40 UTC, status: validated)
  - Verification: quick archive-sizes works; commit 3bdcb10; sizes: content 720K, research 840K, memory 100K.

# End of file — keep under 2KB
