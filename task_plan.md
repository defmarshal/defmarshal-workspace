# Workspace Builder Task Plan

**Session ID:** workspace-builder-20260228-0306  
**Trigger:** Cron (every 2 hours)  
**Start Time:** 2026-02-28 03:06 UTC  
**Goal:** Analyze workspace and implement meaningful improvements

---

## Phase 1: Assessment & Discovery

**Status:** ✅ Completed  
**Findings:**
- Git status: clean, all artifacts tracked
- active-tasks.md: 1685 bytes, 31 lines, contains 2 completed entries that can be archived
- MEMORY.md: 29 lines (healthy)
- Health: green (disk 73%, gateway healthy, no updates)
- Memory index: 4 days old (stale, should reindex)
- Stale branches: 2 idea branches (5h and 3h old) - recent from idea system, not stale
- Research reports: all tracked, INDEX.md up-to-date
- meta-supervisor-restart.sh script: tracked in git but not documented in TOOLS.md

---

## Phase 2: Improvement Implementation Steps

### Step 1: Prune active-tasks.md (Archive Completed Entries)
- **Why:** Keep active-tasks lean (<2KB), remove completed tasks per AGENTS.md guidelines
- **What:** Archive `workspace-builder-23dad379` (Feb 27) to memory/2026-02-28.md
- **What:** Remove validated entry `workspace-builder-20260228-0107` (current session should not archive itself)
- **Verify:** active-tasks size decreases, still <2KB

### Step 2: Trigger Memory Reindex
- **Why:** Memory index is 4 days old; freshness improves search performance
- **What:** Run `./quick memory-index` and monitor completion
- **Verify:** `quick memory-status` shows fresh index

### Step 3: Enhance validate-constraints with Branch Hygiene Check
- **Why:** Proactively detect stale idea branches (>7 days old) before they accumulate
- **What:** Add branch age check to `scripts/validate-constraints.sh` or create new check
- **Verify:** Running validate-constraints shows branch hygiene status

### Step 4: Document meta-supervisor-restart.sh in TOOLS.md
- **Why:** Utility script should be documented for easy reference
- **What:** Add "Meta Supervisor Restart" section with usage in TOOLS.md
- **Verify:** TOOLS.md updated with script reference

### Step 5: Close-the-Loop Validation
- **Run:** `./quick validate-constraints` - all constraints green
- **Check:** No temp files left behind
- **Check:** Git status clean (only planned changes)
- **Check:** active-tasks.md size <2KB
- **Check:** Memory index fresh
- **Check:** No unintended side effects

### Step 6: Commit & Push
- **Commit Prefix:** `build:`
- **Message:** Summarize improvements implemented
- **Push:** To origin/master

### Step 7: Update active-tasks.md
- **Mark:** This session as `validated`
- **Add:** Verification notes
- **Size Check:** Ensure <2KB

---

## Risk Mitigation

- **Backup:** Daily log already contains prior state; edits are additive
- **Rollback:** Git allows revert if any step causes issues
- **Validation:** Each step verified before proceeding
- **Error Handling:** If step fails, debug and fix before continuing; log errors in progress.md

---

## Success Criteria

✅ active-tasks.md pruned and archived  
✅ Memory reindex completed  
✅ Branch hygiene check added (or documented)  
✅ TOOLS.md updated with restart script reference  
✅ All constraints pass validation  
✅ Changes committed with `build:` prefix and pushed  
✅ active-tasks.md updated with this session validated  
✅ No temp files, no broken state

---

## Notes

- Keep changes small but meaningful
- Follow "close the loop" discipline: validate before commit
- Update progress.md after each step with outcomes
- If validation fails, fix issues before proceeding
