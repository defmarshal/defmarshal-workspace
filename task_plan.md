# Workspace Builder — Task Plan

**Session:** 23dad379-21ad-4f7a-8c68-528f98203a33
**Goal:** Commit pending changes, validate constraints, close the loop
**Strategy:** Phased execution with verification checkpoints

---

## Phase 0 — Pre-flight Checks

**Objective:** Confirm workspace state matches expectations before modifications

**Steps:**
1. Read active-tasks.md to detect conflicts (done: one entry reset to running)
2. Check git status for untracked/modified files (confirmed: memory/disk-history.json modified)
3. Verify disk health via `./quick health` (79% OK)
4. Confirm memory index is fresh (1.1d OK)

**Success criteria:**
- Only `memory/disk-history.json` modified (no untracked files)
- Health green (disk 79% acceptable)

**Fallback:** If conflicts detected, investigate before proceeding

---

## Phase 1 — Session Registration (Already Done)

**Objective:** Track this builder run in active-tasks.md

**Status:** ✅ Completed (entry reset to running at 11:01 UTC)

**Verification:** active-tasks entry updated; file size ~1.2KB (<2KB)

---

## Phase 2 — Commit Pending Changes

**Objective:** Commit `memory/disk-history.json` with proper message

**Steps:**
1. Stage `memory/disk-history.json` (ensure no other files staged)
2. Verify staged diff (`git diff --cached`)
3. Commit with prefix `build: update disk history metrics`
4. Verify commit succeeded (`git log -1`)

**Success criteria:**
- Commit created with correct message
- Commit includes only intended file
- Working tree remains otherwise clean

---

## Phase 3 — Validation

**Objective:** Run comprehensive constraint checks

**Steps:**
1. Run `./quick validate-constraints` and capture output
2. Run `./quick health` for system summary
3. Run `./quick hygiene` for file-system checks
4. Check `./quick agent-status` for cron health
5. Verify:
   - active-tasks.md size (<2KB)
   - MEMORY.md line count (≤35)
   - No temp files (`find . -maxdepth 1 -name "*.tmp" -o -name "*.temp"` etc.)
   - No stale idea branches (`git branch --list "idea/*"`)

**Success criteria:**
- All 9 constraints pass
- No hygiene violations
- All agents healthy

---

## Phase 4 — Push & Verify

**Objective:** Push commits and confirm remote sync

**Steps:**
1. Run `git push origin master`
2. Verify push succeeded (`git log origin/master -1` matches local)
3. Confirm no credentials leaked in commit history

**Success criteria:**
- Push successful
- Remote HEAD at latest commit
- No sensitive data in commit

---

## Phase 5 — Close the Loop

**Objective:** Mark session validated, archive to daily log, update active-tasks

**Steps:**
1. Update active-tasks.md entry: change `status: running` → `status: validated`
2. Add verification block with actual outputs
3. Ensure active-tasks.md remains <2KB (prune older validated entries if needed)
4. Append summary to `memory/2026-03-01.md` with session outcome
5. Verify final state: `git status` clean, all constraints green

**Success criteria:**
- active-tasks entry updated with verification metrics
- Daily log updated
- Git clean
- All constraints satisfied

---

## Phase 6 — Final Reporting

**Objective:** Output one-line summary for cron logs

**Format:**
```
✅ Workspace builder validated: active-tasks <size>b, MEM <N> lines, health green, git pushed, constraints all satisfied
```

---

## Checklist Summary

- [x] Phase 0: Pre-flight completed, no conflicts
- [x] Phase 1: Session registered (reset active-tasks entry)
- [ ] Phase 2: Changes committed with build: prefix
- [ ] Phase 3: All validation checks pass
- [ ] Phase 4: Pushed to origin/master
- [ ] Phase 5: active-tasks validated, daily log updated
- [ ] Phase 6: Summary prepared

---

**Execution:** Proceed step by step, updating `progress.md` after each phase.
