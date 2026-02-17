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

- [cron] content-agent — Late evening 2 (started: 13:06 UTC, validated)
  - 2026-02-17-late-evening-2.md; commit f61e245; archive 64 files.

- [cron] research-agent — Brief 13 (started: 13:08 UTC, validated)
  - 2026-02-17-brief-13.md; commit facef31; archive 35 files.

- [isolated] dev-agent — Add cron-failures utility (12:40 UTC, validated)
  - commit 0981da8; quick cron-failures shows erroring jobs.

- [isolated] dev-agent — Fix supervisor memory check (12:55 UTC, validated)
  - commit 9d3f6aa; fixed inverted condition.

- [isolated] dev-agent — Add git-recent (13:01 UTC, validated)
  - commit fe77d7a; quick git-recent shows commit list.

- [isolated] dev-agent — Add gateway-info (13:19 UTC, validated)
  - commit 34379fe; quick gateway-info shows status and troubleshooting.

# End of file — keep under 2KB

# End of file — keep under 2KB
