# Workspace Builder Task Plan
**Date**: 2026-02-18 17:00 UTC
**Session**: cron:23dad379-21ad-4f7a-8c68-528f98203a33
**Goal**: Implement improvements aligned with long-term objectives: system stability, correctness, and maintainability.

## Context
- System health: OK (disk 40%, gateway healthy, memory clean)
- Cron schedules: Correct after previous fix, but meta-agent can corrupt them again
- Meta-agent: Contains flawed resource-based scheduling that threatens schedule integrity
- Validation: Need safety net to enforce documented schedules

## Phases & Tasks

### Phase A: Fix Meta-Agent Schedule Corruption
**Priority**: Critical
**Why**: Meta-agent's `adjust_scheduling` function incorrectly changes cron schedules, breaking timing semantics and causing resource spikes.
- A1: Review `agents/meta-agent.sh` to locate `adjust_scheduling` call (line ~402)
- A2: Disable the call by commenting it out or guarding with a feature flag
- A3: Test meta-agent with `--once` to ensure it runs without errors and does not alter schedules
- A4: If successful, commit as `build: disable meta-agent schedule adjustments to preserve integrity`

### Phase B: Add Cron Schedule Validation (Safety Net)
**Priority**: High
**Why**: Prevent drift from CRON_JOBS.md due to manual changes or other agents.
- B1: Create `scripts/validate-cron-schedules.sh` with intended schedule mappings (from CRON_JOBS.md)
- B2: Script logic:
  - For each known job, fetch current schedule via `openclaw cron list`
  - Compare with intended expression
  - If mismatch, run `openclaw cron update --jobId <id> --cron "<intended>"`
  - Log actions
- B3: Integrate validation into `agents/agent-manager.sh` as a periodic check (call script)
- B4: Add quick command `cron-schedules` that runs the validation and shows status
- B5: Test manually: introduce a deliberate mismatch, run `quick cron-schedules`, verify correction

### Phase C: Documentation Updates
**Priority**: Medium
- C1: Update `TOOLS.md`:
  - Add `cron-schedules` quick command description
  - Note that meta-agent schedule adjustments are disabled (pending rework)
  - Clarify memory-dirty benign stores
- C2: Update `AGENTS.md` if necessary about meta-agent behavior
- C3: Add entry to `lessons.md` describing the meta-agent schedule bug and fix

### Phase D: Final Validation & Commit
**Priority**: Critical
- D1: Run `./quick health` – ensure system OK
- D2: Run `./quick cron-schedules` – check for no mismatches
- D3: Run `./quick memory-dirty` – verify memory state
- D4: Run `./quick mem` and `./quick search test` to confirm memory search works
- D5: Verify `git status` clean, no temp files
- D6: Commit all changes with prefix `build:`
- D7: Update `active-tasks.md`: mark this run as validated, add verification results
- D8: Push to origin/master

---

## Risk Mitigation
- If meta-agent fix causes other issues, we can revert to previous commit and redesign.
- Schedule validation uses conservative mappings; will not alter jobs not in the list.
- All changes will be committed and pushed; failures will be logged in `progress.md`.
