# Workspace Builder Session Plan

**Started:** 2026-02-23 05:00 UTC
**Trigger:** Cron (workspace-builder-cron)
**Goal:** Strategic workspace analysis and meaningful improvements

## Analysis Phases

### Phase 1: Health & Hygiene Audit
- Check git status, uncommitted changes, untracked files
- Verify active-tasks.md size (<2KB) and format
- Check MEMORY.md currency (last updated, line count)
- Inspect memory index health (Voyage/local status)
- Review disk usage and temp files
- Validate .gitignore completeness

### Phase 2: Documentation Quality
- Review CRON_JOBS.md accuracy vs actual schedules
- Check AGENTS.md for outdated info
- Verify TOOLS.md local notes are current
- Ensure planning files (task_plan.md, findings.md, progress.md) follow protocol

### Phase 3: System Optimization
- Look for redundant/duplicate skills (per 2026-02-21 cleanup)
- Identify quick command improvements (quick launcher)
- Check log rotation effectiveness
- Review idea pipeline health (generator/executor status)
- Test memory search fallback (msearch)

### Phase 4: Proactive Maintenance
- Prune stale feature branches (idea/*)
- Archive old memory files if needed
- Update MEMORY.md with recent learnings (if needed)
- Validate cron schedule integrity

### Phase 5: Validation & Handover
- Run `quick health` and verify all OK
- Test modified quick commands
- Check that no temp files remain
- Ensure git clean before commit
- Update active-tasks.md with validated entry
- Commit with `build:` prefix and push

## Success Criteria

- All health metrics pass
- At least one meaningful improvement implemented
- No stale branches or temp files
- Documentation accurate
- active-tasks.md under 2KB
- MEMORY.md <= ~30 lines
- All changes committed and pushed

## Risks & Mitigations

- **Risk:** Running into locked files from other agents
  - **Mitigation:** Check active-tasks.md first; skip if other agents running; proceed with read-only analysis if needed

- **Risk:** Making changes that break automated systems
  - **Mitigation:** Validate each change with tests; use dry-run where available; keep changes small and reversible

- **Risk:** Idea executor running concurrently and creating conflicts
  - **Mitigation:** Check git status frequently; if conflict arises, resolve gracefully and document
