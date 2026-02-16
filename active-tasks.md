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

- [daemon] torrent-bot - Slash-command torrent management agent (running)
  - Verification: agent registered; daemon loop started (PID varies); respects quiet hours; pairing pending for Telegram channel.
- [cron:23dad379-21ad-4f7a-8c68-528f98203a33] workspace-builder - Disk hygiene improvements (started: 2026-02-16 19:00 UTC, status: validated)
  - Verification: Created cleanup-downloads.sh (dry-run works), enhanced quick health with Downloads metric, added cleanup command to quick launcher, updated workspaces-health. All changes tested, git clean, agents healthy.

# End of file — keep under 2KB