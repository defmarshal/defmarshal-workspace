# Workspace Builder - Task Plan

**Session ID:** workspace-builder-$(date +%Y%m%d-%H%M)
**Started:** 2026-02-28 21:01 UTC
**Goal:** Analyze workspace state, implement meaningful improvements, enforce constraints, and maintain system health.

---

## Phase 1: Assessment & Diagnosis

**Objective:** Understand current workspace state and identify actionable improvements.

**Tasks:**
1. Read core workspace files (AGENTS.md, TOOLS.md, MEMORY.md, active-tasks.md)
2. Check git status and recent commits
3. Review daily log (memory/2026-02-28.md) for context
4. Examine CRON_JOBS.md vs actual cron job states (via `quick cron-status`)
5. Validate workspace constraints (`quick validate-constraints`)
6. Assess disk usage and large files (`quick find-large-files`)

**Success criteria:** Complete picture of workspace health, identify at least 1 meaningful improvement.

---

## Phase 2: Fix Cron Job Inconsistency

**Objective:** Align actual cron job states with documentation (disable jobs marked as inactive).

**Tasks:**
1. Compare CRON_JOBS.md "Inactive Cron Jobs" section with `openclaw cron list --json`
2. For each job documented as disabled but actually enabled:
   - Disable via `openclaw cron disable <job-id>`
   - Log action and verify
3. Double-check that enabled jobs match documentation
4. Update CRON_JOBS.md if any documentation is outdated

**Success criteria:** All jobs documented as disabled are actually disabled; no unintended token consumption.

---

## Phase 3: Git Hygiene & Data Commit

**Objective:** Ensure all meaningful changes are tracked and committed.

**Tasks:**
1. Stage `memory/disk-history.json` (legitimate tracking data)
2. Check for any other untracked files that should be committed
3. Review staged changes with `git diff --cached`
4. Commit with appropriate message(s)
5. Push to origin

**Success criteria:** Git clean, all valuable artifacts tracked.

---

## Phase 4: Constraint Validation

**Objective:** Verify all workspace constraints are satisfied.

**Checks:**
- `active-tasks.md` ≤ 2KB
- `MEMORY.md` ≤ 35 lines
- No temp files in workspace root
- All scripts have shebangs
- No pending APT updates
- Memory reindex is fresh (<7 days)
- Git status clean
- Branch hygiene (no stale `idea/*` branches)

**Success criteria:** All constraints green.

---

## Phase 5: Documentation Update & Close Loop

**Objective:** Update tracking files and archive session.

**Tasks:**
1. Update `active-tasks.md`:
   - Add running entry for this workspace-builder session
   - After validation, move to Completed with verification metrics
2. Update `MEMORY.md` if any significant learnings emerged
3. Generate final verification report (health, constraints, git status)
4. Commit any documentation updates with `build:` prefix
5. Push all changes

**Success criteria:** Session fully validated and archived; workspace in green state.

---

## Error Handling

- If any step fails, log the error in `progress.md`, debug, and retry.
- If a fix causes unexpected behavior, revert and investigate.
- Always run `quick health` after changes to ensure system stability.

---

## Notes

- Keep changes small but meaningful.
- Do not make large, sweeping modifications without clear justification.
- Respect existing patterns and conventions.
- Test affected commands before and after changes.
