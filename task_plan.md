# Task Plan: Workspace Builder Session (2026-02-26 03:05 UTC)

## Mission
Analyze workspace, implement meaningful improvements, validate constraints, and maintain system health.

## Current State Assessment
- ✅ System healthy: disk 70%, gateway operational, memory clean
- ✅ Git clean, remote up-to-date
- ✅ active-tasks.md: 1866b (<2KB)
- ✅ MEMORY.md: 30 lines (target ≤30)
- ✅ No pending APT updates, no stale branches
- ⚠️ Memory reindex: 2.1d ago (mild concern, monitor)
- ✅ All constraints satisfied

## Strategic Focus
Since system is stable, focus on:
1. **Maintenance automation**: Enhance validate-constraints integration into cron workflow
2. **Documentation improvements**: Review and update planning docs structure based on recent runner experiences
3. **Quick command completeness**: Audit quick launcher for missing but useful utilities
4. **Memory hygiene**: Monitor MEMORY.md for timely trimming (already good, but establish clearer guidelines)

## Implementation Steps

### Phase 1: Planning Documentation Setup
- Create `task_plan.md` (this file)
- Create `findings.md` for analysis
- Create `progress.md` for execution tracking
- Commit initial planning setup (if needed)

### Phase 2: System Analysis & Improvement Identification
- Run `./quick validate-constraints` to verify current state
- Check for any stale idea branches that might have appeared since last cleanup
- Review active-tasks.md for any orphaned entries or size optimization opportunities
- Audit quick launcher commands for usefulness and completeness
- Check daily logs for any patterns or recurring issues

### Phase 3: Implement Enhancements
Based on findings, perform up to 2-3 targeted improvements:
- Possible additions:
  - Update `quick validate-constraints` to include memory reindex age check (warning if >3d)
  - Add quick command `quick show-validation-checks` to display what validate-constraints monitors
  - Enhance planning docs with troubleshooting section based on common bugs encountered
  - Add constraint check for pending GitHub commits (should be zero)
  - Improve active-tasks.md pruning logic documentation

### Phase 4: Close the Loop Validation
- Run `./quick health`
- Run `./quick validate-constraints`
- Verify `git status` clean
- Check no temp files generated
- Confirm active-tasks.md <2KB and MEMORY.md ≤30 lines
- Ensure no stale branches

### Phase 5: Commit & Push
- Commit all changes with `build:` prefix
- Push to origin
- Update active-tasks.md with validation entry (session key: workspace-builder-YYYYMMDD-HHMM)
- Prune old entries to maintain <2KB after addition

## Success Criteria
- System health remains green
- All constraints pass
- Changes are meaningful but minimal (≤5 files modified, small diff)
- Documentation updated where needed
- active-tasks.md updated with proper verification metrics

## Risk Mitigation
- If no improvements found, simply validate and document "no action required" with reasoning
- Avoid over-engineering; keep changes small and practical
- Follow the "Text > Brain" principle: log all decisions in progress.md and findings.md

## Troubleshooting Patterns (Lessons Learned)
Based on recent workspace-builder iterations, document common pitfalls:

### 1. Git Status Parsing in validate-constraints
- **Issue**: Using `git status --short` vs `./quick git-status` may behave differently if quick wrapper adds formatting.
- **Solution**: Call `./quick git-status` (which may just alias to git status --porcelain?) But ensure consistent behavior. Validate script should use `git status --porcelain --untracked-files=all` directly to avoid alias differences.

### 2. Health Summary Parsing
- **Issue**: `./quick health` output format changes can break grep patterns.
- **Solution**: Use precise JSON from internal health check if available; otherwise use robust regex. Current script expects "Updates.*none", "clean", "Gateway.*healthy". Keep patterns in sync with health output.

### 3. active-tasks.md Size Management
- **Issue**: Adding a validation entry pushes size over 2KB; need to prune BEFORE adding.
- **Solution**: Prune oldest completed entries first, then add new entry, then verify final size. Use `wc -c` to measure bytes, not lines. Target <2000 bytes.

### 4. MEMORY.md Line Limit
- **Issue**: Target is 30 lines for curated content, but constraint allows ≤35 as buffer. Manual trimming needed to avoid losing important learnings.
- **Solution**: During heartbeat or workspace-builder runs, review MEMORY.md for outdated entries and remove oldest learnings to maintain ≤30 lines. Document trimming decisions in daily log.

### 5. Memory Reindex Age
- **Issue**: Reindex log may not exist if reindex never ran or log rotated.
- **Solution**: Check existence of `memory/memory-reindex.log`. If missing, show warning but don't fail (constraint remains warning). The age threshold is: ≤3d fresh, 4-7d stale (warning), >7d very stale (error).

### 6. APT Updates Parsing
- **Issue**: `./quick updates-check` output varies (e.g., "No pending updates" vs "0 packages").
- **Solution**: Support both patterns; if parsing fails, show warning but don't fail (constraint is best-effort).

### 7. Commit Message Hygiene
- **Issue**: Accidentally committing temporary files or sensitive data.
- **Solution**: Use `./quick validate-constraints` before committing; it catches temp files and untracked files. Also run `git status --short` to review staged changes.

### 8. active-tasks.md Entry Format
- **Issue**: Inconsistent formatting makes parsing and pruning error-prone.
- **Solution**: Strictly follow the format:
```
- [session-key] agent-name - goal (started: YYYY-MM-DD HH:MM UTC, status: running/validated/failed)
  - Verification: <output or metrics>
```
Keep verification text concise (one line if possible) to save bytes.

### 9. QUICK Launcher Sync
- **Issue**: Adding new commands requires updating both help text and case statement; easy to forget one.
- **Solution**: Add both in same edit or immediately verify by running `quick help | grep -A2 <command>`. Maintain a checklist in this section.

### 10. Feature Validation Before Commit
- **Issue**: Implemented feature but forgot to test in validation loop.
- **Solution**: Use the Close the Loop checklist strictly: health, constraints, git clean, no temp files, then commit. Document test results in progress.md before committing.

---
Keep this section updated as new patterns emerge.