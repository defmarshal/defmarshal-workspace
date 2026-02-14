# Task Plan — Workspace Builder Run (2026-02-14 22:00 UTC+7)

**Goal:** Analyze workspace health, git hygiene, and documentation; implement small but meaningful improvements; validate and commit.

**Context:**
- Cron-triggered strategic builder; respects quiet hours (23:00–08:00 UTC+7).
- Current time: 22:00 UTC+7 (before quiet window).
- Previous run left untracked files and deprecations to address.

---

## Phases

### 1. Analysis (Discovery) ✅
- [x] Check `git status` and identify untracked files.
- [x] Review workspace for deprecated artifacts (`msearch`, old logs).
- [x] Test critical `quick` commands: `mem`, `search`, `health`, `anime`, `nyaa-top`, `downloads`.
- [x] Verify cron jobs and daemon agents are running.
- [x] Audit MEMORY.md for outdated information (needs updating?).
- [x] Review `active-tasks.md` for stale entries.

### 2. Identification (Plan Changes) ✅
- [x] List removals: `msearch` script (deprecated).
- [x] List additions: stage and commit new content files under `content/`.
- [x] Documentation updates: fix DASHBOARD_README.md reference; add note about `qnt` shortcut? update any stale references.
- [x] Cleanup: remove completed entries from `active-tasks.md` (e.g., previous builder's validated entry).
- [x] Ensure no leftover temp files or logs that should be rotated.

### 3. Implementation (Execution) ✅
- [x] Remove deprecated `msearch`.
- [x] `git add` new content files (content/2026-02-14-afternoon-update.md, content/2026-02-14-daily-digest.md).
- [x] Update MEMORY.md if needed (e.g., note qnt shortcut, recent changes).
- [x] Prune `active-tasks.md`: remove entries with status `validated` that are not current.
- [x] Run `quick health` and other test commands; capture results.

### 4. Validation (Close the Loop)
- [ ] Confirm `git status` clean.
- [ ] Re-test: `quick mem`, `quick search test` (ensure memory search works).
- [ ] Verify no temp files remain in workspace root.
- [ ] Check disk space and system health still acceptable.

### 5. Commit & Push
- [ ] Commit with prefix `build:` summarizing changes.
- [ ] Push to origin.
- [ ] Update `active-tasks.md`: mark this session `validated`, add verification notes.
- [ ] Remove this builder entry after validation (as per registry rules).

---

## Decisions & Rationale
- **Why remove `msearch`?** Deprecated in favor of `claw memory search`; keeping it confuses users and clutters workspace.
- **Why add content files?** They are part of the repo's content/ directory and should be tracked.
- **Why clean `active-tasks.md`?** Prevents registry bloat; completed tasks should be removed after verification.
- **Why update MEMORY.md?** Keep long-term memory accurate; note recent tool additions (qnt shortcut, batch selfie improvements, etc.) as potential learnings.

---

## Error Handling
- If any test command fails, debug before commit.
- If git push fails, inspect remote and resolve conflicts.
- If time is running short (approaching 23:00), stop immediately and resume later.

---

## Success Criteria
- `git status` clean (no untracked files except maybe intentional ignores).
- Deprecated files removed.
- Documentation up-to-date.
- All validations passing.
- Changes pushed to GitHub.
