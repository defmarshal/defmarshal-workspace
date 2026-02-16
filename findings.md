# Findings & Decisions

## Requirements Analysis
- Maintain robust, clean workspace aligned with lessons learned (anti-patterns)
- Convert persistent daemon agents to cron-based scheduling (per lessons.md: "Persistent agent anti-pattern")
- Ensure all cron jobs documented and running
- Keep system health high; address pending updates if reasonable
- Update documentation to reflect current state

## Current System State (2026-02-16 13:00 UTC)

### Git & Version
- Branch: master, up to date with origin/master
- Working tree: clean
- Recent commits from prior builder (workspace-builder 11:00 UTC) showing memory-reindex-cron and log-rotate-cron implementation

### Disk & System
- Disk usage: 65% (2.7G used / 45G total) — healthy
- System updates: 2 upgradable packages (not critical but could be automated)
- Large logs: aria2.log 675 MB (log-rotate-cron will handle weekly; acceptable)

### Memory System
- Main: 7 files indexed, 43 chunks, dirty: false (clean)
- Torrent-bot instance: 0 files, dirty: true (expected, minimal activity)
- Voyage AI provider active, FTS enabled, vector disabled
- No batch processing (rate-limit safe)

### Agents & Daemons
- Persistent daemons running: dev-agent, content-agent, research-agent (via start-background-agents.sh)
- Torrent-bot also running as daemon (slash-command agent; acceptable)
- All respect quiet hours (23:00–08:00 Asia/Bangkok) per logs and code

### Cron Infrastructure
- OpenClaw cron jobs (8 total):
  1. workspace-builder (every 2h Bangkok)
  2. email-cleaner-cron (09:00 Bangkok)
  3. auto-torrent-cron (02:00 Bangkok)
  4. random-torrent-downloader (every 2h UTC)
  5. traffic-report-cron (22:00 UTC)
  6. content-index-update-cron (05:30 Bangkok)
  7. memory-reindex-cron (Sunday 04:00 Bangkok)
  8. log-rotate-cron (Sunday 05:00 Bangkok)
- Documentation in CRON_JOBS.md is accurate and complete

### Quick Launcher
- Commands for memory-index, memory-stats, log-rotate, health, verify all present and functional
- Log-rotate script exists (1198 bytes) and is executable

## Identified Improvement Areas

### 1. Persistent Daemons → Cron (High Impact)
**Problem**: dev-agent, content-agent, research-agent run as infinite-loop daemons. Lessons.md explicitly warns: "Do NOT use long-running subagents for periodic tasks. Use cron jobs instead."
**Impact**: 
- Orphaned processes if gateway restarts (subagents die, no auto-respawn)
- Higher resource usage (constant process)
- Violates established best practice
**Solution**: Convert each agent to a cron job that executes their main loop once per scheduled interval. The agent code already uses `sleep` between iterations; we can wrap a single iteration in a cron job.

### 2. Pending System Updates (Medium)
Two packages upgradable. Could:
- Manual: `sudo apt upgrade` (one-time)
- Automated: create weekly update check cron (or enable unattended-upgrades)
**Decision**: Low priority; can be manual for now. Document in notes.

### 3. Documentation Refresh (Low)
`active-tasks.md` currently lists daemons as running; need update after conversion.
`projects.md` lists "24/7 Autonomous Agents" as active with daemon approach; should reflect cron migration.
`MEMORY.md` already up-to-date (2026-02-16 entry covers log rotation and reindex).

## Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Convert agents to cron with same intervals (20/10/15 min) | Maintains frequency; respects quiet hours within agent code; eliminates infinite loops |
| Keep agents' existing log files (dev-agent.log, content-agent.log, research-agent.log) | Consistency; easy to tail; cron payload will append |
| Do NOT change agent code itself; only scheduling | Agents already designed for periodic execution; their loop script does: while true; do work; sleep; done. We'll create a wrapper that runs once, or call the loop with a count=1? Better: create a script that runs the agent's core function once. Need to inspect agent loop contents. |
| Disable daemons after verifying cron works | Avoid duplication and resource waste |
| Update active-tasks.md and projects.md; no MEMORY.md change needed | active-tasks.md reflects current state; projects.md records methodology |
| Defer update automation | Not urgent; could be separate future builder task |

## Potential Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Cron agent runs overlap or take longer than interval → multiple instances concurrent | Use lockfile (flock) in cron wrapper to prevent overlap; agents should be idempotent |
| Agents assume long-running state (e.g., caches in memory) | Agents appear simple (content-agent creates content files; research-agent fetches research; dev-agent writes utilities). Likely stateless per-run. Verify by inspecting loop scripts. |
| Log format changes (daemon vs one-shot) | Ensure cron appends to same log files (`>>`) as before; timestamps should still appear |
| Quiet hours not respected in cron | Agent code already checks quiet hours; verify in code. Cron job payload can also include pre-check, but redundant. |
| Conversion breaks something → agents stop producing | Test each cron job manually via `openclaw cron run` before disabling daemons. Keep daemon scripts as fallback. |

## Dependencies
- Need to examine agent loop scripts to see how to invoke them correctly for one-shot execution.
- OpenClaw cron must be functional (it is, per existing jobs).
- Ability to kill daemon processes (we have permissions).

## Open Questions
- Are the agents truly idempotent per-run? They fetch/create new content each run. That's fine; multiple runs generate multiple items. That's expected. They don't rely on stateful memory between iterations, so one-shot is safe.
- Should we keep the daemon scripts for emergency fallback? Yes, keep them but comment out or rename to *.sh.disabled.
- Do we need to adjust `start-background-agents.sh`? Yes, comment out daemon launches or disable script entirely.

## Proposed Cron Payloads

**dev-agent-cron** (every 20 min: `0,20,40 * * * *` Asia/Bangkok)
```
Execute: bash -c 'cd /home/ubuntu/.openclaw/workspace && ./dev-agent-loop.sh --once >> dev-agent.log 2>&1'
```
(Need to verify if loop script accepts `--once` or we need to call the agent's main directly)

Better approach: Create wrapper scripts that invoke the agent's core functionality without the infinite loop. We'll inspect the loop scripts to see what the agent's actual command is (likely they call some agent API or script). Might be simpler: The loop script is already a bash script that runs `openclaw agents spawn` or similar with an infinite loop. We can extract that command and run it once.

Let's read the loop scripts to understand their structure.
