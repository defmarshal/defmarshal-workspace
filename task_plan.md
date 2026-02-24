# Workspace Builder Plan

**Mission:** Analyze workspace state and implement meaningful improvements while maintaining hygiene constraints.

**Session Key:** 23dad379-21ad-4f7a-8c68-528f98203a33

**Constraints (Non-Negotiable):**
- active-tasks.md ≤ 2KB
- MEMORY.md ≤ 30 lines
- Git clean, no temp files
- All changes committed with `build:` prefix
- Close-the-loop validation before marking validated

**Current State Analysis:**
- Health: OK (disk 67%, gateway healthy, memory clean)
- Git: clean (0 changed)
- Stale branch detected: `idea/write-a-rudra-safe-fix-pattern` (successful idea, unmerged)
- active-tasks.md: 44 lines (~2400b) → needs pruning to ≤2KB
- MEMORY.md: 30 lines (optimal)
- Idea executor: idle

**Implementation Plan:**

### Phase 1: Cleanup Stale Resources
1. Delete stale idea branch: `git branch -D idea/write-a-rudra-safe-fix-pattern`
2. Verify branch removed

### Phase 2: active-tasks.md Optimization
1. Check current size: `wc -c < active-tasks.md`
2. Prune oldest completed entries (pre-2026-02-24) until size < 2KB
3. Shorten verification descriptions to save space (e.g., "health OK" instead of longer phrases)
4. Re-check size: must be ≤ 2048 bytes

### Phase 3: Validation & Documentation
1. Run `./quick health` to verify system health
2. Confirm no temp files: `git status --porcelain` should show only tracked files
3. Update planning docs (this file, findings.md, progress.md) with actual results
4. Commit changes: `git add -A && git commit -m "build: workspace hygiene - cleanup stale branches, prune active-tasks"`
5. Push to origin

### Phase 4: Active Tasks Update
1. Add validated entry for this session to active-tasks.md
2. Commit: `git commit -am "build: mark workspace-builder session validated (2026-02-24 15:24 UTC run)"`
3. Push

### Phase 5: Final Close-the-Loop
1. Re-run `./quick health` to confirm post-commit cleanliness
2. Verify active-tasks.md size still ≤2KB
3. Verify MEMORY.md ≤30 lines (unchanged)
4. Check no idea branches remain: `git branch -a | grep idea/` should be empty
5. Final commit of planning updates and push

**Error Handling:**
- If git push fails → check remote status, pull/merge if needed, retry
- If active-tasks.md cannot be pruned under 2KB → contact human for manual review (unlikely)
- If health check fails → investigate, log error, abort commit until resolved

**Success Criteria:**
- active-tasks.md ≤ 2KB
- MEMORY.md ≤ 30 lines (maintained)
- Git clean, no temp files, no stale branches
- All changes committed with `build:` prefix
- Session marked validated in active-tasks.md
