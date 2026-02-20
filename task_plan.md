# Workspace Builder Plan: Meta-Supervisor Improvements & Hygiene

**Session Key:** 23dad379-21ad-4f7a-8c68-528f98203a33
**Started:** 2026-02-20 11:00 UTC
**Goal:** Commit meta-supervisor enhancements; remove temp artifacts; apply pending updates; validate system; update active-tasks.

---

## Phase 1: Assessment & Planning

**Actions:**
- Read SOUL.md, USER.md, MEMORY.md (context already loaded)
- Check active-tasks.md → currently empty running entries
- Run health checks: `quick health`, `quick memory-status`, `quick agent-status`
- Inspect workspace: git status shows modified meta-supervisor-cycle.sh, untracked temp files

**Findings:**
- System health: OK (Disk 44%, Gateway healthy, Memory 18f/77c clean local FTS+, Git dirty)
- Modified: `agents/meta-supervisor/meta-supervisor-cycle.sh` (improved Agni/Rudra check with 2h grace, fixed daily digest path, added debug)
- Untracked temp files: `agents/meta-supervisor/.meta-supervisor.pid`, `agents/meta-supervisor/meta-supervisor.nohup` (should be removed)
- Pending APT updates: 3 (optional but recommended for security)
- No other uncommitted changes
- active-tasks.md has no current running entry; we should add one to avoid conflicts.

**Plan:**
- Add running task entry to active-tasks.md
- Remove temp artifacts
- Optionally apply pending APT updates
- Stage and commit meta-supervisor improvements
- Write fresh planning docs (task_plan.md, findings.md, progress.md) for this run
- Run validation checks (syntax, health, git status, temp file check)
- Push commit with `build:` prefix
- Update active-tasks.md to validated with verification notes
- Final health check

---

## Phase 2: Implementation Steps

### Step 1: Register running task
Edit `active-tasks.md`: add entry under "Currently Running" with session key, agent name "workspace-builder", goal summary, start time, status "running".

### Step 2: Cleanup temp files
Remove: `agents/meta-supervisor/.meta-supervisor.pid` and `agents/meta-supervisor/meta-supervisor.nohup`.

### Step 3: Apply system updates (optional)
Run `./quick updates-apply --execute` to apply pending APT updates and improve system health.

### Step 4: Validate meta-supervisor syntax
Run `bash -n agents/meta-supervisor/meta-supervisor-cycle.sh` to ensure no syntax errors.

### Step 5: Write planning documents
- Overwrite `task_plan.md` (this file)
- Create `findings.md` with current assessment
- Create `progress.md` with initial log entry

### Step 6: Stage changes
- Stage modified: `agents/meta-supervisor/meta-supervisor-cycle.sh`
- Stage updated: `active-tasks.md`
- Stage new: `task_plan.md`, `findings.md`, `progress.md`

### Step 7: Commit and push
Commit with message: `build: meta-supervisor enhancements; clean temp files; apply updates`
Push to origin.

### Step 8: Close the loop
- Update `active-tasks.md`: move our entry to "Recently Completed", set status "validated", add verification notes (commands/outputs)
- Run final `./quick health` to confirm post-commit state

---

## Phase 3: Success Criteria

- meta-supervisor improvements versioned and pushed
- Temp artifacts removed
- active-tasks.md accurately reflects this run (size <2KB)
- All health checks pass (Disk, Gateway, Memory, Git clean, Updates 0)
- No leftover uncommitted changes
- Planning docs reflect this session

---

## Notes

- The meta-supervisor-cycle.sh changes are backward-compatible and improve robustness.
- The daily digest check now correctly points to `reports/` (previous check used `content/` erroneously).
- Agni/Rudra check now allows 2-hour grace period, reducing false alerts.
- Debug print added; acceptable for now.
