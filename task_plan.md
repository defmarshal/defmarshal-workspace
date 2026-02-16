# Workspace Builder Task Plan
**Started**: 2026-02-16 19:00 UTC
**Builder Session**: cron-triggered (23dad379)
**Goal**: Address disk space warning (82% usage) and improve system hygiene

## Phase 1: Diagnosis & Analysis (Status: In Progress)
- [ ] Enumerate large directories and files (excluding legitimate git repo)
- [ ] Identify candidates for cleanup (logs, downloads, temp files)
- [ ] Check log rotation effectiveness (aria2.log size)
- [ ] Review download management strategy (completed vs active torrents)
- [ ] Check for orphaned agent logs or temp files
- [ ] Verify systemd linger enablement (lesson learned)
- [ ] Check memory system health beyond basic health check

## Phase 2: Cleanup & Optimization
- [ ] Archive old logs (beyond existing rotation)
- [ ] Clean up temporary files (__pycache__, .pyc, build artifacts)
- [ ] Review downloads directory; flag old/stale content
- [ ] Tune log rotation parameters if needed
- [ ] Run comprehensive git garbage collection
- [ ] Update findings.md with specific metrics

## Phase 3: Enhancements & Automation
- [ ] Add disk usage thresholds to health check script
- [ ] Implement downloads retention policy (e.g., auto-clean after 30 days)
- [ ] Add disk space monitoring to daily/weekly cron checks
- [ ] Create cleanup script with safe defaults (dry-run first)
- [ ] Document cleanup procedures in CRON_JOBS.md

## Phase 4: Validation
- [ ] Run `quick health` and verify disk warning cleared (<80%)
- [ ] Test cleanup script in dry-run mode
- [ ] Verify no critical data deleted
- [ ] Check git status clean
- [ ] Ensure all agents still running
- [ ] Confirm memory system operational

## Phase 5: Commit & Close Loop
- [ ] Stage all documentation and script changes
- [ ] Commit with prefix: `build: disk hygiene improvements`
- [ ] Push to GitHub
- [ ] Update active-tasks.md: mark validated, add verification results
- [ ] Log summary to memory

---
## Risk Mitigation
- All cleanup operations will include dry-run capability
- Deletions will preserve recent anime downloads (< 30 days)
- Log rotation will maintain compressed archives, not delete history
- All changes tested in workspace before commit
- No database migrations or skill changes
