# Task Plan — Workspace Builder Run (2026-02-15 06:00 UTC+7)

**Goal:** Perform a strategic health check, capture critical learnings from recent operations, and maintain active-tasks registry hygiene.

**Context:**
- Cron-triggered builder runs every 2h; respects quiet hours (23:00–08:00 UTC+7).
- Current time: 06:00 UTC+7 (outside quiet window).
- Previous builder run (22:00 UTC+7) completed successfully and was committed.
- Workspace is clean and healthy; pending items are documentation updates rather than functional fixes.

---

## Phases

### 1. Analysis (Discovery)
- [ ] Verify system health via `quick health`.
- [ ] Test key commands: `quick mem`, `quick search test`, `quick agents`.
- [ ] Review daily log `memory/2026-02-14.md` for noteworthy learnings and decisions.
- [ ] Audit `MEMORY.md` for outdated or missing information.
- [ ] Inspect `active-tasks.md` for stale validated entries (e.g., previous builder entry).

### 2. Identification (Plan Changes)
- [ ] List specific changes:
  - Update `MEMORY.md`: Append learnings from Feb 14 operations (daemon persistence, aria2 RPC config, Telegram dash normalization, non-interactive alternatives).
  - Clean `active-tasks.md`: Remove entries with status `validated` that are not current (specifically the previous workspace-builder entry).
- [ ] Determine if any other documentation updates are needed (quick help, DASHBOARD_README.md already fixed; qnt shortcut documented in MEMORY.md).
- [ ] Confirm no other cleanup needed (no temp files, logs fine).

### 3. Implementation (Execution)
- [ ] Edit `MEMORY.md` to add new learnings subsection.
- [ ] Edit `active-tasks.md` to remove stale validated entries.
- [ ] Ensure changes are staged for commit.

### 4. Validation (Close the Loop)
- [ ] Re-run `quick health` and capture output.
- [ ] Re-run `quick mem` and `quick search "daemon"` to verify memory search works.
- [ ] Run `quick agents` to confirm agents are still running.
- [ ] Run `git status` to confirm clean working tree (only intended changes).
- [ ] Verify no leftover temp files or unintended modifications.

### 5. Commit & Push
- [ ] Stage all changes (`git add -u` and any new files).
- [ ] Commit with prefix `build:` summarizing changes (e.g., "build: capture Feb 14 learnings; clean active-tasks").
- [ ] Push to origin.
- [ ] (Optional) Update `active-tasks.md` to reflect this builder run's completion? Per rules, we will remove any transient entry we added; no additional action needed.

---

## Decisions & Rationale
- **Why capture learnings now?** The Feb 14 daily log contains valuable insights about daemon persistence, aria2 RPC quirks, Telegram dash compatibility, and chat UX. These belong in long-term memory to inform future troubleshooting and avoid repeating mistakes.
- **Why clean active-tasks?** Keeping validated entries clutters the registry and violates the "remove after verification" rule. A clean registry improves clarity for ongoing agent management.
- **Minimal scope:** Since the workspace is already well-maintained, this run focuses on documentation hygiene rather than code changes.

---

## Error Handling
- If any validation command fails, debug and fix before commit.
- If git push fails, inspect remote state and resolve conflicts.
- If time approaches 23:00 UTC+7 (quiet window), pause immediately and resume later.

---

## Success Criteria
- `git status` clean with only intended documentation updates.
- `MEMORY.md` updated with new learnings from Feb 14.
- `active-tasks.md` has no stale validated entries (only running daemons).
- All validation checks pass.
- Changes pushed to GitHub.
