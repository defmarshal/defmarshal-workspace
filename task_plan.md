# Workspace Builder Plan — 2026-02-19 01:00 UTC

**Goal:** Resolve gateway RPC token mismatch, commit pending meta-agent/supervisor improvements, validate system health, and push changes.

**Session:** Cron-triggered agent run (workspace-builder)

---

## Phase 1: Assessment & Context

- Confirm gateway RPC status (expected: unauthorized)
- Check git status (uncommitted meta-agent.sh, supervisor.sh)
- Review active-tasks.md (should show this builder running)
- Verify memory status (main store clean)
- Quick health baseline

**Deliverable:** Initial findings recorded.

---

## Phase 2: Gateway Recovery

**Critical:** Gateway RPC is failing with `device token mismatch`. A stray process is listening on port 18789 while systemd service is dead.

Steps:
- Execute `./gateway-fix.sh`
- Wait for service to start and RPC to become ready
- Verify:
  - `openclaw gateway status` shows healthy
  - `./quick health` shows Gateway: healthy
  - No stray processes; port 18789 owned by systemd service

**Notes:** This script kills all gateway processes, removes identity/device-auth.json, restarts service, and waits for RPC readiness.

---

## Phase 3: Commit Pending Changes

After gateway health restored:
- Review uncommitted changes (meta-agent.sh: cron payload fix; supervisor.sh: PATH export)
- Stage and commit with prefix `build:` (or more specific: `fix(meta-agent): use --message instead of --system-event for cron jobs` and `fix(supervisor): ensure PATH includes npm global bin`)
- Push to origin/master

---

## Phase 4: System Validation

Re-check system health and functionality:
- `./quick health` (all OK)
- `./quick mem` (show recent memories)
- `./quick search test` (verify search works)
- `./quick cron-status` (ensure schedules still match docs)
- `active-tasks.md` size check (<2KB)
- `./quick memory-status` (main store clean)
- `./quick memory-dirty` (check other stores)

**Success criteria:** All checks green, no errors.

---

## Phase 5: Documentation & Cleanup

- Update `active-tasks.md`:
  - Change status from `running` to `validated`
  - Add verification notes
- Optionally update `findings.md` with summary of this session (can also be separate)
- Ensure all files properly committed (including any modified docs)
- Verify no temp files left behind

---

## Phase 6: Close the Loop

- Final health verification
- Confirm no orphaned processes
- All changes pushed
- Session complete

---

## Risk Mitigation

- Gateway fix may require multiple attempts if token rotation fails; script includes retries via loops.
- If commit fails due to remote issues, retry once; if still failing, log and leave for next agent-manager auto-commit.
- Keep changes minimal: only meta-agent.sh, supervisor.sh, active-tasks.md, and this planning set.

---

**Dependencies:** None beyond existing scripts.
