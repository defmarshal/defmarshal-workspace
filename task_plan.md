# Workspace Strategic Improvement Plan
**Session:** workspace-builder-20260228-1307
**Goal:** Archive completed tasks, clean stale branches, enforce constraints
**Started:** 2026-02-28 13:07 UTC

---

## Phase 1: Archive Validated Workspace-Builder Entry
**Why:** The entry `[workspace-builder-20260228-1107]` has status `validated` but remains in active-tasks.md Running section. Completed tasks must be archived to daily logs to keep Running section accurate and active-tasks under 2KB.

**Steps:**
1. Read active-tasks.md to extract the full entry details for `workspace-builder-20260228-1107`.
2. Read `memory/2026-02-28.md` to locate the "## Archived Completed Tasks" section.
3. Append the entry (with its verification metrics) to that section, preserving the established format.
4. Remove the entry from active-tasks.md's Running section.
5. Verify active-tasks.md size remains <2KB.
6. Commit both files with message: `build: archive completed workspace-builder session 20260228-1107`
7. Push to origin/master.

**Success:** active-tasks.md no longer contains the validated entry; daily log includes it with proper formatting.

---

## Phase 2: Cleanup Stale Idea Branches
**Why:** Idea branches that are stale (no recent activity, abandoned, or empty) clutter the repository and should be removed to maintain branch hygiene. Previous workspace-builder runs have pruned stale branches successfully.

**Steps:**
1. List all branches matching `idea/*`.
2. For each branch, check last commit date and merge status.
3. Identify branches that are:
   - Empty (no commits) OR
   - Older than 30 days with no activity OR
   - Marked as abandoned/experimental without merge
4. Delete identified stale branches both locally and remotely (`git branch -d`, `git push origin --delete`).
5. Document deletions in findings.md.
6. Commit a summary if branches were deleted: `build: prune stale idea branches`
7. Push to origin.

**Success:** No stale idea branches remain; repository cleaner.

---

## Phase 3: Final Validation & Documentation
**Why:** Ensure all constraints remain satisfied and document the session outcome.

**Steps:**
1. Run `./quick validate-constraints` to verify all checks pass.
2. Run `./quick health` to confirm overall system health.
3. Verify `git status` clean and up-to-date with origin.
4. Update active-tasks.md:
   - Add a new running entry for this session: `[workspace-builder-20260228-1307]`
   - Include initial status and start time.
5. If active-tasks.md approaches 2KB, prune oldest completed entries.
6. Create/update progress.md with phase completion notes.

**Success:** All constraints green, active-tasks updated with current session, git clean.

---

## Phase 4: Close the Loop
**Steps:**
1. After ensuring all work is done, update active-tasks entry to `status: validated` with detailed verification metrics.
2. Prune any oldest completed entries if needed to keep size <2KB.
3. Commit active-tasks.md update: `build: mark workspace-builder session validated (2026-02-28 13:07 UTC) - archive task, prune branches`
4. Push to origin.
5. Perform final validation: `./quick validate-constraints` one last time.

**Success:** Repository fully synchronized; session properly closed; all constraints satisfied.

---

## Risk Mitigation
- **Active-tasks edit:** Before removing any entry, copy its full details (including verification notes) to daily log to preserve history.
- **Ideas deletion:** Only delete branches that are clearly stale (empty or >30d no activity). Do not delete active/work-in-progress branches.
- **Git pushes:** Verify remote is `origin/master` before pushing.
- **Backout:** If any step fails, debug and fix; use `git revert` if needed.

---

## Metrics for Success
- active-tasks.md size < 2KB after archival
- No stale idea branches remain
- All constraints (including shebang) pass
- Git clean and pushed
- Daily log properly updated with archived entry
