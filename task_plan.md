# Workspace Builder Task Plan

**Session Key:** workspace-builder-20260223-2300  
**Trigger:** Cron schedule (every 2h UTC)  
**Timestamp:** 2026-02-23 23:00 UTC

---

## Mission

Analyze workspace health, enforce constraints, and implement meaningful improvements.

---

## Constraints

- active-tasks.md must be ≤ 2KB (2048 bytes)
- MEMORY.md must be ≤ 30 lines
- Git must be clean after validation
- No temp files
- All planning docs must be committed with `build:` prefix
- Close the loop: run `quick health`, verify changes, then commit

---

## Current State (Pre-Analysis)

- **Git status:** Clean (no changed files)
- **Disk usage:** 67% (healthy)
- **Gateway:** Healthy
- **Memory index:** Clean, stale (7d) but acceptable
- **MEMORY.md:** 30 lines (optimal)
- **active-tasks.md:** 2062 bytes, 39 lines → **NEEDS PRUNING** (14 bytes over limit)
- **Stale branches:** None (checked)
- **Temp files:** None
- **Uncommitted research artifacts:** None

---

## Phase 1: Analysis & Findings

**Goal:** Document current state and identify all issues.

**Tasks:**
1.1 Check active-tasks.md size and content  
1.2 Verify MEMORY.md line count  
1.3 Check git status for any modified/untracked files  
1.4 Check for stale idea branches  
1.5 Check for temp files  
1.6 Check workspace health via `quick health`  
1.7 Record all findings in `findings.md`

---

## Phase 2: Implementation

**Goal:** Fix any violations.

**Planned actions:**
2.1 Prune `active-tasks.md` to ≤ 2KB
   - Strategy: Remove oldest entries that are already well-archived in daily logs
   - Keep at least 3-5 recent entries for context
   - Optionally shorten verification lines to save bytes
2.2 Verify MEMORY.md remains ≤ 30 lines (no action if already compliant)
2.3 Ensure no temp files or untracked artifacts

---

## Phase 3: Close the Loop

**Goal:** Validate workspace hygiene.

**Validation checks:**
- `./quick health` passes
- active-tasks.md size < 2048 bytes
- MEMORY.md ≤ 30 lines
- Git clean (no uncommitted changes after commits)
- No temp files
- All planning docs committed with `build:` prefix
- Feature branches cleaned (only master)

**Actions:**
3.1 Create `progress.md` and update throughout  
3.2 Commit changes (if any)  
3.3 Update `active-tasks.md` with validated entry for this session  
3.4 Push to origin  
3.5 Final validation

---

## Phase 4: Memory Updates (If Needed)

If any important learnings emerged during this run, update MEMORY.md while keeping ≤ 30 lines. Likely no changes needed as this is routine maintenance.

---

## Success Criteria

- active-tasks.md ≤ 2KB
- MEMORY.md ≤ 30 lines
- All validation checks pass
- Commits pushed
- active-tasks.md entry added

---

**Plan created:** 2026-02-23 23:00 UTC  
**Estimated duration:** 5-10 minutes
