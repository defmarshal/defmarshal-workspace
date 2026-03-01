# Task Plan: Workspace Builder Session

**Session ID:** 23dad379-21ad-4f7a-8c68-528f98203a33
**Trigger:** cron:workspace-builder-cron (every 2 hours)
**Start Time:** 2026-03-01 13:02 UTC
**Goal:** Routine maintenance — enforce constraints, commit state, validate, close loop

---

## Phase 1: Analysis & Assessment

**Objective:** Gather current state snapshot (disk, memory, git, agents, constraints)

**Actions:**
1. Run `./quick health` — get system health summary
2. Run `git status` — identify modified/untracked files
3. Check disk usage trend (from disk-history.json)
4. Check active agents (from active-tasks.md)
5. Verify constraints with `./quick validate-constraints`

**Success criteria:**
- Health check completes without errors
- Git status shows only expected state files (disk-history.json)
- No constraint violations

**Status:** ✅ Complete — Health green, git dirty (1 file), constraints all satisfied

---

## Phase 2: Verification & Planning

**Objective:** Confirm workspace integrity, plan minimal but meaningful actions

**Assessment:**
- Disk usage: 79% (healthy, below 90% threshold)
- Downloads: 31 files, 7.6GB (stable, no cleanup needed)
- Memory index: 29 fragments / 322 chunks, reindex 1.2d ago (fresh)
- active-tasks.md: 1235 bytes (<2KB) — healthy
- MEMORY.md: 32 lines (≤35) — healthy
- No stale idea branches
- No temp files
- APT updates: none pending
- Gateway: healthy

**Planned actions:**
1. Stage modified file: `memory/disk-history.json`
2. Create planning docs (task_plan.md, findings.md, progress.md) if not already present
3. Commit changes with `build:` prefix
4. Push to origin/master
5. Validate constraints again
6. Update active-tasks.md: mark session validated with verification metrics
7. Prune stale completed entries (maintain <2KB)

**Success criteria:**
- All commits pushed
- active-tasks.md updated with verification details
- Constraints remain satisfied
- No temp files left behind

---

## Phase 3: Implementation & Documentation

**Objective:** Execute plan, commit, push, document

**Steps:**
1. `git add memory/disk-history.json`
2. `git commit -m "build: update disk history metrics"`
3. If planning docs modified/created: `git add task_plan.md findings.md progress.md` then commit with `build: workspace-builder planning docs and session registration`
4. `git push origin master`
5. Run `./quick validate-constraints` to verify
6. Edit active-tasks.md:
   - Ensure running entry exists with session key
   - Add verification notes (sizes, health status, counts)
   - Change status to `validated`
7. Prune old completed entries to keep file <2KB

**Verification commands to include in active-tasks:**
- `./quick validate-constraints` output summary
- active-tasks size: X bytes (<2KB)
- MEMORY.md lines: Y (≤35)
- Health: green
- Git: clean & pushed
- Memory reindex: Z day(s) fresh
- No temp files: ✅
- Shebang check: ✅
- APT: none pending
- Branch hygiene: ✅
- Downloads: N files, X.XGB

---

## Phase 4: Validation & Closure

**Objective:** Confirm everything is clean, push final state, close session

**Final validation checklist:**
- [ ] `./quick health` passes
- [ ] `./quick validate-constraints` all ✅
- [ ] `git status` clean (nothing to commit)
- [ ] No temp files (`find . -type f -name "*.tmp" -o -name "*.temp" -o -name "*~"` empty)
- [ ] active-tasks.md ≤ 2KB
- [ ] MEMORY.md ≤ 35 lines
- [ ] All commits pushed to origin

**Close the loop:**
- Append summary to `memory/2026-03-01.md` daily log
- Update active-tasks.md entry with final verification
- Mark session `validated`

**If any check fails:** Debug immediately, fix issue, re-run validation before proceeding.

---

## Success Definition

✅ All constraints satisfied after commit
✅ Git clean & pushed
✅ active-tasks.md updated with verification metrics and pruned to <2KB
✅ Daily log updated
✅ No leftover temp files or untracked artifacts
✅ Session marked validated in active-tasks.md

**Outcome:** Workspace synchronized, verifiably healthy, and fully documented.
