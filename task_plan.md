# WorkspaceBuilder Plan: Memory System Enhancements

** Started**: 2026-02-15 07:00 UTC (UTC+7: 14:00)
**Timezone**: Asia/Bangkok (UTC+7)
**Current commit**: (clean working tree)
**Goal**: Enhance memory system usability with better visibility and management tools while keeping changes small and meaningful.

## Phases

### Phase 1: Analyze Current State & Define Scope
- [x] Read active-tasks.md, MEMORY.md, quick launcher, web-dashboard.py
- [x] Check memory status (openclaw memory status)
- [x] List memory files and recent daily logs
- [x] Review git status and recent commits
- **Status**: complete

### Phase 2: Design Enhancements
- [ ] Identify gaps in memory visibility/management
- [ ] Select 2-3 small but meaningful improvements
- [ ] Document design in findings.md
- **Status**: pending

### Phase 3: Implement Enhancements
- [ ] Enhance web dashboard memory card with stats (indexed count, last indexed)
- [ ] Add `quick memory-stats` command showing memory usage, file count, chunk count, last indexed time
- [ ] Optionally add `quick memory-prune` dry-run to show old memories that could be removed (respect 100/7 limit)
- **Status**: pending

### Phase 4: Test & Validate
- [ ] Run `quick memory-stats` and verify output
- [ ] Start web-dashboard.py and verify memory card shows stats
- [ ] Run `quick health` to ensure system health
- [ ] Check `git status` - all changes should be clean
- [ ] Verify no temporary files left behind
- **Status**: pending

### Phase 5: Commit & Push
- [ ] Commit changes with prefix `build: memory system enhancements`
- [ ] Push to GitHub (defmarshal/defmarshal-workspace)
- [ ] Update active-tasks.md with verification results
- **Status**: pending

## Decisions

- Keep scope small (max 3 new features)
- Leverage existing `openclaw memory status` output for stats
- Make all changes backward-compatible (no breaking changes to existing commands)
- Follow pattern: display stats in terminal + (where relevant) enhance web dashboard

## Constraints

- Respect quiet hours (23:00-08:00 UTC+7) - currently safe (14:00)
- Memory system uses Voyage AI free tier (3 RPM) - avoid heavy reindexing
- All changes must be validated before commit
- Update active-tasks.md with verification notes

## Success Criteria

- `quick memory-stats` shows useful information (files, chunks, last indexed, dirty status)
- Web dashboard memory card displays stats (not just recent snippets)
- `git status` clean, no leftover temp files
- Changes committed and pushed
- active-tasks.md updated with validation results
