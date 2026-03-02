# Workspace Builder Task Plan

**Session:** 23dad379-21ad-4f7a-8c68-528f98203a33  
**Trigger:** Cron (every 2h)  
**Goal:** Validate workspace health, commit pending changes, implement improvements.

---

## Phase 1: Analysis (0-5 min)

- Read active-tasks.md, MEMORY.md, daily logs (today + yesterday)
- Check git status, health summary, and constraints
- Identify untracked/modified files that need attention
- Assess memory index health and other metrics

**Status:** Completed

---

## Phase 2: Findings & Planning (5-10 min)

- Document current state in `findings.md`
- Identify improvements (e.g., add new scripts to version control, fix filters)
- Create this task plan with clear phases
- Initialize `progress.md` tracking

**Status:** In Progress

---

## Phase 3: Execution (10-20 min)

- Update active-tasks.md entry to running (if stale)
- Add/commit legitimate untracked files:
  - `scripts/update-heartbeat-state.py` (new utility)
- Create/refresh planning docs (task_plan.md, findings.md, progress.md)
- Run `./scripts/validate-constraints.sh` and confirm all pass
- Commit all changes with `build:` prefix
- Push to origin/master
- Update active-tasks.md to validated with verification metrics

**Status:** Pending

---

## Phase 4: Close the Loop (20-25 min)

- Run `quick health` to confirm green status
- Verify active-tasks.md <2KB and MEMORY.md ≤35 lines
- Ensure no temp files left behind
- Check that git is clean and pushed
- Append summary to `memory/2026-03-02.md`
- Prune stale active-tasks entries if needed to stay under limit

**Status:** Pending

---

## Success Criteria

- All constraints 10/10 satisfied
- Git clean and pushed to origin
- active-tasks.md updated with validated status and verification details
- No uncommitted legitimate outputs
- Planning docs created and versioned

---

## Contingencies

- If validation fails: debug, fix, re-run until pass
- If network issues: skip push, note in verification; retry later
- If disk space low: run cleanup before commit
