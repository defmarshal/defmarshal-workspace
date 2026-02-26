# Workspace Builder Plan
**Session:** 2026-02-26 05:07 UTC
**Goal:** Analyze workspace and implement meaningful improvements while enforcing constraints

## Current State
- All constraints satisfied (validate-constraints passes)
- active-tasks.md: 1902 bytes (<2KB)
- MEMORY.md: 30 lines (≤35)
- Git clean, health green
- 6 local idea branches present (executed/validated)
- Memory reindex age: 2.1 days (fresh enough)
- Cron schedules match documentation

## Proposed Improvements

### Phase 1: Repository Hygiene
**Why:** Stale branches cause clutter and confusion. Clean up to maintain clarity.
- Identify all local `idea/*` branches
- Check execution logs to determine which are truly completed/stale
- Delete stale branches
- Verify no remote tracking branches remain

### Phase 2: Robustness Enhancement
**Why:** validate-constraints script shows a warning about APT parsing; improve reliability.
- Update APT check to handle different output formats gracefully
- Add fallback patterns for various `quick updates-check` outputs
- Maintain exit code behavior (0=safe, 1=fail, warnings don't fail)
- Test the updated script

### Phase 3: Documentation Sync
**Why:** Keep CRON_JOBS.md accurate; proposal for research-digest-cron may need status update.
- Review the "Additional OpenClaw Cron Jobs (Proposed)" section
- Determine if research-digest-cron should be marked as implemented or remain proposed
- Update status accordingly (likely mark as completed since it exists in cron list)
- If found in actual cron, move to active list or add completion note

### Phase 4: Close the Loop
- Run `./quick health`
- Run `./quick validate-constraints`
- Check `git status` (should be clean)
- Verify no temp files
- Commit changes with prefix `build:`
- Push to origin
- Update active-tasks.md with validation entry

## Success Criteria
- All constraints remain satisfied
- No stale branches (only recent/active idea branches if any)
- validate-constraints script warning resolved
- Documentation reflects reality
- Changes committed and pushed
- active-tasks.md updated with this session's entry (size <2KB)

## Risk Mitigation
- Each phase validated before proceeding
- If any step fails, debug and retry
- Keep changes small and traceable
- Ensure active-tasks.md stays under 2KB throughout
