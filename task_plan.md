# Workspace Builder Task Plan

**Session Key:** workspace-builder-20260224-0306
**Trigger:** Cron schedule (every 2h UTC)
**Timestamp:** 2026-02-24 03:06 UTC

---

## Mission

Fix cron schedule validation script JSON parsing bug and verify workspace health.

---

## Constraints

- active-tasks.md must be ≤ 2KB (2048 bytes)
- MEMORY.md must be ≤ 30 lines
- Git must be clean after validation
- No temp files
- All changes committed with `build:` prefix
- Close the loop: run `quick health`, verify changes, then commit

---

## Current State

- Git: clean, up-to-date
- Health: excellent (disk 68%, gateway healthy, memory clean)
- active-tasks.md: 1853 bytes, 39 lines (OK)
- MEMORY.md: 30 lines (OK)
- Issue found: `quick cron-schedules` exits with code 1 due to JSON parsing failure in `scripts/validate-cron-schedules.sh`
- Root cause: The script does not filter Doctor warnings from `openclaw cron list --json` output (missing `sed -n '/^{/,$p'`)

---

## Phase 1: Analysis

Already complete (see above). The `show-cron.sh` script already has the fix; `validate-cron-schedules.sh` does not.

---

## Phase 2: Implementation

### Task 2.1: Fix validate-cron-schedules.sh

- Add `sed -n '/^{/,$p'` filter to the `openclaw cron list --json` pipeline
- Add JSON validation check (like show-cron.sh) to fail early with helpful message
- Test: `./quick cron-schedules` should exit 0 and show validation results

### Task 2.2: Verify all constraints

- Ensure active-tasks.md size stays <2KB
- MEMORY.md ≤ 30 lines
- Run `./quick health` and `./quick validate`

---

## Phase 3: Finalization

- Commit changes with message: "build: fix validate-cron-schedules.sh JSON parsing"
- Update active-tasks.md: add validated entry for this session, prune oldest if needed to maintain <2KB
- Push to origin
- Final verification

---

**Plan created:** 2026-02-24 03:15 UTC
