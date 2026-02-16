# Findings & Decisions

## Requirements
- Maintain memory system reliability despite Voyage rate limits
- Keep documentation (MEMORY.md) current with recent changes
- Prevent disk space issues from uncontrolled log growth (aria2.log)
- Enhance monitoring of memory indexing status
- Ensure overall system health remains high

## Current System State (2026-02-16 07:00 UTC)

### Git & Version
- Branch: master, up to date with origin/master
- Working tree: clean (no uncommitted changes)
- Recent commits from content-agent, dev-agent, research-agent (normal operations)

### Disk & System
- Disk usage: ~65% (2.7G used of ~45G total) — healthy
- System updates: 0 upgradable packages
- Large files: `aria2.log` 675 MB (needs rotation)

### Memory System (openclaw-memory)
- Main instance:
  - Indexed: 6 of 6 source files, 41 chunks
  - Dirty: yes (some files pending re-embedding due to Voyage rate limits)
  - Features: FTS ready, embedding cache enabled (152 entries), batch disabled (previous failures)
- Torrent-bot instance:
  - Indexed: 0 of 6 files, 0 chunks (expected, no logs yet)
  - Dirty: yes
- Note: Voyage AI rate limit (3 RPM) causes indexing delays; search remains functional; this is an acceptable known limitation per MEMORY.md.

### Agents & Daemons
- Running daemons: dev-agent, content-agent, research-agent, torrent-bot
- All respect quiet hours (23:00–08:00 Asia/Bangkok)
- Recent logs show no critical errors

### Content Index
- `content/INDEX.md` includes 2026-02-16 content files; appears up-to-date
- The `quick content-index-update` command works and cron job (05:30 Bangkok) is active via OpenClaw cron

### Quick Launcher
- Commands include: memory-status, memory-index, memory-stats, health, etc.
- All appear functional

### CRON_JOBS.md
- Already documents content-index-update-cron and other jobs
- Up-to-date

## Identified Improvement Areas

1. **Memory Reindex Strategy**
   - Dirty flag persists; to eventually clear, schedule periodic reindex (weekly)
   - Use `claw memory index` or `quick memory-index`
   - Log output to `memory/memory-reindex.log`
   - Add to OpenClaw cron to avoid interfering with rate-limited manual runs

2. **Log Rotation**
   - `aria2.log` is 675 MB and growing; risk of filling disk over time
   - Implement simple rotation: compress and truncate when > 100 MB, keep last 4 archives
   - Provide `quick log-rotation` command

3. **Documentation Refresh**
   - MEMORY.md last updated 2026-02-15
   - Needs entries for:
     - Content Index Update cron (05:30 Bangkok)
     - Memory stats and index commands (`memory-stats`, `memory-index`)
     - Acknowledgment of Voyage dirty flag and planned mitigation (weekly reindex)
     - Mention of log rotation plan

4. **Monitoring**
   - `quick health` already shows memory file counts and dirty status; sufficient for now
   - No immediate need for alerts; dirty flag visible enough
   - May enhance later to warn if dirty > 7 days

## Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Add weekly (Sunday 04:00 Bangkok) memory reindex via OpenClaw cron | Spreads load, gives Voyage time to recover, should eventually clear dirty |
| Implement custom logrotate script (bash) for aria2.log | No external dependencies; easy to adjust thresholds |
| Update MEMORY.md (not create separate changelog) | Centralized reference for long-term memory |
| Use absolute path in cron for `quick` and scripts | Consistency with existing cron entries (content-index-update, email-cleaner) |
| Keep Voyage as provider for now (no migration) | Free tier sufficient; switching requires new API keys and config |
| Delay alerts for dirty flag | Current manual checks via health/memory-status adequate; could add later if persistent |

## Potential Risks & Mitigations

- Rate limit on memory reindex may cause incomplete indexing in one run → Accept partial; next weekly run will continue.
- Log rotation script could accidentally delete needed logs → Keep 4 archives; ensure we only compress/truncate, not delete all but one.
- Cron misconfiguration could cause overlapping jobs → Use distinct times: reindex 04:00 Bangkok, content-index 05:30.

## Dependencies
- None external; all scripts use existing tools (bash, gzip, mv, tail)
- OpenClaw `claw memory` CLI must remain available (already is)

## Open Questions
- Could we switch to `neural-memory` as primary? Not yet; FTS is working; need evaluation.
- Should we also rotate other logs (agent logs)? They are moderate; focus on largest first.