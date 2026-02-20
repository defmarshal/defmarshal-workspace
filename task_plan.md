# Workspace Builder Task Plan

**Session ID:** workspace-builder-20260220-2300  
**Start Time:** 2026-02-20 23:00 UTC  
**Goal:** Fix idea generator/executor pipeline and clean up git tracking

---

## Phase 1: Assessment & Planning

**Status:** In Progress

### Tasks
1.1 Analyze current state (git status, logs, cron, scripts)  
1.2 Identify blocking issues (JSON invalid, untracked files)  
1.3 Document findings in `findings.md`  
1.4 Define success criteria

**Success Criteria:**
- Idea generator produces valid JSON (jq-parsable)
- Idea executor can read and update latest.json without errors
- Generated idea files are gitignored
- All changes committed with `build:` prefix
- active-tasks.md updated with validation

---

## Phase 2: Implementation - Core Fixes

**Status:** Pending

### Task 2.1: Fix idea-generator-cycle.sh JSON generation
- Replace manual JSON building with jq-based construction
- Ensure proper escaping of all string fields
- Keep existing functionality intact
- Test: generator output must be valid JSON

### Task 2.2: Update .gitignore
- Add `agents/ideas/*.json` to ignore generated idea artifacts
- Also ignore any executor logs in that dir if any

### Task 2.3: Commit and validate
- Run generator manually to produce new valid JSON
- Run executor manually to process an idea
- Verify logs and status files
- Clean up old broken JSON files (remove from git tracking, keep disk or remove)
- Commit changes with proper messages

---

## Phase 3: Validation & Documentation

**Status:** Pending

- Run `./quick health` and ensure all OK
- Verify no leftover temp files
- Check active-tasks.md size <2KB
- Ensure changes are pushed to origin
- Update memory files as needed

---

## Notes
- The cron jobs (idea-generator-cron, idea-executor-cron) already exist and are scheduled.
- jq is available on system.
- The generator script has 755 permissions; preserve.
