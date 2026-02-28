# Workspace Builder Task Plan

**Session ID:** workspace-builder-20260228-0510
**Trigger:** Cron (every 2 hours)
**Start Time:** 2026-02-28 05:10 UTC
**Goal:** Strategic maintenance - archive old active-tasks, update documentation, enforce constraint hygiene, close the loop

---

## Phase 1: Assessment & Discovery

**Status:** ✅ Completed (during initial analysis)
**Findings:**
- System health: green (disk 72%, gateway healthy, no updates)
- Git status: clean, no untracked files
- active-tasks.md: 1697 bytes (<2KB), contains two validated entries from today (01:07 and 03:06) plus running meta-supervisor-daemon
- MEMORY.md: 29 lines (≤35)
- Memory index: dirty=false, last reindex log 4 days old → warning but acceptable (no dirty files)
- Branch hygiene: one idea branch fresh (<1 day) → no stale branches
- Documentation gaps:
  1. CRON_JOBS.md lists 4 cron jobs that are currently disabled (supervisor-cron, linkedin-pa-agent-cron, meta-supervisor-agent, daily-digest-cron) → mismatch with actual state
  2. TOOLS.md lacks documentation for ClawDash backend (port 3001, PM2 service name)
- Constraint validation: 6/7 green, 1 warning (reindex age) → acceptable

---

## Phase 2: Improvement Implementation Steps

### Step 1: Archive Oldest Validated active-tasks Entry
- **Why:** Follow AGENTS.md: "Remove completed tasks after verification" to keep active-tasks lean (<2KB) and maintainable.
- **What:** Archive `workspace-builder-20260228-0107` (oldest validated) to `memory/2026-02-28.md` under "Archived Completed Tasks". Remove it from active-tasks Running section. Keep `workspace-builder-20260228-0306` and meta-supervisor-daemon.
- **Verify:** active-tasks size decreases, still <2KB; daily log updated.

### Step 2: Update CRON_JOBS.md for Disabled Jobs
- **Why:** Documentation must reflect actual operational state. Four cron jobs are disabled for token conservation per user request, but docs still list them as active → confusion and potential auto-re-enable via schedule validator.
- **What:**
  - Create new section: "## Inactive Cron Jobs" at the end of file.
  - Move entries for: supervisor-cron, linkedin-pa-agent-cron, meta-supervisor-agent, daily-digest-cron to that section.
  - For each, list original schedule and note: *"Status: Disabled (token conservation, user request, 2026-02-28). Can be re-enabled with `openclaw cron enable <id>`."*
  - Ensure the active cron section still has accurate sequential numbering (1-27 remain unchanged). Inactive section uses bullet list without numbers.
- **Verify:** CRON_JOBS.md syntax valid, clear distinction between active/inactive.

### Step 3: Document ClawDash Backend in TOOLS.md
- **Why:** The ClawDash project includes a Node.js backend running on port 3001 (PM2: `clawdash-backend`). This is not documented in TOOLS.md, making it harder to manage.
- **What:**
  - Add new subsection under "Daemon Management" or new "Dashboard" section.
  - Document:
    - Backend port: 3001
    - PM2 process name: `clawdash-backend`
    - Quick commands to manage: `pm2 restart clawdash-backend`, `pm2 logs clawdash-backend`
    - Reference: `dash` and `dashboard` quick commands interact with the system.
  - Keep formatting consistent.
- **Verify:** TOOLS.md updated, readable, accurate.

### Step 4: Validation (Pre-commit)
- **Run:** `./quick validate-constraints`
- **Check:** All 7 constraints satisfied (active-tasks <2KB, MEMORY.md ≤35, health green, git clean, no temp files, APT none, branch hygiene)
- **Note:** Memory reindex age warning persists but OK since index not dirty.
- **If fails:** debug and fix before proceeding.

### Step 5: Commit & Push
- **Commit Prefix:** `build:`
- **Message:** Summarize implemented improvements.
- **Actions:**
  ```bash
  git add -A
  git commit -m "build: archive old active-tasks entry, mark disabled cron jobs in docs, document ClawDash backend"
  git push origin master
  ```
- **Verify:** Push succeeds, remote up-to-date.

### Step 6: Update active-tasks.md
- **Add:** Running entry for this session with comprehensive verification notes.
- **Prune:** If total size >2KB after addition, archive oldest completed entry (likely `workspace-builder-20260228-0306`) to daily log before adding new entry (or after commit, ensure final size <2KB).
- **Commit & Push:**
  ```bash
  git add active-tasks.md
  git commit -m "build: mark workspace-builder session 20260228-0510 validated - all constraints satisfied"
  git push origin master
  ```
- **Verify:** active-tasks size <2KB, entry present, remote synced.

### Step 7: Final Validation & Closure
- Re-run `./quick health` and `./quick validate-constraints` to confirm final state green.
- Check for leftover temp files: `git status` should show only tracked files.
- Ensure daily log (memory/2026-02-28.md) is up-to-date with archive entry.

---

## Risk Mitigation

- **Archiving:** Only removing validated entries; daily log preserves history.
- **Doc updates:** Non-destructive; moving cron entries to "Inactive" retains information without affecting operation.
- **Validation:** Each step verified; if any fails, halt and resolve before next.
- **Rollback:** All changes are tracked in git; can revert if needed.

---

## Success Criteria

✅ active-tasks.md pruned, only running tasks remain, size <2KB
✅ CRON_JOBS.md accurately reflects current cron job status (inactive ones marked)
✅ TOOLS.md includes ClawDash backend documentation
✅ All constraints pass validation
✅ Changes committed with proper prefix and pushed
✅ active-tasks.md updated with this session validated
✅ No temp files, no broken state
✅ Daily log updated with archived task

---

## Notes

- Keep changes small, focused, and well-documented.
- Follow "close the loop": validate before committing, update active-tasks after validation.
- Respect token conservation: avoid unnecessary LLM calls; this run uses minimal reasoning.
