# Workspace Builder Plan

**Session:** 2026-02-28 17:05 UTC (cron-triggered)
**Goal:** Restore git clean state, enforce constraints, and close the loop

---

## Phase 1: Analyze (Done)
- ✅ Read current workspace state
- ✅ Validated constraints: active-tasks OK (1329b), MEMORY 31 lines, health green, no temp files, shebangs OK, APT none, memory fresh, branches clean
- ❌ Git dirty: 2 modified files (`apps/dashboard/data.json`, `memory/disk-history.json`)

## Phase 2: Execute
### Step 2.1: Commit pending state files
- [ ] Stage both files
- [ ] Commit with message: `build: commit auto-generated state files (dashboard metrics, disk history)`

### Step 2.2: Verify git clean
- [ ] Run `git status` to confirm no unstaged changes

### Step 2.3: Update active-tasks.md
- [ ] Find current running entry `[workspace-builder-<id>]` (if not present, add)
- [ ] Move to Completed with verification notes
- [ ] Prune oldest completed entries to keep size <2KB

### Step 2.4: Validate constraints
- [ ] Run `./quick validate-constraints`
- [ ] Ensure all 7 checks pass

### Step 2.5: Push to origin
- [ ] Push all commits to `origin/master`

## Phase 3: Close the Loop
- [ ] Commit planning docs (task_plan.md, findings.md, progress.md) with prefix `build:`
- [ ] Final validation: `./quick health` green, `git status` clean
- [ ] No temp files anywhere

## Phase 4: Update active-tasks.md archival
- [ ] Confirm workspace-builder entry marked validated
- [ ] Archive to daily log if needed (optional; active-tasks pruning done)

---

## Success Criteria
- All constraints satisfied ✅
- Git clean & pushed ✅
- active-tasks.md <2KB ✅
- No temp files ✅
- Workspace builder session properly documented ✅
