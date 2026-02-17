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

- [cron] content-agent - late wrap (14:10 UTC)
- [cron] research-agent - brief 15 (14:05 UTC)
- [cron] content-agent - evening digest (14:03 UTC)
- [isolated] dev-agent - openclaw-status (14:00 UTC)

# End of file — keep under 2KB
