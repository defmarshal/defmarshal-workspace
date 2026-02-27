# Task Plan — Workspace Builder (23dad379)

**Session**: 2026-02-27 11:12 UTC  
**Goal**: Enforce constraints, commit pending changes, clean stale branches, validate health, push to origin.

---

## Phase 1 — Assessment (Context Gathering)

- [x] Read SOUL.md, USER.md, active-tasks.md, MEMORY.md
- [x] Read daily logs: 2026-02-27, 2026-02-26
- [x] Run `quick health` and `quick validate-constraints`
- [x] Check git status and identify modified files
- [x] List stale idea branches

**Status**: ✅ Complete

**Findings**:
- 2 modified files: `apps/research-hub/INDEX.md` (major restructuring), `memory/heartbeat-state.json` (routine update)
- 1 stale idea branch: `idea/add-a-new-quick-utility`
- Constraints fail: Git dirty (expected — needs commit)
- active-tasks.md: 1695 bytes (healthy)
- MEMORY.md: 31 lines (within ≤35 limit, target ≤30 for optimal)
- Memory reindex age: 3.4d (fresh)
- All other constraints green

---

## Phase 2 — Execution (Fix & Publish)

### Step 1: Commit pending changes
**Task**: Stage and commit the 2 modified files with appropriate messages.
**Detail**:
- `apps/research-hub/INDEX.md`: restructured index with full descriptive headlines (substantive improvement)
- `memory/heartbeat-state.json`: timestamp, disk usage, weather status update (routine)
- Commit message: `build: refresh research-hub index with enhanced metadata + heartbeat-state update (workspace-builder 20260227)`
- Push to origin/master

**Verification**:
- `git status` should show clean after commit
- `git log -1` shows new commit with correct message
- `git push` succeeds

### Step 2: Cleanup stale idea branch
**Task**: Delete local branch `idea/add-a-new-quick-utility` (confirmed stale from logs)
- Command: `git branch -D idea/add-a-new-quick-utility`
- Verify no other `idea/*` branches remain

**Verification**:
- `git branch | grep 'idea/'` shows nothing

### Step 3: Update active-tasks.md
**Task**: Mark current session as validated, prune oldest entry to keep <2KB.
- Add validated entry for session `workspace-builder-23dad379`
- Include verification metrics (size, constraints status, git clean)
- Remove oldest completed entry (likely `workspace-builder-20260227-0921`) to prevent bloat
- Re-check size: must be ≤2048 bytes

**Verification**:
- `wc -c active-tasks.md` shows <2048
- Entry format follows spec: `- [sessionKey] agent-name - goal (started: time, status: validated)`

### Step 4: Commit documentation updates
**Task**: Commit `active-tasks.md` reorganization.
- Commit message: `build: mark workspace-builder session validated, prune active-tasks (session 23dad379)`
- Push to origin

**Verification**:
- Git clean after push
- Remote synchronized

---

## Phase 3 — Close the Loop Validation

Run comprehensive checks:

- `./quick health` → all green
- `./quick validate-constraints` → all constraints ✅
  - active-tasks.md ≤2KB
  - MEMORY.md ≤35 lines
  - git clean
  - no temp files
  - APT none pending
  - memory reindex age fresh
- `git status --short` → nothing
- `ls -m *tmp* *.tmp` → no matches (temp files absent)
- Review active-tasks.md format correctness

If any check fails: debug BEFORE committing.

---

## Phase 4 — Finalization

- Ensure no dangling processes (meta-supervisor is allowed to run)
- Write final session log to `memory/2026-02-27.md` (append)
- Update active-tasks.md entry with verification notes (already done in Step 3)
- Session complete

---

## Risk Notes

- Low risk: standard maintenance pattern, well-tested
- Potential issue: active-tasks.md size bloat → prune carefully
- Git push conflicts unlikely (no concurrent push-pending agents expected at this hour)

---

## Success Criteria

All constraints satisfied, workspace clean, remote synchronized, documentation up-to-date.
