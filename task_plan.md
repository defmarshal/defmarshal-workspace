# Task Plan: Content Index Automation & System Health Verification

## Goal
Implement operational improvements to maintain workspace reliability, focusing on:
- Automating content archive index updates (content/INDEX.md)
- Verifying system health after recent changes
- Ensuring documentation reflects current cron setup
- Validating all agents and memory system status

## Current Phase
Phase 1: Requirements & Discovery

## Phases

### Phase 1: Requirements & Discovery
- [x] Archive previous planning files (build-archive/)
- [x] Check active tasks and running agents
- [x] Review MEMORY.md and recent daily logs (2026-02-15, 2026-02-16)
- [x] Verify git status and recent commits (clean, up-to-date)
- [x] Inspect crontab for duplicates/errors
- [x] Check memory system health (indexed 6/6, dirty flag known limitation)
- [x] Test `quick content-index-update` command (works, tracks 41 files)
- [x] Document findings in findings.md
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Define specific improvement tasks based on findings
- [x] Prioritize by impact and urgency
- [x] Create detailed implementation steps
- [x] Document decisions with rationale
- **Status:** complete

### Phase 3: Implementation
- [ ] Add cron job to run `quick content-index-update` daily (e.g., 05:30 Bangkok)
- [ ] Update CRON_JOBS.md to document new cron entry
- [ ] Run `quick content-index-update` manually to verify current index includes latest content
- [ ] Check email-cleaner API key warning (MATON_API_KEY) - assess if fix needed
- [ ] Verify memory system: run `quick memory-stats`, ensure search works
- [ ] Run `quick health` to confirm no issues
- [ ] Validate agent daemons are running (ps, pgrep)
- **Status:** pending

### Phase 4: Testing & Verification
- [ ] Test cron command by simulating it (run the exact command that will be in cron)
- [ ] Verify content-index-update completes without errors
- [ ] Check that content/INDEX.md reflects latest files (e.g., 2026-02-16-pre-dawn-wrap.md)
- [ ] Run `quick health` again after changes
- [ ] Confirm memory search still functional: `quick search "test"`
- [ ] Ensure all changed files are properly staged
- [ ] Check for any temp files to clean
- **Status:** pending

### Phase 5: Delivery
- [ ] Review all output files (task_plan, findings, progress updated)
- [ ] Ensure deliverables complete
- [ ] Commit changes with prefix `build:`
- [ ] Push to GitHub (`git push origin master`)
- [ ] Update active-tasks.md: mark this session as validated with verification notes
- [ ] Archive planning files with timestamp (already done at start)
- **Status:** pending

## Key Questions
1. Should content-index-update run daily or hourly? Daily at early morning is sufficient; content generated throughout day, index refreshed next morning.
2. Does email-cleaner need MATON_API_KEY set, or is fallback acceptable? The script falls back to config warning but still works. Not critical, but could be cleaned up.
3. Is there any risk of duplicate cron entries when adding new job? Must use `crontab -l | grep -v '^$' | sort -u | crontab -` or manual check. But we'll add distinct command; duplicates unlikely. We'll verify with `crontab -l` after adding.
4. Should we address memory dirty flag? It's a known Voyage rate limit issue; acceptable for now. Document in findings.
5. Are all background agents healthy? Yes, 3 daemons + torrent-bot running. Confirm with `pgrep`.
6. Could content-index-update be integrated into content-agent directly? Possibly, but cron is simpler and decoupled. Keep as is.

## Decisions Made (to fill during process)
| Decision | Rationale |
|----------|-----------|
| Add cron at 05:30 Bangkok | After pre-dawn wrap generated (~05:05), index fresh for new day |
| Keep MATON_API_KEY warning for now | Non-blocking, can address in future if needed |
| Use `quick content-index-update` in cron | Leverages existing script, easy to test |
| Do not reindex memory now | Rate limits; dirty flag acceptable, search works |

## Errors Encountered
(Will log during execution)

## Notes
- Respect quiet hours (23:00–08:00 UTC+7). Currently outside quiet window.
- Use absolute path `/home/ubuntu/.openclaw/workspace/quick` in cron to avoid PATH issues.
- All changes should be small but meaningful.
- After each phase, update this file to reflect progress.
