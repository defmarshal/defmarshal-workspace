# Workspace Builder Plan

**Started:** 2026-02-18 16:00 UTC  
**Session ID:** agent:main:cron:23dad379  
**Goal:** Analyze workspace state, fix critical misconfigurations, validate system health, commit improvements.

---

## Phase 1: Diagnose Cron Misconfiguration

**Objective:** Verify which cron jobs deviated from CRON_JOBS.md documentation and identify the root cause.

**Actions:**
1. Run `./quick cron-status` and capture current OpenClaw cron schedules.
2. Compare each job against `CRON_JOBS.md` to create a diff table.
3. Determine if schedules were manually edited, or if the previous fix (workspace-builder build at 14:00 UTC) failed to persist.

**Expected Output:** Table of mismatched schedules with job IDs, current vs intended expressions.

**Success Criteria:** Complete list of misconfigured jobs; clear understanding of cause.

---

## Phase 2: Correct Cron Schedules

**Objective:** Update all OpenClaw cron jobs to match their documented schedules using `openclaw cron update`.

**Actions:**
1. For each misconfigured job, call `openclaw cron update --job-id <id> --patch '{"schedule":{"expr":"<correct-cron>"}}'`.
2. Use timezone `Asia/Bangkok` for jobs that require it (all except those explicitly UTC).
3. Log each update with verification that `openclaw cron list --json` reflects the change.

**Jobs to fix (expected based on latest status):**
- `workspace-builder`: `0 */2 * * *`
- `random-torrent-downloader`: `0 */2 * * *`
- `dev-agent-cron`: `0,20,40 8-22 * * *`
- `content-agent-cron`: `0,10,20,30,40,50 8-22 * * *`
- `research-agent-cron`: `0,15,30,45 8-22 * * *`
- `agni-cron`: `0 */2 * * *`
- `agent-manager-cron`: `0,30 * * *`
- `supervisor-cron`: `*/5 * * * *`

**Success Criteria:** All schedules match CRON_JOBS.md; `cron-status` shows correct expressions.

---

## Phase 3: Secondary Health Checks

**Objective:** Ensure other subsystems are operating correctly.

**Checks:**
1. Run `./quick memory-dirty` → expect main store `dirty=False`.
2. Run `./quick health` → expect all OK.
3. Check `agents/meta-agent.sh` last run status via `cron list` (should be `ok` and no consecutive errors).
4. Verify `gateway-fix.sh` has been applied by user; if gateway still showing issues, add note in findings.

**Success Criteria:** No alerts; all checks pass.

---

## Phase 4: Documentation & Housekeeping

**Objective:** Keep documentation aligned with reality.

**Actions:**
1. Ensure any changes to schedules are reflected in `CRON_JOBS.md` (it already states correct schedules; just verify consistency).
2. If the memory-dirty command had issues, fix them; otherwise leave as-is.
3. No new files to create; planning files already exist or will be created by this session.

**Success Criteria:** Docs up to date; no stale TODOs.

---

## Phase 5: CLOSE THE LOOP Validation

**Objective:** Verify that fixes are effective and system is stable.

**Actions:**
1. Run `./quick health` → must pass.
2. Run `./quick cron-status` and verify schedules match CRON_JOBS.md.
3. Run `./quick memory-status` → main store clean.
4. Run `./quick mem` and `./quick search "test"` to confirm memory functions.
5. Check `git status` – should be clean (no uncommitted changes).
6. Verify no temporary files left in workspace root (e.g., *.tmp, *.log from this session).
7. Check `active-tasks.md` – should have <=2KB size and reflect this builder's entry with verification.

**Success Criteria:** All validation steps pass; system stable.

---

## Phase 6: Commit & Push

**Objective:** Persist changes to GitHub.

**Actions:**
1. `git add` any modified files (likely none; this builder only changes cron state which is stored in OpenClaw config, not tracked by git; but if we edit CRON_JOBS.md or other docs, include them).
2. `git commit -m "build: fix cron misconfigurations; validate system health; ensure scheduling integrity"`.
3. `git push origin master`.
4. Verify push succeeded.

**Success Criteria:** Commit created with correct prefix; push successful.

---

## Phase 7: Update Active Tasks

**Objective:** Mark this session as validated with verification details.

**Actions:**
1. Read `active-tasks.md`.
2. Add an entry for this session with `status: validated` and concise verification results.
3. Prune any old validated entries to stay under 2KB.

**Success Criteria:** active-tasks.md current and within size limit.

---

## Risk Mitigation

- If a cron update fails, capture error and retry with correct job ID.
- If memory-dirty is broken, inspect script at `memory-dirty` and fix logic.
- If health check fails, investigate before committing any docs changes.

---

## Long-term Objectives Alignment

This run addresses **System Reliability & Autonomy** by restoring essential timing semantics, reducing resource contention from over-frequent agent spawns, and ensuring health observability remains accurate.
