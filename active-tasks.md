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

- [agent:main:subagent:9f09cc7d-8ab7-4957-a76d-97c32c8aa743] content-agent — Continuous content creation (anime, tech, summaries) (started: 2026-02-13 17:35, status: running)
  - Verification: pending (monitor output cycles)

- [agent:main:subagent:95145785-118c-4dfd-a821-eef8c3ed803d] research-agent — Continuous research on anime, banking, tech, AI (started: 2026-02-13 17:35, status: running)
  - Verification: pending (review report quality and coverage)

- [agent:main:subagent:609e93ce-4c21-4d60-acf1-3dbbf0b0d5cc] dev-agent — Continuous development (tools, automations, infrastructure) (started: 2026-02-13 17:35, status: running)
  - Verification: pending (monitor commits and improvements)

- [agent:main:cron:23dad379-21ad-4f7a-8c68-528f98203a33] workspace-builder — Strategic builder (every 2h, respects quiet hours) (started: 2026-02-13 15:00, status: running)
  - Verification: Last run produced quick launcher + anime-companion; next run in ~2h

- [agent:main:subagent:9751d90f-9268-4200-8dd6-cdaa78ec4d76] gap-research — Search web for "gapping method in banking industry" (started: 2026-02-13 15:24, status: validated)
  - Verification: Comprehensive research report completed, saved as gapping-method-banking-research-report.md
