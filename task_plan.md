# Workspace Builder - Task Plan

**Session:** workspace-builder (cron)
**Date:** 2026-02-21 21:00 UTC
**Goal:** Strategic workspace improvements and hygiene

---

## Phase 1: Assessment & Planning

### Analysis
- Read SOUL.md, USER.md, MEMORY.md, active-tasks.md, recent daily logs
- Check git status, branch hygiene, temp files
- Run health checks (`./quick health`)
- Identify actionable improvements

### Findings
- active-tasks.md: Contains 2 validated entries that should be archived (size OK but should not accumulate indefinitely)
- Temp files: CRON_JOBS.md.bak present (13092 bytes) - should be removed
- Git branches: One stale/incomplete branch: `idea/create-a-health-check-for`
- Idea pipeline: Recent implementation, documentation may need enhancement
- System health: All OK (Disk 54%, Gateway healthy, Memory clean)

---

## Phase 2: Execution Plan

### Task 1: Archive Completed Active Tasks
- Move the 2 validated entries from `active-tasks.md` to `memory/2026-02-21.md`
- Keep only "Currently Running" section (empty) and maybe very recent (last 1-2) if needed
- Ensure file stays <2KB

### Task 2: Cleanup Temporary Files
- Remove `CRON_JOBS.md.bak`
- Verify no other temp files (`.tmp`, `.temp`, `.swp`, etc.)

### Task 3: Git Branch Hygiene
- Delete stale branch `idea/create-a-health-check-for`
- Verify branch deletion pushed to origin
- Ensure no other stale branches

### Task 4: Enhance Idea Pipeline Documentation
- Check if `agents/ideas/README.md` exists and is adequate
- If missing or sparse, create comprehensive README covering:
  - Purpose of generator/executor
  - How to monitor status (`quick ideas-status`)
  - How to manually trigger
  - Log locations
  - Validation rules (what makes an idea valid)
- Update `TOOLS.md` or `docs/` if appropriate

### Task 5: Validation & Testing
- Run `./quick health` - must pass
- Test `quick ideas-status` command if available
- Check `git status` - must be clean
- Check active-tasks.md size (<2KB)
- Verify no temp files remain
- Check memory status

### Task 6: Commit & Push
- Commit all changes with prefix `build:`
- Push to origin
- Update active-tasks.md with this session's entry (after committing, mark validated)
- Include verification notes

---

## Phase 3: Close the Loop

After commit:
- Run final health check
- Confirm all validations passed
- Ensure git working tree clean
- No leftover temp files

---

## Success Criteria

✅ All tasks completed and validated  
✅ No temp files remain  
✅ Git clean, branches tidy  
✅ active-tasks.md pruned and <2KB  
✅ Health checks pass  
✅ Changes committed and pushed
