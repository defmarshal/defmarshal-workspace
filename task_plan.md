# Workspace Builder - Task Plan
**Session ID:** workspace-builder-20260225-0705  
**Started:** 2026-02-25 07:05 UTC  
**Goal:** Strategic maintenance: apply updates, cleanup stale branches, enforce constraints, and validate repository health

## Phases

### Phase 1: Analysis
- Check system health (./quick health)
- Check git status and untracked files
- Count active-tasks.md size (must be <2KB)
- Verify MEMORY.md line count (~30 lines)
- Identify stale idea branches
- Check pending APT updates
- Check memory reindex status

**Acceptance:** Complete when baseline metrics documented in findings.md

### Phase 2: Maintenance Actions
- Apply pending APT security updates (3 packages)
- Delete stale idea branches (`idea/add-dark-mode-toggle-to`, `idea/create-quick-command-to-find`)
- Prune active-tasks.md by removing oldest validated entries to stay <2KB
- Run memory reindex check (if needed)
- Update MEMORY.md if critical changes occurred

**Acceptance:** All actions completed without errors; git status clean

### Phase 3: Validation & Documentation
- Run comprehensive health check (./quick health)
- Verify all constraints: active-tasks < 2KB, MEMORY.md ~30 lines, no stale branches, no temp files
- Update progress.md with detailed log of actions
- Update active-tasks.md with this session's validation entry
- Commit changes with prefix 'build:'
- Push commits to origin

**Acceptance:** All validation checks pass; git clean; pushes successful

### Phase 4: Close the Loop
- Re-run health check to confirm final state
- Verify no untracked files remain
- Confirm no temp files in workspace
- Document final metrics in progress.md

**Acceptance:** System fully validated and stable

## Error Handling
- If any command fails, log error in progress.md and halt before proceeding to next phase
- Debug and retry failed steps before continuing
- If validation fails, iterate until all constraints satisfied

## Notes
- Keep changes small but meaningful
- Follow commit message format: `build: <description>`
- Respect active-tasks.md size constraint strictly (max 2048 bytes)
