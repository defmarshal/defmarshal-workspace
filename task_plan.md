# Task Plan: Finalize Migration and System Health
**Builder Run**: 2026-02-16 15:00 UTC (22:00 Bangkok)
**Session**: manual main session (user-initiated)

## Phase 1: Discovery & Assessment (COMPLETE)
- [x] Read active-tasks.md → only torrent-bot daemon running (good)
- [x] Check git status → 1 staged file: `content/2026-02-16-final-confirmation.md`
- [x] Run `quick health` → Disk 82%, 6 updates, git dirty, memory clean, reindex: never, gateway: orphaned
- [x] Memory status: main: 7f/43c (clean) voyage FTS+; no issues
- [x] Verify cron jobs: all 11 present, including dev-agent-cron, content-agent-cron, research-agent-cron (enabled, last run ok)
- [x] Check daemon processes: only torrent-bot running; dev/content/research daemons stopped (good)
- [x] Review docs: CRON_JOBS.md and projects.md already reflect migration (noted 2026-02-16)
- [x] Confirm start-background-agents.sh: old daemon launches commented out (good)

## Phase 2: Gap Analysis & Prioritization
**Remaining Issues**:
1. **High**: Gateway supervision gap – port 18789 listening but systemd service inactive (orphaned). Risk of unsupervis ed restart on crash.
2. **Medium**: Memory reindex log never created (expected since weekly on Sunday). Health warns "never". Manual reindex would establish baseline and silence warning.
3. **Low**: Disk usage 82% – acceptable but monitor; aria2.log already rotated weekly.
4. **Low**: Pending package updates (6). Could automate but not urgent.
5. **Pending commit**: Staged content file from content-agent not yet committed (should be committed with `build:` prefix to keep history clean).

**Priority**:
1. Fix gateway supervision (restart via systemd, ensure service enabled)
2. Perform manual memory reindex
3. Commit staged content file
4. Validate health and system functionality
5. Document this run in planning files (this file, findings.md, progress.md)
6. Push to GitHub

## Phase 3: Implementation Plan
**Step 1: Reindex memory**
- Run: `quick memory-index`
- Expected: Creates `memory/memory-reindex.log` with timestamp

**Step 2: Fix gateway**
- Check if systemd user service exists: `systemctl --user status openclaw-gateway`
- Restart via gateway command: `openclaw gateway restart` (should activate service)
- Verify: `systemctl --user is-active openclaw-gateway` → active; port still listening

**Step 3: Commit staged changes**
- Verify staged: `git diff --cached`
- Commit: `git commit -m "build: commit pending content file from content-agent"`
- Push: `git push origin master`

**Step 4: Validate**
- Run `quick health` and `quick verify` – expect disk warning still but reindex now recent, gateway healthy, git clean.
- Test `quick mem` and `quick search test` to confirm memory functions.

**Step 5: Update planning files**
- task_plan.md (this file) – already detailed
- findings.md – capture findings from this run
- progress.md – log completion and verification results

**Step 6: Finalize**
- Ensure all changes committed and pushed
- Verify no temp files left behind (e.g., staging area cleared)
- Provide summary to user

## Dependencies & Risks
- `quick memory-index` requires Voyage API; rate limits possible but index is small (7 files). Should succeed.
- Gateway restart may temporarily drop connections; acceptable during daytime.
- Disk usage warning will persist (82% >80%) but not critical.
- No risky changes; all operations are safe.

## Rollback
- If gateway restart fails, fallback to manual launch: `openclaw gateway start`
- If commit fails, resolve and retry.

## Success Criteria
- Memory reindex log created (reindex status in health: today)
- Gateway service active (systemd)
- Git clean (no pending changes after push)
- Verification passes with expected warnings (disk OK)
- Planning files updated and committed
