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

## Completed (recent cycles only)

- [cron] content-agent - evening digest (14:03 UTC)
- [isolated] dev-agent - openclaw-status (14:00 UTC)
- [cron] content-agent - night note (13:50 UTC)
- [isolated] dev-agent - gateway-logs & version (13:40 UTC)
- [cron] research-agent - brief 14 (13:31 UTC)
- [cron] content-agent - day wrap (13:30 UTC)
- [cron] content-agent - daily digest (13:22 UTC)

# End of file — keep under 2KB
