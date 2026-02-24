# Workspace Builder Session Plan
**Date:** 2026-02-24 23:00 UTC  
**Goal:** Maintain workspace hygiene, commit pending content changes, validate constraints, and push to origin.

## Analysis Phase
- [x] Read SOUL.md, USER.md, active-tasks.md, MEMORY.md, daily logs (2026-02-23, 2026-02-24)
- [x] Check git status: 1 modified file (content/INDEX.md)
- [x] Verify health metrics: Disk 68%, Gateway healthy, Memory clean, Downloads 5.7G
- [x] Check constraints: active-tasks.md 1913b (<2KB), MEMORY.md 30 lines, 0 stale idea branches
- [ ] Identify improvements needed

## Implementation Phase
1. Commit content/INDEX.md changes with appropriate message
2. Verify active-tasks.md size remains <2KB after adding new entry
3. Verify MEMORY.md remains ≤30 lines (no changes needed)
4. Check for any other uncommitted files (none expected)
5. Update active-tasks.md with validated entry for this session
6. Commit the active-tasks.md update
7. Push all commits to origin

## Validation Phase (Close the Loop)
- Run `./quick health` and confirm OK
- Verify git status clean
- Confirm no temp files
- Check no stale idea branches
- Validate active-tasks.md size <2KB
- Validate MEMORY.md ≤30 lines
- Ensure all commits pushed

## Known Constraints
- active-tasks.md ≤ 2048 bytes (strict limit)
- MEMORY.md ≤ ~30 lines (curated memory)
- No untracked files (except transient locks in .clawhub)
- All changes must be committed with 'build:' prefix
- All commits must be pushed to origin

## Risk Mitigation
- If active-tasks.md exceeds limit after adding entry: prune oldest entries and shorten verification text
- If MEMORY.md exceeds lines: condense entries, remove blank lines
- If push fails: check network, retry, or abort with error logged to daily log
