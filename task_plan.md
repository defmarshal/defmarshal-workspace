# Workspace Builder Task Plan
**Started**: 2026-02-16 21:00 UTC
**Builder Session**: cron-triggered (23dad379)
**Goal**: Improve disk hygiene and implement backup rotation to address 82% disk usage

## Phase 1: Quick Assessment (Status: Complete)
- [x] Verify previous builder's outputs (cleanup-downloads.sh, health updates)
- [x] Test cleanup-downloads in dry-run (found no old downloads; all recent)
- [x] Identify major space consumers: backup tarballs in /home/ubuntu (2.2G each x2 = 4.4G)
- [x] Confirm disk usage and health status
- [x] Check existing cron jobs (cleanup-downloads-cron already exists)

## Phase 2: Backup Cleanup Implementation
- [ ] Create `scripts/cleanup-backups.sh`:
  - Dry-run by default
  - Keep most recent N backups (default 1) in /home/ubuntu
  - Match pattern `openclaw-backup-*.tar.gz`
  - Verbose output
  - Safety: don't delete if fewer than N backups
- [ ] Make script executable
- [ ] Test in dry-run mode to verify it would keep the latest and delete older ones
- [ ] If dry-run safe, execute with `--execute` to free space
- [ ] Add `quick cleanup-backups` command to launcher

## Phase 3: Documentation Updates
- [ ] Update `CRON_JOBS.md`:
  - Document `cleanup-downloads` command and existing weekly cron
  - Document proposed `cleanup-backups` (even if not scheduled yet)
  - Note that cleanup-downloads is already scheduled weekly
- [ ] Add backup cleanup considerations (retention policy)
- [ ] Update `findings.md` with observations about backup strategy

## Phase 4: Validation
- [ ] Run `quick health` and verify disk usage decreased (expect ~79% after deleting one 2.2G backup)
- [ ] Verify no critical data lost: ensure at least one backup remains
- [ ] Test `quick cleanup-backups --days 0` (dry-run) shows correct targets
- [ ] Check git status clean
- [ ] Ensure all agents still running
- [ ] Confirm memory system operational

## Phase 5: Commit & Close Loop
- [ ] Stage all changes (scripts, docs, quick launcher)
- [ ] Commit with prefix: `build: disk hygiene; add backup cleanup, docs; free 2.2G`
- [ ] Push to GitHub
- [ ] Update active-tasks.md: mark validated, add verification results
- [ ] Log summary to memory

## Risk Mitigation
- All cleanup operations default to dry-run; require explicit --execute
- Backup cleanup keeps at least 1 most recent backup by default (configurable)
- No impact on active downloads or agent logs
- Changes are small and focused