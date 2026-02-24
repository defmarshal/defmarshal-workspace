# Workspace Builder Plan

**Mission:** Analyze workspace state and implement meaningful improvements while maintaining hygiene constraints.

**Session Key:** 23dad379-21ad-4f7a-8c68-528f98203a33
**Start:** 2026-02-24 19:03 UTC

**Constraints (Non-Negotiable):**
- active-tasks.md ≤ 2KB
- MEMORY.md ≤ 30 lines
- Git clean, no temp files
- All changes committed with `build:` prefix
- Close-the-loop validation before marking validated

**Current State Analysis (19:03 UTC):**
- Health: OK (disk 68%, gateway healthy, memory clean, reindex today)
- Git: clean (0 changed)
- Stale branch: `idea/build-a-cli-game-inside` (successful idea execution, unmerged, needs deletion)
- active-tasks.md: 37 lines, 1846 bytes (already ≤2KB - no pruning needed)
- MEMORY.md: 30 lines (optimal)
- Downloads: 17 files, 5.7G (0 files >30d - no cleanup needed)
- Idea executor: idle

**Implementation Plan:**

### Phase 1: Cleanup Stale Resources
1. Verify stale branch exists: `git branch | grep build-a-cli-game-inside`
2. Delete it: `git branch -D idea/build-a-cli-game-inside`
3. Verify removal

### Phase 2: Validation & Documentation
1. Run `./quick health` to verify system health (baseline)
2. Confirm no temp files: `git status --porcelain` should show only tracked files
3. Create/update planning docs (task_plan.md, findings.md, progress.md) with actual results
4. Commit changes: `git add -A && git commit -m "build: workspace hygiene - delete stale idea branch"`
5. Push to origin

### Phase 3: Active Tasks Update
1. Add validated entry for this session to active-tasks.md with verification notes
2. Commit: `git commit -am "build: mark workspace-builder session validated (2026-02-24 19:03 UTC)"`
3. Push

### Phase 4: Final Close-the-Loop
1. Re-run `./quick health` to confirm post-commit cleanliness
2. Verify active-tasks.md size still ≤2KB
3. Verify MEMORY.md ≤30 lines (unchanged)
4. Confirm no idea branches remain: `git branch -a | grep idea/` should be empty
5. Final commit of planning docs (if needed) and push

**Error Handling:**
- If git push fails → check remote status, pull/merge if needed, retry
- If branch not found → continue (already cleaned)
- If health check fails → investigate, log error, abort until resolved

**Success Criteria:**
- stale `idea/*` branches deleted
- active-tasks.md ≤ 2KB (maintained)
- MEMORY.md ≤ 30 lines (maintained)
- Git clean, no temp files
- All changes committed with `build:` prefix
- Session marked validated in active-tasks.md
