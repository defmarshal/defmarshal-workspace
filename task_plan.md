# Workspace Strategic Improvement Plan
**Session:** workspace-builder-20260228-1107
**Goal:** Archive completed tasks, commit auto-generated files, enhance validation, maintain constraints
**Started:** 2026-02-28 11:07 UTC

---

## Phase 1: Active Tasks Archive Cleanup
**Why:** The entry `[workspace-builder-20260228-0907]` is validated but still in Running section. It should be archived to today's daily log and removed from active-tasks.md to keep the Running section accurate.

**Steps:**
1. Read today's daily log (memory/2026-02-28.md) to locate "## Archived Completed Tasks" section.
2. Append the completed entry (with its verification details) to that section, preserving format.
3. Remove the entry from active-tasks.md.
4. Verify active-tasks.md size remains <2KB.
5. Commit active-tasks.md and daily log updates with message: `build: archive completed workspace-builder session 20260228-0907`

**Success:** active-tasks.md no longer contains the validated entry; daily log includes it.

---

## Phase 2: Commit Auto-Generated Dashboard Files
**Why:** `apps/dashboard/data.json` and `memory/disk-history.json` are modified by agent runs (supervisor/agent-manager). They should be committed to keep git clean and version dashboard data.

**Steps:**
1. Review changes via `git diff` to ensure they are expected (timestamp updates, metrics).
2. Stage both files.
3. Commit with message: `build: update dashboard data and disk history (workspace-builder 20260228-1107)`
4. Push to origin/master.

**Success:** Git clean and up-to-date.

---

## Phase 3: Enhance Constraint Validation
**Why:** Proactive script hygiene: ensure all shell scripts have shebangs. This prevents runtime errors when scripts are executed without proper interpreter directive.

**Steps:**
1. Add a new check to `scripts/validate-constraints.sh`:
   - Find all `scripts/*.sh` (or scripts/**/*.sh)
   - Verify each is executable (already true) and has a shebang as first line.
   - Count missing shebangs; if any, exit with error.
2. Test the new check by intentionally breaking a test script (dry-run), then revert.
3. Ensure existing scripts pass.

**Success:** `./quick validate-constraints` includes ✅ "Shebang check: all scripts have #!" line; exit code 0.

---

## Phase 4: Final Validation & Documentation
**Why:** Ensure all constraints satisfied and document session.

**Steps:**
1. Run `./quick validate-constraints` until all green.
2. Run `./quick health` to confirm overall health.
3. Verify git clean and pushed.
4. Update active-tasks.md: add running entry for this session `[workspace-builder-20260228-1107]` and later mark validated with verification metrics.
5. If active-tasks.md approaches 2KB, prune oldest completed entries.
6. Optionally update MEMORY.md (if significant learning emerges) but keep ≤35 lines.

**Success:** All constraints green, active-tasks updated, git clean.

---

## Phase 5: Close the Loop
**Steps:**
1. After validation, update active-tasks.md entry status to validated with detailed verification.
2. If needed, prune oldest completed entries to keep size <2KB.
3. Commit active-tasks.md update with message: `build: mark workspace-builder session validated (2026-02-28 11:07 UTC) - all constraints satisfied`
4. Push to origin.
5. Final sanity: `./quick validate-constraints` one last time.

**Success:** Repository fully synchronized; session properly closed.

---

## Risk Mitigation
- **Active-tasks edit:** Before removing the entry, copy its full details to daily log to preserve history.
- **Constraint check:** Ensure new shebang validation does not false-positive on non-shell files; limit to `*.sh` under scripts/.
- **Git pushes:** Verify remote is origin/master before pushing to avoid mismatches.
- **Backout:** If any step fails, debug and fix before proceeding; use git revert if needed.

---

## Metrics for Success
- active-tasks.md size < 2KB after archival
- All 8+ constraints (including new shebang) satisfied
- Git clean and pushed
- No temp files
- SHEBANG check added and passing
- Daily log updated with archived task details
