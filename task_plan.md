# Task Plan: Strategic Workspace Improvements
**Builder Run**: 2026-02-16 13:00 UTC (20:00 Bangkok)
**Session Key**: agent:main:cron:workspace-builder-20260216-1300

## Phase 1: Discovery & Assessment (COMPLETE)
- [x] Read active-tasks.md → confirmed 4 daemons running (dev, content, research, torrent-bot)
- [x] Check git status → clean, up to date
- [x] Run `quick health` → Disk 65%, 2 updates, memory clean, reindex: never
- [x] Memory system status → main: 7f/43c (clean) voyage FTS+; torrent-bot: dirty
- [x] Verify cron jobs → memory-reindex-cron and log-rotate-cron are registered and enabled
- [x] Check scripts → log-rotate and memory-stats exist and executable
- [x] Review MEMORY.md → last updated 2026-02-16; includes content-index cron, memory commands
- [x] Review lessons.md → anti-pattern: persistent agents should be cron jobs
- [x] Review CRON_JOBS.md → well documented

## Phase 2: Gap Analysis & Prioritization
**Identified Gaps**:

1. **High Impact**: Persistent daemons (dev-agent, content-agent, research-agent) use infinite loops; should be converted to cron jobs per lessons.md. This prevents orphaned processes, improves reliability after restarts, and reduces resource usage.
2. **Medium**: Updates pending (2 packages) — could be automated via unattended-upgrades or a weekly cron job.
3. **Low**: torrent-bot is a slash-command agent; not periodic so daemon is acceptable (or could be moved to systemd service). Keep as-is for now.
4. **Documentation**: Need to update active-tasks.md and projects.md after conversion. MEMORY.md may need note about daemon→cron migration.

**Priority Order**:
1. Convert dev-agent to cron
2. Convert content-agent to cron
3. Convert research-agent to cron
4. Update documentation (active-tasks.md, projects.md, MEMORY.md if needed)
5. Optionally: create weekly update check cron (or leave manual)

## Phase 3: Implementation Plan
**Step 1: Analyze agent loop scripts** (`dev-agent-loop.sh`, `content-agent-loop.sh`, `research-agent-loop.sh`)
- Determine their core periodic tasks (intervals: dev 20min, content 10min, research 15min)
- Check they respect quiet hours already (should)
- Identify output logging (existing log files)

**Step 2: Create isolated cron payloads**
- For each agent, craft an agentTurn message that executes the agent's main work (without infinite loop)
- Keep the same schedule (every N minutes) in Asia/Bangkok timezone
- Preserve logging to their respective log files
- Ensure they respect quiet hours (agent code already does)

**Step 3: Register new cron jobs**
- Use `openclaw cron add` for each
- Names: dev-agent-cron, content-agent-cron, research-agent-cron
- Schedule: `*/20 * * * *` in Asia/Bangkok for dev? Actually every 20 min: `0,20,40 * * * *`
- content: every 10 min: `0,10,20,30,40,50 * * * *`
- research: every 15 min: `0,15,30,45 * * * *`

**Step 4: Test new cron jobs**
- Manually run each with `openclaw cron run <jobId>` or via script
- Check logs for successful execution
- Verify they don't overlap or conflict

**Step 5: Disable old daemons**
- Kill the persistent processes for dev-agent, content-agent, research-agent
- Remove or comment out entries from `start-background-agents.sh` (or keep but mark deprecated)
- Update active-tasks.md to remove daemon entries and add new cron tasks

**Step 6: Update documentation**
- `active-tasks.md`: remove daemon entries; add cron job task entries (with verification states)
- `projects.md`: update "24/7 Autonomous Agents" to reflect cron-based scheduling; note daemon→cron migration
- `CRON_JOBS.md`: add entries for dev-agent-cron, content-agent-cron, research-agent-cron
- `MEMORY.md`: optional: add note about migration to cron (like other entries)

**Step 7: Validation (CLOSE THE LOOP)**
- Run `quick health` → baseline
- Run `quick verify` → comprehensive checks
- Test `quick agent-logs` to see recent cron runs
- Confirm git status clean
- Check no temp files left
- Ensure all files committed

**Step 8: Commit & Push**
- Commit message prefix: `build:`
- Include all modified files
- Push to origin/master

## Dependencies & Risks
- Agent code must respect quiet hours; verify in loop scripts.
- Cron jobs run in isolated sessions; ensure they can write logs (absolute paths)
- Existing daemon processes may interfere if both run; disable daemons first.
- Risk: Cron may not perfectly replace daemon if agents assume long-running context. Review agent code to ensure they are idempotent per-run.

## Rollback Plan
- Keep the daemon scripts; if cron fails, can restart daemons via `start-background-agents.sh`
- Cron jobs can be disabled via `openclaw cron disable <id>` or removed.

## Success Criteria
- All three agents run via cron on schedule (we can see logs in `memory/` or their dedicated logs)
- No persistent daemon processes for dev-agent, content-agent, research-agent (except torrent-bot)
- active-tasks.md reflects the new state (cron jobs running, daemons stopped)
- Documentation updated (CRON_JOBS.md, projects.md)
- Verification passes; changes committed and pushed
