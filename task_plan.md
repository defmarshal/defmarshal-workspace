# Workspace Builder Task Plan
**Started**: 2026-02-16 23:00 UTC
**Builder Session**: cron-triggered (23dad379)
**Goal**: Enhance system reliability and maintenance automation

## Phase 1: Quick Assessment (In Progress)
- [x] Check previous builder's status: completed disk hygiene, files committed
- [x] Current disk: 77% (healthy), pending updates: 7
- [x] Identify gaps:
  - Systemd linger not enabled (agents die on logout/reboot)
  - Backup cleanup script exists but not scheduled via cron
  - Agent logs (dev-agent.log, content-agent.log, research-agent.log) lack rotation
  - Updates management: no safe workflow (dry-run → apply)
- [x] Verify all cron jobs operational
- [ ] Verify neural-memory integration status

## Phase 2: Reliability Improvements

### Enable systemd linger (persistent user services)
- [ ] Check current linger status: `loginctl show-user ubuntu -p Lingering`
- [ ] If not enabled, run: `sudo loginctl enable-linger ubuntu`
- [ ] Verify: `loginctl show-user ubuntu -p Lingering` should return ` yes`
- [ ] Note: This allows user services (openclaw-gateway) to survive logout/reboot

### Schedule backup cleanup (prevent recurrence)
- [ ] Create cron job for weekly backup cleanup (Sunday 07:00 Asia/Bangkok, after cleanup-downloads)
- [ ] Use existing script: `./quick cleanup-backups --execute --keep 1`
- [ ] Document in CRON_JOBS.md
- [ ] Test dry-run first to confirm safe

### Implement agent log rotation
- [ ] Extend `log-rotate` script to handle agent logs (dev-agent.log, content-agent.log, research-agent.log)
- [ ] Rotation policy: compress when >1MB, keep 4 archives
- [ ] Ensure rotation runs weekly (already scheduled Sunday 05:00 Bangkok)
- [ ] Test manually: create large log, run rotation, verify .gz created and original truncated

### Improve update management (safe workflow)
- [ ] Create `scripts/updates-check.sh`: dry-run list of upgradable packages
- [ ] Create `scripts/updates-apply.sh`: apply updates (with sudo), with optional dry-run
- [ ] Add to quick launcher as:
  - `quick updates-check` (runs apt list --upgradable)
  - `quick updates-apply [--dry-run]` (runs apt upgrade)
- [ ] Document in skills/tools.md and maybe CRON_JOBS.md (not auto-scheduled yet)
- [ ] Safety: require explicit `--execute` for apply; default dry-run

## Phase 3: Documentation Updates
- [ ] Update `CRON_JOBS.md`:
  - Add `cleanup-backups-cron` description (weekly Sunday 07:00 Bangkok)
  - Add note about log-rotation now including agent logs
  - Mention updates management commands (manual)
- [ ] Update `TOOLS.md` with new commands (`updates-check`, `updates-apply`)
- [ ] Update `MEMORY.md` with this build's summary after validation

## Phase 4: Validation
- [ ] Run `quick health` and verify no errors
- [ ] Run `quick updates-check` to confirm it works
- [ ] Verify systemd linger: `loginctl show-user ubuntu -p Lingering`
- [ ] Check `openclaw cron list` shows new backup-cleanup job (if added)
- [ ] Test agent log rotation manually (simulate large log)
- [ ] Ensure git status clean
- [ ] Confirm all agents still running (cron jobs active)
- [ ] Run `quick verify` for comprehensive check

## Phase 5: Commit & Close Loop
- [ ] Stage all changes (scripts, docs, quick launcher, cron config)
- [ ] Commit with prefix: `build: reliability; enable systemd linger, add backup cleanup cron, rotate agent logs, updates management`
- [ ] Push to GitHub
- [ ] Update active-tasks.md: mark validated, add verification results
- [ ] Log summary to memory via `quick log`
- [ ] Clean up planning files? According to AGENTS.md: after verification, remove task_plan.md, findings.md, progress.md or archive? Since they are per-run artifacts, they could be deleted after commit to keep workspace clean. But keeping them might be useful for audit. To align with builder's design, they should remain as the latest plan in the repo. I'll keep them but ensure they reflect the latest run.

## Risks & Mitigations
- systemd linger: requires sudo; we have passwordless sudo. Verify after enable.
- Cron job duplication: check existing jobs before adding.
- Log rotation: ensure it doesn't interfere with active writes; rotation should handle truncation safely (copytruncate or send signal). We'll use copytruncate approach to avoid needing to restart processes.
- Updates apply: never auto-apply; require human or explicit flag. Dry-run by default.

## Dependencies
- Passwordless sudo already configured (from 2026-02-15)
- OpenClaw cron management via `openclaw cron` commands
- Existing log-rotate script as base for agent log rotation
