# Workspace Builder - Task Plan

**Started**: 2026-02-18 14:00 UTC  
**Session**: cron:23dad379-21ad-4f7a-8c68-528f98203a33  
**Goal**: Analyze workspace health, fix cron schedule misconfiguration, and validate system

---

## Phase 1: Analysis & Discovery

### Observations
- System health: ✅ Good (41% disk, clean git, memory clean, gateway healthy)
- active-tasks.md: 39 lines, 4.0K (within 2KB limit)
- **CRITICAL ISSUE**: 9 cron jobs incorrectly set to `0 * * * *` (every hour) instead of intended schedules
  - workspace-builder (doc: 2h) → actual: hourly
  - random-torrent-downloader (doc: 2h) → actual: hourly
  - dev-agent-cron (doc: every 20min 08-22) → actual: hourly 24/7
  - content-agent-cron (doc: every 10min 08-22) → actual: hourly 24/7
  - research-agent-cron (doc: every 15min 08-22) → actual: hourly 24/7
  - agni-cron (doc: 2h) → actual: hourly
  - agent-manager-cron (doc: 30min) → actual: hourly
  - supervisor-cron (doc: 5min) → actual: hourly
  - meta-agent-cron (doc: hourly) → actual: hourly (CORRECT)

### Risks of Mis-scheduling
- Over-spawning: agents run more frequently than intended, wasting resources
- Loss of intended timing semantics (e.g., supervisor should check every 5min, not 60min)
- Potential agent collisions and race conditions
- Inconsistent with documentation (CRON_JOBS.md)

---

## Phase 2: Fix Cron Schedules

### Target Corrections

| Job Name                  | Intended Schedule (from CRON_JOBS.md)   | Correct Cron Expression       |
|---------------------------|------------------------------------------|-------------------------------|
| workspace-builder         | Every 2 hours                            | `0 */2 * * *`                 |
| random-torrent-downloader | Every 2 hours (UTC)                      | `0 */2 * * *`                 |
| dev-agent-cron            | Every 20min (08:00-22:00 Asia/Bangkok)  | `0,20,40 8-22 * * *`          |
| content-agent-cron        | Every 10min (08:00-22:00 Asia/Bangkok)  | `0,10,20,30,40,50 8-22 * * *` |
| research-agent-cron       | Every 15min (08:00-22:00 Asia/Bangkok)  | `0,15,30,45 8-22 * * *`       |
| agni-cron                 | Every 2 hours (UTC)                      | `0 */2 * * *`                 |
| agent-manager-cron        | Every 30 minutes                         | `0,30 * * * *`                |
| supervisor-cron           | Every 5 minutes                          | `*/5 * * * *`                 |
| meta-agent-cron           | Every hour                               | `0 * * * *` (already correct) |

**Note**: vishwakarma-cron and weekly jobs are already correct; no changes needed.

### Action Steps
1. For each mis-scheduled job, use `openclaw cron update` to set correct `schedule.expr`
2. Verify changes via `openclaw cron list --json`
3. Check logs to ensure no immediate adverse effects

---

## Phase 3: Documentation Sync

- Ensure CRON_JOBS.md matches the corrected actual schedules
- Update any other references if needed

---

## Phase 4: Validation

- Run `./quick health` → must be OK
- Verify cron list shows corrected schedules
- Check that no agents are currently locked or failing
- Confirm active-tasks.md still under 2KB
- Git status clean

---

## Phase 5: Close the Loop

- Commit all changes with prefix `build:`
- Push to GitHub
- Update active-tasks.md: mark session validated, add verification results
- If any step fails, debug and document in findings.md / progress.md

---

## Success Criteria

✓ All 9 mis-scheduled jobs corrected to intended frequencies  
✓ Documentation matches reality  
✓ System health remains stable  
✓ No lingering temp files or untracked changes  
✓ Git push successful  
✓ active-tasks.md updated with validation
