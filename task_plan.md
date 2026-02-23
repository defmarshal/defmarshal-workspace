# Workspace Builder Task Plan

**Session:** workspace-builder-20260223-2107
**Trigger:** Manual follow-up (noise reduction)
**Time:** 2026-02-23 21:07 UTC
**Goal:** Prevent .clawhub/lock.json from appearing as modified by ignoring lock files in .gitignore

---

## Analysis Summary

**Current State:**
- Health: OK ( Disk 67%, Gateway healthy, Memory clean, Git clean)
- active-tasks.md: 39 lines (<2KB) ✓
- MEMORY.md: 30 lines (≤30) ✓
- No stale branches ✓

**Issue Identified:**
- `.clawhub/lock.json` periodically shows as modified in git status
- It is a transient lock file and should not be tracked
- `.gitignore` currently lacks a pattern for `*.lock.json`

**Root Cause:** OpenClaw uses lock files for concurrency control; these are runtime artifacts, not source files.

---

## Task Phases

### Phase 1: Analysis & Planning
- Verify .clawhub contents: lock.json present, config.json exists and should be kept
- Determine safe ignore pattern: `*.lock.json` (covers all lock files)
- Edit .gitignore to add the pattern at the end

### Phase 2: Implementation
- Add `*.lock.json` to .gitignore
- Ensure file formatting is clean (no trailing spaces, newline at EOF)
- Stage .gitignore: `git add .gitignore`
- Commit with message: `build: ignore OpenClaw lock files (*.lock.json) to prevent noise`
- Push to origin

### Phase 3: Validation
- Run `./quick health` - expect OK
- Verify git status: clean
- Check no temp files exist
- Confirm .clawhub/config.json remains tracked (if exists)

### Phase 4: Documentation
- Update active-tasks.md: add entry for this session with verification notes
- Update planning files (task_plan.md, findings.md, progress.md) with completion status
- Append summary to memory/2026-02-23.md

---

## Success Criteria

- .gitignore updated with `*.lock.json`
- Commit pushed to origin
- Git working tree clean
- active-tasks.md updated and <2KB
- All validation checks pass

---

## Risk Mitigation

- **Risk:** Ignoring too broadly (e.g., all .json in .clawhub)
  - **Mitigation:** Use precise pattern `*.lock.json` to avoid ignoring config.json
- **Risk:** Breaking existing ignores
  - **Mitigation:** Append to file; no removals
