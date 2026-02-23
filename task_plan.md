# Workspace Builder Task Plan
**Session:** 2026-02-23 09:08 UTC
**Goal:** Strategic improvements based on current state analysis

## Phase 1: Analyze Current State (COMPLETED)
- ✅ Read active-tasks.md, MEMORY.md, daily logs
- ✅ Check git status (clean)
- ✅ Check idea executor status (idle, 1 rejected idea)
- ✅ Identify stale idea branch: `idea/build-a-voice-based-tts-news`
- ✅ Review idea generator quality issues (low-value template placeholders)

## Phase 2: Immediate Hygiene Fixes
- Delete stale idea branch
- Verify no other stale branches remain
- Clean up any orphaned artifacts

## Phase 3: Improve Idea Generator Quality
**Problem:** Generator produces low-value ideas that only "touch quick" without substantive changes.
**Root cause:** Templates and step generation encourage minimal placeholder commits.

**Actions:**
- Enhance templates to include actual implementation steps (not just "touch quick")
- Add deduplication: check slug uniqueness before emitting
- Expand inspiration sources: analyze git log for common patterns, check memory files for recurring themes
- Improve steps generation: avoid generic `touch quick` as the only file modification

## Phase 4: Documentation Updates
- Update findings.md with analysis and changes
- Update progress.md throughout execution
- Ensure MEMORY.md stays within 30 lines (currently 34)

## Phase 5: Close the Loop Validation
- Run `./quick health`
- Check active-tasks.md size (<2KB)
- Verify git clean after commits
- Ensure no temp files left
- Push changes with `build:` prefix

## Phase 6: Update active-tasks.md
- Add validated entry with verification notes

---

**Success criteria:**
- Stale branch deleted
- Idea generator produces at least 2 substantive ideas (≥5 lines changed, modifies non-quick files)
- Generator deduplicates slugs
- All validation checks pass
- Commits pushed with proper prefixes
