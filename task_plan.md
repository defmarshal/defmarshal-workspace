# Workspace Builder - Task Plan

**Session:** workspace-builder (cron)
**Date:** 2026-02-21 23:00 UTC
**Goal:** Fix cron monitoring issue (agent-manager-cron timeout) and perform validation

---

## Phase 1: Assessment & Planning

### Analysis
- Read active-tasks.md → added current session entry
- Checked cron status (`quick cron-health`) → agent-manager-cron shows ✗ error
- Investigated agent-manager.sh → spawns content/research agents with 10min timeout, but cron job timeout is only 5min (300s). This mismatch causes timeout errors.
- Confirmed manual run of agent-manager.sh --once completes OK within time, but cron kills it after 300s when agents take longer.

### Findings Summary
- **Issue**: agent-manager-cron has `timeoutSeconds: 300` but its payload runs `agent-manager.sh --once`, which may spawn agents with 600000ms (10min) timeout, risking overshoot.
- **Impact**: Cron job status shows error; may skip maintenance cycles.
- **Fix**: Increase agent-manager-cron timeout to 900 seconds (15 minutes) to accommodate.
- **Doc Sync**: CRON_JOBS.md should reflect the new timeout (if we choose to document it there).

---

## Phase 2: Execution Plan

### Task 1: Update Cron Job Timeout
- Use `openclaw cron update` to set `timeoutSeconds` to 900 for agent-manager-cron.
- Verify via `openclaw cron list --json` that the change took effect.

### Task 2: Validate the Fix
- Run `./quick cron-health` to confirm agent-manager-cron status is now OK.
- Optionally run `./agents/agent-manager.sh --once` to sanity-check it completes cleanly.
- Run `./quick health` to ensure overall health.

### Task 3: Record the Improvement
- Append a new entry to `memory/2026-02-21.md` describing the problem, fix, and verification.
- Optionally add a note to `CRON_JOBS.md` if deemed appropriate (e.g., mention increased timeout in job description).

### Task 4: Update active-tasks.md
- Mark this session entry as `validated`.
- Add verification notes summarizing the change and check results.

### Task 5: Commit & Push
- Stage all modified files (memory log, active-tasks.md, maybe CRON_JOBS.md).
- Commit with message prefix `build:` (e.g., "build: increase agent-manager-cron timeout to 900s to prevent errors").
- Push to origin.
- Verify push succeeded and remote is up to date.

---

## Phase 3: Close the Loop

- Run final health check (`./quick health`) to ensure workspace remains clean.
- Check `git status` – working tree should be clean.
- Ensure no temp files remain.
- Confirm `active-tasks.md` size < 2KB.
- All validations passed → commit done.

---

## Success Criteria

✅ agent-manager-cron timeout increased to 900s  
✅ Cron health shows no errors for agent-manager  
✅ Memory log updated with fix details  
✅ active-tasks.md reflects validated session  
✅ Changes committed and pushed  
✅ Overall health remains OK
