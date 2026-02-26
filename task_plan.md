# Workspace Builder Task Plan

**Session Key:** workspace-builder-23dad379
**Started:** 2026-02-26 19:02 UTC
**Goal:** Strategic workspace maintenance, cleanup, and constraint enforcement

## Phases

### Phase 1: Analysis & Discovery
- Validate all workspace constraints (active-tasks size, MEMORY.md line count, git status, health)
- Identify stale branches (idea/*)
- Identify temporary files
- Review recent daily logs for any unresolved issues

### Phase 2: Cleanup & Organization
- Delete identified stale branches
- Remove temporary files
- Prune active-tasks.md if needed to maintain <2KB
- Verify active-tasks.md structure and completeness

### Phase 3: Documentation & Planning
- Create/update task_plan.md (this file)
- Create/update findings.md (analysis results)
- Create/update progress.md (execution log)
- Ensure all planning documents follow the planning-with-files workflow

### Phase 4: Validation & Commit
- Run `./quick validate-constraints` to verify all constraints
- Run `./quick health` to confirm system health
- Update active-tasks.md with validated entry and verification metrics
- Commit all changes with `build:` prefix
- Push to origin

### Phase 5: Close the Loop
- Final validation: health, constraints, git status
- Ensure all changes are pushed
- Update active-tasks.md entry to validated status with complete verification notes

## Success Criteria

- All constraints satisfied (active-tasks ≤2KB, MEMORY.md ≤35 lines, git clean, health green, no temp files, no pending updates)
- Zero stale idea branches
- Zero temporary files
- active-tasks.md properly updated with this session's validation entry
- Planning documents (task_plan.md, findings.md, progress.md) created/updated and committed
- All changes pushed to origin
- Final health check green

## Risks & Mitigations

- **Risk:** active-tasks.md exceeds 2KB after adding new entry
  - **Mitigation:** Prune oldest completed entries before adding new validation entry
- **Risk:** Commit doesn't match validation criteria
  - **Mitigation:** Run `./quick validate-constraints` before committing and fix any issues
- **Risk:** Push fails due to remote conflicts
  - **Mitigation:** Pull first, resolve conflicts, then push
