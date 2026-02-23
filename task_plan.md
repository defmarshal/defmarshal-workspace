# Workspace Builder Task Plan
**Session:** 2026-02-23 11:12 UTC
**Goal:** Clean up stale artifacts, track published research, and maintain documentation hygiene

## Phase 1: Analyze Current State ✅ COMPLETED
- ✅ Read active-tasks.md, MEMORY.md, daily logs
- ✅ Check git status (1 untracked research file in public/research/)
- ✅ Check idea executor status (idle, last run rejected one idea)
- ✅ Identify stale idea branches: `idea/add-a-new-quick-utility`, `idea/write-a-rudra-safe-fix-pattern`
- ✅ Verify Research Hub prebuild process syncs from /research/ to public/research/

## Phase 2: Track Published Research Files
**Rationale:** Research agent produced a new report with MP3 companion. The files exist in `/research/` (tracked) and have been synced to `public/research/` via prebuild. The public files should also be tracked as part of the Research Hub's static assets.

**Actions:**
- Add `apps/research-hub/public/research/2026-02-23-quantum-computing-commercialization-2026-outlook.md`
- Add `apps/research-hub/public/research/2026-02-23-quantum-computing-commercialization-2026-outlook.mp3`
- Verify git status shows these as staged

## Phase 3: Delete Stale Idea Branches
**Rationale:** Both branches are left over from executor runs. The first was rejected; the second succeeded. Both should be removed to keep branch list clean.

**Actions:**
- Checkout master (if not already)
- Delete local branches: `git branch -D idea/add-a-new-quick-utility idea/write-a-rudra-safe-fix-pattern`
- Verify branch removal with `git branch -a`

## Phase 4: Documentation Hygiene
**MEMORY.md trim:** Currently 34 lines, needs ≤30. Keep:
- Personal and project metadata (lines 1-10)
- Learnings section: condense to 4-5 bullet lines summarizing recent improvements
  - 2026-02-23: Generator quality fix (deduplication, printf steps), executor validation working
  - 2026-02-23: Research Hub prebuild sync, tracking public research artifacts
  - Keep other recent learnings (meta-agent, TTS polyglot, capability evolver) as-is
- Remove any redundant phrasing

**active-tasks.md:** Ensure entry for this session will be added after validation.

**Progress tracking:** Create/update progress.md throughout.

## Phase 5: Commit and Validate
**Commit strategy:**
- First commit: Add research files (build: prefix)
- Second commit: Delete stale branches and documentation updates (build: prefix)
- Or combine into one commit if all changes are cohesive.

**Validation checklist:**
- Run `./quick health` → OK
- Check active-tasks.md size <2KB
- Check MEMORY.md line count ≤30
- Ensure no temp files
- Git clean after push

**Final step:** Add validated entry to active-tasks.md with verification notes.
