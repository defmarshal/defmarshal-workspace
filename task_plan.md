# Workspace Builder Plan - 2026-02-24 15:17 UTC

**Session:** workspace-builder-<session-id>
**Goal:** Strategic workspace improvements through targeted maintenance and hygiene enforcement

## Analysis Phase

### Items to verify
- [ ] Git status: check for uncommitted changes, stale branches
- [ ] System health: disk, gateway, memory status
- [ ] active-tasks.md size and format (<2KB, proper entries)
- [ ] MEMORY.md line count (≤30 lines) and accuracy
- [ ] Pending APT updates (security relevance)
- [ ] Idea pipeline state (executor/generator health)
- [ ] Stale feature branches (idea/*)
- [ ] Temporary files or artifacts to clean
- [ ] Research outputs properly tracked
- [ ] Daily digest up-to-date

### Potential improvements
- Apply pending APT updates (17 updates noted in 12:05 run) during low-activity window
- Run memory reindex if indicated (Voyage disabled, local FTS+ active)
- Test git-branch-cleanup utility
- Verify idea executor can successfully execute an idea
- Ensure no stale branches remain
- Prune active-tasks.md if >2KB
- Validate all cron jobs operational
- Update planning docs and MEMORY.md as needed
- Close the loop: validate health, commit with 'build:' prefix, mark session validated

## Execution Phases

1. **Initial Assessment** - Run health checks, git status, active-tasks size
2. **Issue Identification** - Document any constraints or problems in findings.md
3. **Implement Fixes** - Apply updates, clean branches, prune files
4. **Validation** - Run ./quick health, test modified commands, verify no temp files
5. **Documentation** - Update planning files, MEMORY.md if significant learnings
6. **Commit & Push** - Commit all changes with proper prefix
7. **Finalize** - Update active-tasks.md with validation notes

## Success Criteria
- active-tasks.md ≤ 2KB
- MEMORY.md ≤ 30 lines
- Git clean after pushes (0 uncommitted changes)
- No stale idea branches
- ./quick health returns OK
- No temp files left behind
- All changes committed with 'build:' prefix
