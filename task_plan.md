# Task Plan - Workspace Builder (2026-02-24 09:07 UTC)

## Objective
Implement automated cleanup of stale `idea/*` branches to reduce manual maintenance and prevent branch accumulation.

## Current State
- No stale branches exist currently (system clean)
- Manual deletion performed in previous builder cycles when stale branches detected
- Git-janitor handles auto-commits but not branch cleanup
- Idea executor leaves feature branches intact for manual review (policy: retain after success for review)

## Problem
Stale idea branches (from rejected or long-completed ideas) accumulate if not manually cleaned. This creates clutter and increases cognitive load.

## Proposed Solution
Add automated stale branch cleanup to **git-janitor-cycle.sh** with safe guards:
- Define stale threshold: branches older than 7 days (configurable)
- Only delete `idea/*` branches that are fully merged into master (safe)
- Log cleanup actions
- Respect policy: keep successful branches for 7 days before deletion

## Steps

1. Analyze git-janitor current behavior and structure
2. Design branch cleanup logic with safety constraints
3. Implement cleanup function in `agents/git-janitor-cycle.sh`
4. Test manually (dry-run mode)
5. Update documentation (CRON_JOBS.md if needed)
6. Close-the-loop validation:
   - Run `./quick health`
   - Verify git-janitor runs clean
   - Check active-tasks.md size (<2KB)
   - Confirm MEMORY.md ≤30 lines
   - Ensure no temp files, git clean
7. Commit changes with `build:` prefix and push

## Success Criteria
- Automated cleanup runs without manual intervention
- Only merged, stale (>7d) idea branches removed
- No accidental deletion of active branches
- Updated planning documents committed
- All validation checks pass
