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

- [daemon] torrent-manager (running)
- [build] workspace-builder - Fix agent-manager reindex bug; add memory-dirty; update docs (started: 2026-02-18 01:00 UTC, status: validated)
  - Verification: agent-manager --once correct (no spurious reindex); memory-dirty works; docs updated; health OK; git push succeeded.

## Completed (Feb 17)

- All cycles concluded; archive sealed at 77 content + 39 research files.
- Gateway token rotation completed; UI accessible via Tailscale.
- Supervisor-cron schedule changed to every 2 hours (`0 */2 * * *).
- Content follow-up added confirming no pending tasks.
- Workspace-builder (19:00 UTC) validated; archived to memory/2026-02-17.md.
- Workspace-builder (23:00 UTC) validated; fixed meta-agent memory reindex logic; documented Voyage limits; archived.

# End of file — keep under 2KB
