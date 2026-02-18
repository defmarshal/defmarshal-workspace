# Workspace Builder Plan

**Started**: 2026-02-18 21:00 UTC
**Session**: agent:main:cron:23dad379-21ad-4f7a-8c68-528f98203a33
**Goal**: Strategic improvements: system updates, active-tasks hygiene, gateway verification, validation

---

## Phase 1: Analysis & Preparation

**Tasks**:
1.1 Check git status and modified files
1.2 Review active-tasks.md for stale entries
1.3 Check gateway token status
1.4 Assess system update needs
1.5 Verify memory system health

**Status**: ✅ Complete

**Findings**:
- Git dirty: `memory/2026-02-18.md` modified (daily log updates)
- Active-tasks.md is clean (no stale entries after Feb 18 cleanup)
- Gateway token mismatch still present (from Feb 18)
- 16 APT updates pending (mostly GCC-13 security/updates)
- Memory system: main store clean, reindex not needed

---

## Phase 2: System Updates

**Tasks**:
2.1 Run `./quick updates-apply --dry-run` to preview
2.2 Apply updates with `--execute` if safe
2.3 Verify system health post-update

**Rationale**: Security/bug fixes; maintains system integrity. All updates are from `noble-updates` (official Ubuntu security/updates pocket), low risk.

**Status**: ⏳ Pending

---

## Phase 3: Gateway Token Resolution

**Tasks**:
3.1 Check if gateway RPC is currently functional
3.2 If token mismatch exists, run `./gateway-fix.sh`
3.3 Verify gateway status and RPC connectivity
3.4 Document resolution in active-tasks.md

**Rationale**: Gateway token mismatch prevents RPC connections, breaking agents that rely on gateway API (supervisor notifications, agent-spawn, etc.). Must be fixed for full autonomy.

**Status**: ⏳ Pending

---

## Phase 4: Git Hygiene & Commit

**Tasks**:
4.1 Stage `memory/2026-02-18.md` changes
4.2 Optionally include any other uncommitted files
4.3 Commit with message: `build: system updates; verify memory reindex; agent-status; validation`
4.4 Push to origin/master
4.5 Confirm clean git status

**Status**: ⏳ Pending

---

## Phase 5: Active-Tasks Maintenance

**Tasks**:
5.1 Review active-tasks.md entries from Feb 18
5.2 Archive completed workspace-builder records (keep only active)
5.3 Add new validated record for this session
5.4 Ensure file size < 2KB

**Status**: ⏳ Pending

---

## Phase 6: Final Validation

**Tasks**:
6.1 Run `./quick health` — expect all OK
6.2 Test `./quick mem` and `./quick search test` — confirm memory functional
6.3 Run `./quick agent-status` — verify all cron jobs healthy
6.4 Run `./quick validate` — comprehensive check
6.5 Check for temp files (clean)
6.6 Verify no orphaned agents (sessions list)
6.7 Confirm active-tasks.md accurate

**Status**: ⏳ Pending

---

## Phase 7: Close the Loop

**Tasks**:
7.1 Update active-tasks.md with verification results
7.2 Mark this session as validated
7.3 Final push if any post-commit changes
7.4 Clear workspace (no temp files, logs rotated)

**Status**: ⏳ Pending

---

## Notes

- Keep changes small but meaningful
- Do not modify cron schedules (already validated on Feb 18)
- No Voyage reindex needed (main store clean, last reindex 2.2d ago)
- Respect existing system design; focus on hygiene and stability
