# Workspace Builder Plan — 2026-02-18 23:00 UTC

**Goal:** Restore system health, fix gateway token mismatch, validate system integrity, and commit pending changes.

**Session:** Cron-triggered agent run (workspace-builder)

---

## Phase 1: Assessment & Planning

- Run `quick health` to establish baseline
- Review cron job schedules against CRON_JOBS.md
- Check memory status (memory-dirty, memory-status)
- Inspect git status for uncommitted changes
- Identify critical issues requiring immediate action

**Deliverable:** Initial findings recorded; plan refined based on current state.

---

## Phase 2: Gateway Recovery

**Critical:** The gateway is experiencing a device token mismatch, causing RPC failures and leaving a stray process. This must be fixed to restore agent communication.

Steps:
- Execute `./gateway-fix.sh`
- Wait for service to start
- Verify:
  - `openclaw gateway status` shows healthy
  - Port 18789 listening
  - No stray gateway processes (except the systemd-managed one)
  - RPC connectivity OK

**Notes:** This script kills all gateway processes, removes identity tokens, restarts service, and waits for readiness. Should fully resolve mismatch.

---

## Phase 3: Maintenance Operations

After gateway health restored:
- Run `./agents/agent-manager.sh --once` to:
  - Clean up stale locks
  - Perform memory reindex check (defer if rate-limited)
  - Auto-commit any pending untracked files (e.g., content/INDEX.md) if under threshold
- Check `git status` to confirm working directory clean
- If still dirty, manually commit safe changes (e.g., INDEX.md) with appropriate message

---

## Phase 4: System Validation

Re-check system health and functionality:
- `quick health` (should be OK)
- `quick mem` (show recent memories)
- `quick search test` (verify search works)
- `./quick cron` (ensure schedules match docs)
- `active-tasks.md` size check (<2KB)
- `./quick memory-status` (main store clean)

**Success criteria:** All checks green, no errors.

---

## Phase 5: Documentation & Cleanup

- Update `active-tasks.md`:
  - Remove current running entry
  - Ensure "Completed (Feb 18)" section remains for historical runs
- Compose final report for `findings.md`
- Commit **all** changes (including task_plan.md, progress.md, findings.md, active-tasks.md updates) with prefix `build:`
- Push to `origin/master`

---

## Phase 6: Close the Loop

- Final health verification
- Ensure no temporary files left behind
- Confirm no orphaned processes
- Summarize outcomes in `findings.md`

---

**Notes:**
- All operations should respect existing automation (e.g., agent-manager auto-commit).
- Use minimal disruption; avoid unnecessary restarts.
- Keep log updates concise.
