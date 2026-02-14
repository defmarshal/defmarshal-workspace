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

- [validated] gap-research — Search web for "gapping method in banking industry" (started: 2026-02-13 15:24, status: validated)
  - Verification: Comprehensive research report completed, saved as gapping-method-banking-research-report.md
