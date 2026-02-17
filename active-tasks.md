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

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] content-agent - Pre‑lunch status 3 (started: 2026-02-17 09:23 UTC, status: validated)
  - Verification: 2026-02-17-pre-lunch-3.md; commit df35aee; archive 47 files.

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] content-agent - Late morning status 5 (started: 2026-02-17 09:30 UTC, status: validated)
  - Verification: 2026-02-17-late-morning-5.md; commit 8aa569b; archive 48 files.

# End of file — keep under 2KB
