# Workspace Builder - Task Plan

**Session:** `cron:23dad379-21ad-4f7a-8c68-528f98203a33`  
**Started:** 2026-02-17 07:00 UTC  
**Goal:** Strategic improvements and validation

---

## Phase 1: Assessment & Diagnostics

**Objective:** Analyze current state and identify issues.

Tasks:
1. Check active-tasks.md for conflicts ✓ already done
2. Read SOUL.md, USER.md, memory/2026-02-17.md ✓
3. Search memory for past decisions (memory_search) ✓
4. Run `quick health` and `quick memory-status` ✓
5. Examine git status ✓ clean
6. Check for orphaned artifacts (pycache, temp files, empty plans)
7. Check memory database health (main + torrent-bot)
8. Verify cron job configuration (openclaw cron list)
9. Inspect builds/ directory for archival completeness

**Deliverable:** Initial findings report into `findings.md`.

---

## Phase 2: Targeted Improvements

**Objective:** Implement meaningful, small changes.

Potential improvements (prioritized):
- A. Fix torrent-bot memory database (dirty, 0 files indexed)
- B. Run memory reindex if needed (reindex-check)
- C. Verify agent log rotation (aria2.log rotation, other logs)
- D. Check for stale lock files / empty plan files (cleanup-agent-artifacts simulation)
- E. Validate that quiet hours are respected by all cron jobs
- F. Check gitignore coverage (are any secrets or temp files being tracked?)
- G. Verify daily digest generation (reports/ exists and has recent file?)
- H. Add memory stats to quick health or create a monitoring script
- I. Ensure builds/ directory has proper structure; consider compressing old builds (>2 weeks)

**Selection:** Implement all except I (defer compression) and G (quick verification only). Keep changes small and safe.

---

## Phase 3: Close the Loop Validation

**Objective:** Confirm all changes work and system remains healthy.

Tests:
- `quick health` passes
- `quick memory-status` shows healthy (no dirty)
- `quick mem` and `quick search test` work
- Git status clean, no untracked artifacts
- All files properly committed

---

## Phase 4: Commit & Update

**Objective:** Push changes with `build:` prefix and update active-tasks.md.

Actions:
- Commit with message: `build: <summary of changes>`
- Push to GitHub
- Add validation entry to active-tasks.md with verification results
- Ensure session status reflects completion

---

## Success Criteria

- No errors during execution
- Memory system clean (no dirty databases)
- Disk usage stable, no orphaned files
- All validations pass
- Changes committed and pushed

---

## Notes

- The previous builder runs (01:00 UTC, 05:00 UTC) already did major cleanup: MEMORY.md reorganization, pycache removal, builds/ archiving, systemd linger documentation.
- This run should address any lingering issues (e.g., torrent-bot memory) and ensure ongoing health.
- Keep changes minimal and focused on system health, not new features.
