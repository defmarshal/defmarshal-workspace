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

- [daemon] dev-agent — Running as persistent daemon (`dev-agent-loop.sh`, every 20 min, respects quiet hours). PID: 215960. Logs: dev-agent.log.
  - Verification: Monitor log and commits; daemon auto-restarts.

- [agent:main:subagent:9a226a1c-d763-47d6-aa8f-9cef6fb0f355] research-agent — Continuous research on anime, banking, tech, AI (started: 2026-02-14 08:57, status: running)
  - Note: Use startup script to respawn if missing after Gateway restart.
  - Verification: pending (review report quality and coverage)

- [agent:main:subagent:b8df7b21-6e63-4257-a432-dd44e608ee1a] content-agent — Continuous content creation (anime, tech, summaries) (started: 2026-02-14 08:57, status: running)
  - Note: Use startup script to respawn if missing after Gateway restart.
  - Verification: pending (monitor output cycles)

- [agent:main:cron:23dad379-21ad-4f7a-8c68-528f98203a33] workspace-builder — Strategic builder (every 2h, respects quiet hours) (started: 2026-02-13 15:00, status: running)
  - Verification: Last run produced quick launcher + anime-companion; next run in ~2h

- [validated] gap-research — Search web for "gapping method in banking industry" (started: 2026-02-13 15:24, status: validated)
  - Verification: Comprehensive research report completed, saved as gapping-method-banking-research-report.md
