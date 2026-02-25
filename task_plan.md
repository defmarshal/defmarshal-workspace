# Task Plan - Strategic Workspace Builder

**Session:** 2026-02-25 21:00 UTC  
**Session Key:** workspace-builder-23dad379-21ad-4f7a-8c68-528f98203a33  
**Trigger:** Cron (workspace-builder-cron)  
**Goal:** Analyze workspace and implement meaningful improvements while maintaining strict constraints

## Phase 1: Workspace Analysis (30 min)
- Read all memory files (today + yesterday) and MEMORY.md
- Check active-tasks.md for running agents
- Run comprehensive health check (`./quick health`)
- Analyze git status and recent commits
- Identify constraints violations or risks

## Phase 2: Identify Improvement Opportunities (20 min)
- Review past logs for recurring patterns
- Check for unused files/stale branches
- Evaluate active-tasks.md size trends
- Assess planning documentation quality
- Identify 1-2 meaningful, small-scope improvements

## Phase 3: Implement Changes (40 min)
- Create/modify files with surgical precision
- Update active-tasks.md with running entry
- Document each step in progress.md
- Commit changes incrementally with 'build:' prefix
- Push after each successful validation

## Phase 4: Close the Loop Validation (20 min)
- Run `./quick health` - ensure all constraints green
- Test any modified commands
- Verify active-tasks.md <2KB
- Verify MEMORY.md ~30 lines
- Confirm no temp files or untracked artifacts
- Ensure git clean and pushed

## Phase 5: Finalize and Report (10 min)
- Update active-tasks.md status to validated with verification metrics
- Commit final validation entry
- Push to origin
- Log completion in daily memory file

**Success Criteria:**
- All constraints (active-tasks.md size, MEMORY.md length, health checks) satisfied
- At least one meaningful improvement implemented
- Full traceability in planning docs
- Git clean and up-to-date

---

*Plan created: 2026-02-25 21:00 UTC*
