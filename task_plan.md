# Workspace Builder Session Plan

**Session Key:** 23dad379-21ad-4f7a-8c68-528f98203a33
**Started:** 2026-02-27 03:10 AM UTC
**Goal:** Strategic maintenance: enforce constraints, clean workspace, validate health, and document outcomes

---

## Context

- **Previous run:** 2026-02-27 01:09 UTC (successful, validated)
- **Current state:** Healthy but git dirty (INDEX.md timestamp update)
- **Constraints to enforce:**
  - active-tasks.md ≤ 2KB
  - MEMORY.md ≤ 30 lines
  - Git clean & pushed
  - No temp files, no stale branches
  - Health green
  - Memory reindex age acceptable (<4 days)

---

## Phase 1: Analysis & Diagnosis

**Objective:** Understand current workspace state and identify issues

**Steps:**
1. Run `./quick health` and capture output
2. Run `./quick validate-constraints` (check if exists)
3. Check git status and identify uncommitted changes
4. Check active-tasks.md structure (Running vs Completed sections)
5. Look for stale branches (`git branch --list 'idea/*'`)
6. Look for temp files (`find . -name "*.tmp" -o -name "*~"`)
7. Check memory index age and health
8. Verify quick commands functionality (agents-summary, etc.)

**Success criteria:** Complete understanding of all violations and opportunities

---

## Phase 2: Cleanup & Corrections

**Objective:** Fix all identified issues

**Steps:**
1. Commit any pending changes (e.g., INDEX.md timestamp update)
2. Push commits to origin if needed
3. Delete stale idea branches if any
4. Remove temp files if any
5. Reorganize active-tasks.md:
   - Move validated entries from Running to Completed
   - Prune oldest completed entries to stay <2KB
   - Add current session entry (status: running)
6. Ensure MEMORY.md size ≤ 30 lines
7. Fix any broken quick commands or missing files

**Success criteria:** All constraints passing, workspace clean

---

## Phase 3: Documentation & Validation

**Objective:** Document work and verify completeness

**Steps:**
1. Create/update planning docs (task_plan.md, findings.md, progress.md)
2. Run comprehensive validation:
   - `./quick validate-constraints`
   - `./quick health`
   - `./quick git-status`
3. Verify:
   - No untracked files (except expected)
   - active-tasks.md size < 2KB
   - MEMORY.md ≤ 30 lines
   - All services healthy
4. If all green, commit planning docs with prefix 'build:'
5. Push commit to origin

**Success criteria:** All validations pass, changes committed and pushed

---

## Phase 4: Close The Loop

**Objective:** Mark session validated and update active-tasks

**Steps:**
1. Update active-tasks.md:
   - Change current entry status from running → validated
   - Add verification notes (size metrics, validation results)
2. Prune oldest completed entry if size approaching 2KB
3. Final validation sweep
4. Commit active-tasks.md update
5. Push to origin

**Success criteria:** active-tasks.md organized, session fully documented, remote synced

---

## Notes

- Keep changes small and focused
- Follow text-over-brain principle: document everything
- Use `memory_get` for specific lines if needed
- Respect existing patterns (see previous logs in memory/)

---

**Status:** 📋 Planning phase ready → Ready to execute
