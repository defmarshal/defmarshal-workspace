# Task Plan: Memory Maintenance, Docs Update, and Log Rotation

## Goal
Implement targeted improvements to enhance workspace reliability and maintainability:
- Address memory system "dirty" flag with scheduled reindex and monitoring
- Update MEMORY.md with recent developments (post-Feb 15 changes)
- Add log rotation for aria2.log to prevent uncontrolled growth
- Verify overall system health

## Current Phase
Phase 1: Requirements & Discovery

## Phases

### Phase 1: Requirements & Discovery
- [x] Archive previous planning files
- [x] Check active tasks and running agents (4 daemons: dev, content, research, torrent-bot)
- [x] Review MEMORY.md (last updated 2026-02-15; needs update with latest changes)
- [x] Verify git status (clean, up to date with origin/master)
- [x] Inspect memory system status (main: 6/6 files, 41 chunks, dirty: yes; torrent-bot: 0/6, dirty: yes)
- [x] Identify improvement candidates:
  - Dirty flag persists due to Voyage rate limits; need reindex strategy
  - aria2.log size 675MB, no rotation -> risk of disk fill
  - MEMORY.md outdated (missing content-index cron, memory stats command, etc.)
- [x] Check content/INDEX.md freshness (includes 2026-02-16 files; up-to-date)
- [x] Verify quick commands (memory-status, memory-index, memory-stats present and working)
- [x] Check for any error patterns in agent logs (brief tail: no critical errors)
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Define specific tasks:
  1. Add OpenClaw cron for memory reindexing (maybe weekly, low-traffic time)
  2. Create monitoring note: if `quick memory-status` shows dirty after 24h, alert via log or message
  3. Update MEMORY.md: add content-index cron, memory commands, recent learnings
  4. Implement log rotation for aria2.log (rotate weekly, keep 4)
  5. Add `quick log-rotate` command to manually trigger rotation
- [x] Prioritize: docs update (high), log rotation (medium), memory reindex schedule (medium), monitoring (low)
- [x] Create detailed implementation steps
- **Status:** complete

### Phase 3: Implementation
- [ ] Update MEMORY.md with:
  - Content Index Update cron (05:30 Bangkok)
  - memory-stats and memory-index quick commands
  - Note about Voyage dirty flag as known limitation and planned weekly reindex
  - Mention log rotation plan
- [ ] Create log rotation script:
  - Use `logrotate` or custom bash: compress aria2.log if >100MB, keep 4 rotations
  - Command: `./quick log-rotate` to run manually
- [ ] Add OpenClaw cron for memory reindex:
  - Weekly (e.g., Sunday 04:00 Bangkok): `claw memory index` or `./quick memory-index`
  - Log to `memory/memory-reindex.log`
  - Add to CRON_JOBS.md with entry "memory-reindex-cron"
- [ ] Add simple monitoring check in health script? Actually `quick health` already includes memory file/dirty status; maybe enhance to warn if dirty > 1 day? Could be separate phase.
- [ ] Test each change:
  - Run `./quick memory-index` manually (may hit rate limits; handle failures gracefully)
  - Run log-rotate script on a test file to verify rotation
  - Verify cron entry added correctly
- **Status:** pending

### Phase 4: Testing & Verification
- [ ] Run `./quick health` and ensure no regressions
- [ ] Confirm memory reindex cron runs (simulate, check log)
- [ ] Check that after reindex, dirty flag may clear or reduce (but Voyage rate limit may cause failures; accept partial)
- [ ] Verify log rotation created compressed archive (aria2.log.1.gz) and reset aria2.log
- [ ] Update `quick help` if new command added
- [ ] Ensure all changed files are properly staged (git status)
- [ ] Remove any temp files left by scripts
- **Status:** pending

### Phase 5: Delivery
- [ ] Review all output files (task_plan, findings, progress updated)
- [ ] Commit changes with prefix `build:`
- [ ] Push to GitHub (`git push origin master`)
- [ ] Update active-tasks.md: add entry for this session with verification notes, mark validated after commit
- [ ] Archive planning files with timestamp (already done at start)
- **Status:** pending

## Key Questions
1. Should we run memory reindex weekly or daily? Weekly reduces load; daily may keep dirty flag low. Weekly (Sunday early AM) is sufficient.
2. How to handle Voyage rate limit during batch reindex? The `openclaw memory index` may process files sequentially; still could hit 3 RPM limit. Could add `--throttle`? We'll accept that it might take multiple runs to clear dirty. We'll add retry in cron? Cron will run again weekly; if fails due to rate limit, it'll be retried next week. That's acceptable.
3. Should log rotation use built-in logrotate? Simpler to write custom script; but logrotate may require config. We'll write simple script: if aria2.log > 100M, move to aria2.log.1 (compress) and truncate aria2.log. Keep 4 backups.
4. Should we add a health check warning for persistent dirty? Could enhance `quick health` later. For now, we'll rely on memory-status output showing dirty. Not urgent.
5. Are there other large logs? aria2.log is the only large one. We'll handle just that.

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Weekly memory reindex cron at Sunday 04:00 Bangkok | Low-traffic time; avoids daily rate limit pressure; acceptable to clear dirty gradually |
| Custom log rotation script (quick log-rotate) | Simpler than installing/configuring logrotate; can be run manually or via another cron if needed |
| Update MEMORY.md rather than create separate changelog | Centralized reference; keeps MEMORy.md current |
| Use absolute path in cron (`/home/ubuntu/.openclaw/workspace/quick`) | Consistency with existing cron entries (e.g., content-index-update) |
| Accept Voyage rate limit as a known limitation; document in MEMORY.md | No immediate fix; switching providers requires API keys; keep as-is |

## Errors Encountered
(Will log during execution)

## Notes
- Respect quiet hours (23:00–08:00 UTC+7). Currently outside quiet window.
- All changes should be small and low-risk.
- After each phase, update this file.