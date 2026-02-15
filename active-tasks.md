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
- [sessionKey] <agent-name> — <goal> (started: <time>, status: <running/validated/failed>)
  - Verification: <curl/test/check command outputs>
```

## Current Active Tasks

- [daemon] dev-agent — Running as persistent daemon (`dev-agent-loop.sh`, every 20 min, respects quiet hours). PID: 215961. Logs: dev-agent.log.
- [daemon] content-agent — Running as persistent daemon (`content-agent-loop.sh`, every 10 min, respects quiet hours). PID: 225692. Logs: content-agent.log.
- [daemon] research-agent — Running as persistent daemon (`research-agent-loop.sh`, every 15 min, respects quiet hours). PID: 225712. Logs: research-agent.log.

- [agent:main:cron:23dad379-21ad-4f7a-8c68-528f98203a33] workspace-builder — Added content-latest command, updated content/INDEX.md, added new content files, reindexed memory (started: ~2026-02-15 11:00 UTC, status: validated)
  - Verification: `quick health` OK; `quick content-latest` works; `quick memory-status` shows healthy; all changed files verified; commit pushed successfully.
