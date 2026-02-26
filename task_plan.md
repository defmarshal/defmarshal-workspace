# Workspace Builder Task Plan
**Session:** workspace-builder-20260226-1505  
**Trigger:** Cron (workspace-builder-cron)  
**Started:** 2026-02-26 15:05 UTC  
**Goal:** Perform strategic workspace maintenance and enforce constraints

---

## Phase 1: Pre-flight Analysis
- Record current state: git status, active-tasks.md size, MEMORY.md lines, idea branches count, downloads count, health status
- Verify constraints via `./quick validate-constraints`
- Identify issues: stale branches, size overflows, pending work

## Phase 2: Cleanup Stale Branches
- Delete local idea branches older than threshold (none > 2h but stale if abandoned)
  - `idea/create-a-health-check-for`
  - `idea/integrate-content-digest-with-telegram`
- Verify removal with `git branch --list 'idea/*'`
- Attempt remote deletions if needed (likely local only)

## Phase 3: Constraint Validation
- Run `./quick validate-constraints` to ensure all checks pass
- If failures: debug and fix before proceeding

## Phase 4: Documentation
- Create planning docs:
  - `findings.md` — analysis of current state and issues found
  - `progress.md` — step-by-step execution log with timestamps
- Update `active-tasks.md`:
  - Add running entry (session key: workspace-builder-20260226-1505)
  - After validation, update to validated status with verification metrics
  - Prune oldest completed entry to maintain <2KB

## Phase 5: Commit & Push
- Commit changes:
  - active-tasks.md
  - task_plan.md, findings.md, progress.md
- Commit message prefix: `build:`
- Push to origin

## Phase 6: Post-Commit Validation
- Run `./quick health`
- Run `./quick validate-constraints`
- Verify `git status` clean
- Confirm remote up-to-date

## Success Criteria
- All constraints satisfied (active-tasks <2KB, MEMORY ≤35 lines, git clean, health green, no temp files)
- Stale idea branches removed
- All changes committed and pushed
- active-tasks.md updated with validated entry
- Planning documentation complete and accurate

## Error Handling
- If any command fails: log error in progress.md, debug, retry or adjust plan
- If validation fails: fix root cause, re-run validation, document resolution
