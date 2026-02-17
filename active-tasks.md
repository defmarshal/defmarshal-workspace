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

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] content-agent - Final pre‑evening 1 (started: 2026-02-17 12:07 UTC, status: validated)
  - Verification: 2026-02-17-final-pre-evening-1.md; commit c07b49f; archive 61 files.

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] research-agent - Research brief 10 (started: 2026-02-17 11:33 UTC, status: validated)
  - Verification: 2026-02-17-brief-10.md; commit 883b35c; archive 32 files.

- [cron:e345525c-f289-4eab-bf25-6d6fa065e4b0] research-agent - Research brief 9 (started: 2026-02-17 11:13 UTC, status: validated)
  - Verification: 2026-02-17-brief-9.md; commit f89e091; archive 31 files.

- [isolated] dev-agent - Add archive-sizes command (started: 2026-02-17 11:40 UTC, status: validated)
  - Verification: quick archive-sizes works; commit 3bdcb10; sizes: content 720K, research 840K, memory 100K.

- [isolated] dev-agent - Tune cron timeouts (supervisor-cron 60→300, workspace-builder 600→900) (started: 2026-02-17 12:01 UTC, status: validated)
  - Verification: Updated cron job payload timeouts via gateway; error rates should drop.

# End of file — keep under 2KB
