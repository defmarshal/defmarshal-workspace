# Workspace Builder Task Plan
**Started**: 2026-02-21 03:00 UTC  
**Goal**: Strategic improvements based on current workspace analysis

## Analysis Summary

**Current Branch**: `idea/generate-a-monthly-digest-of` (incomplete feature)
**System Health**: All green (disk 49%, memory clean, gateway healthy)
**Core Finding**: Idea generator produces low-value placeholder ideas; monthly digest attempt incomplete

## Identified Improvement Areas

1. **Idea System Quality** (Critical)
   - Ideas are generic templates with placeholder execution steps
   - Current execution: `touch quick`, `echo '...'`, `git commit` with vague messages
   - Produces noise commits without actual functionality
   - Need: Either enhance generator with concrete, valuable ideas or decommission it

2. **Monthly Digest Feature** (Incomplete)
   - Branch exists: `idea/generate-a-monthly-digest-of`
   - Last commit (247804d) added research file but no monthly digest implementation
   - Daily digest exists and works; monthly summary would be logical extension
   - Could complete the feature by adding `quick monthly-digest` command

3. **Documentation Gaps**
   - Idea system not documented in AGENTS.md or READMEs
   - No clear purpose/quality standards for generated ideas
   - No guidance on what makes a "good" idea

4. **Branch Hygiene**
   - Stale feature branch not merged; may clutter repo
   - Should either complete and merge, or delete

## Proposed Plan (3 Phases)

### Phase 1: Immediate Cleanup & Quality Gate
- Add quality validation to idea executor (require actual code changes, not just touch quick)
- Add pre-commit hook or validation step to reject placeholder commits
- Document minimum acceptance criteria for idea execution
- Clean up existing low-value commits (interactive rebase to squash/remove noise)

### Phase 2: Implement or Remove Monthly Digest Feature
- Option A (Implement): Create `quick monthly-digest` that aggregates monthly reports from daily digests
- Option B (Remove): Delete the incomplete branch; document that idea generator needs enhancement first
- Decision based on user preference; I'll implement Option A as it's useful

### Phase 3: Enhance Idea Generator (Long-term)
- Replace template-based random generation with:
  - Scan for actual TODO/FIXME comments and suggest fixes
  - Analyze unused/deprecated files and suggest removal
  - Identify missing quick utilities from common tasks
  - Look for stale locks/stale artifacts and propose cleanup
- Output: concrete PR-ready branches with actual changes (not just commit placeholders)
- Add quality metrics: must touch at least 2 real files (not just quick), must include tests/docs

## Success Criteria

- No more noise commits with generic "feat(idea):" messages lacking substance
- Idea system either produces valuable, implementable improvements or is paused
- Monthly digest feature (if implemented) works and generates useful reports
- All changes validated: `./quick health` clean, git clean, no temp files
- Active-tasks.md updated with verification notes

## Risks & Mitigations

- **Risk**: Idea generator enhancement may be complex
- **Mitigation**: Phase approach; can disable generator cron temporarily if needed
- **Risk**: Monthly digest implementation time
- **Mitigation**: Keep simple—use existing daily digest data, just aggregate by month

## Resources

- Existing daily digest infrastructure: `content/YYYY-MM-DD-daily-digest.md`, `reports/`
- Idea generator/executor scripts already in place
- Quick launcher pattern for adding utilities

---

**Status**: Planning complete • Ready to execute Phase 1 then Phase 2
