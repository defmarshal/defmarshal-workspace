# Workspace Builder - Task Plan
**Session ID:** workspace-builder-20260225-1107
**Started:** 2026-02-25 11:07 UTC
**Goal:** Cleanup stale artifacts, enforce constraints, and validate workspace health

## Phases

### Phase 1: Analysis
- Run comprehensive health check (./quick health)
- Identify untracked files, modified tracked files, stale branches
- Verify constraints: active-tasks.md <2KB, MEMORY.md ~30 lines
- Check memory status, downloads size, pending updates
- Document findings in findings.md

**Acceptance:** All baseline metrics documented

### Phase 2: Maintenance Actions
- Delete stale idea branch `idea/add-a-new-quick-utility`
- Verify active-tasks.md size; if adding new entry exceeds 2KB, prune oldest validated entry
- Consider memory reindex if indicated (check last reindex time and dir)
- Ensure no untracked files exist (already clean)
- Run final health validation

**Acceptance:** All actions completed without errors; git remains clean

### Phase 3: Validation & Documentation
- Re-run health check (./quick health)
- Verify all constraints satisfied
- Update progress.md with detailed execution log
- Update active-tasks.md with this session's validation entry
- Commit planning documents and active-tasks update with 'build:' prefix
- Push all commits to origin

**Acceptance:** All validation checks pass; git clean; push successful

### Phase 4: Close the Loop
- Final health check
- Confirm no untracked files remain
- Verify no temp files or oversized logs
- Document final metrics

**Acceptance:** System fully validated and stable

## Error Handling
- If any command fails, log error in progress.md and halt
- Debug and retry before proceeding
- If validation fails, iterate until all constraints satisfied

## Notes
- Follow commit format: `build: <description>`
- Keep active-tasks.md size ≤2048 bytes
- Respect quiet hours if any (currently none per policy)
- Memory reindex: only if >=2 days since last, and Voyage rate limits allow (currently disabled, use local FTS+)
