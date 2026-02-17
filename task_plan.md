# Workspace Builder Plan — 2026-02-17 21:00 UTC

## Mission
Analyze the workspace and implement meaningful improvements aligned with long-term objectives: reliability, performance, and maintainability.

## Context (from memory & current state)
- Previous builder run (19:00 UTC) completed documentation updates and validation; left planning artifacts in root and marked active-tasks entry as validated but did not remove it.
- Core systems stable: disk 79%, gateway healthy, memory main clean.
- Voyage AI rate limits (3 RPM) continue to cause memory reindex failures; meta-agent already watches and triggers reindex, but repeated failures can hammer the API. A rate-lock mechanism would reduce noise and avoid unnecessary attempts.
- Build archive (`builds/`) accumulates timestamped planning directories; after many runs it could grow unchecked. Need retention policy (e.g., keep last 10 builds).
- active-tasks.md includes a stale builder entry (validated) that should be archived and removed to keep the registry clean.
- Quick launcher and health checks are comprehensive.
- Systemd linger enabled, gateway stable.

## Goal
- Clean up active-tasks.md: archive stale builder verification note, remove old entry, add fresh builder entry for this run.
- Add memory reindex rate-lock protection via meta-agent modifications to prevent repeated Voyage 429 attempts within a short window.
- Add cleanup-build-archive script and quick command to prune old build directories.
- Update TOOLS.md with new utilities and notes.
- Validate system health and functionality.
- Commit changes with prefix `build:` and push.
- Mark this builder as validated in active-tasks.md with verification summary.

## Success Criteria
- active-tasks.md contains only current running agents (torrent-bot) and this builder (running → validated at end).
- `memory/.voyage-rate-lock` file management works: created when rate limit occurs, expires after 1 hour; meta-agent respects it.
- `quick cleanup-build-archive [--execute]` available and correctly lists/removes old builds (dry-run safe by default).
- TOOLS.md updated with entries for rate-lock and build-archive cleanup.
- `./quick health` passes; no errors in supervisor alerts.
- All changes committed and pushed; no uncommitted artifacts left behind.

## Task Plan (Phases)

### Phase A: Active Tasks Housekeeping
- A.1: Read memory/2026-02-17.md and append the stale builder verification note as a completed task record.
- A.2: Remove the stale `[build]` entry (status: validated, started 19:00 UTC) from active-tasks.md.
- A.3: Add a fresh `[build]` entry for this builder with status `running`, started: 2026-02-17 21:00 UTC.

### Phase B: Meta-Agent Rate-Lock Enhancement
- B.1: Create lock file path constant: `memory/.voyage-rate-lock`.
- B.2: In `agents/meta-agent.sh`, modify the "memory reindex" action:
   - Before reindex: if lock file exists and mtime < 1 hour ago, skip and log "Skipping due to Voyage rate-lock".
   - Run reindex and capture output.
   - If output indicates 429/rate limited, `touch` the lock file; exit code 1 (continue with other actions).
   - If reindex succeeds and lock file exists, `rm -f` the lock file.
- B.3: Add a small helper function `rate_lock_active` and `set_rate_lock` to keep code clean (inline in script).
- B.4: Test syntax with `bash -n` and verify logic mentally.

### Phase C: Build Archive Cleanup Utility
- C.1: Write `scripts/cleanup-build-archive.sh`:
   - Default dry-run: list directories that would be removed.
   - Option `--execute` performs deletion.
   - Keep the N most recent builds in `builds/` (by directory name timestamp sort). Default keep=10.
   - Exclude `builds/` itself and any non-directory entries.
   - Exit codes: 0 = clean or dry-run success, 1 = error, 2 = dry-run with deletions pending.
- C.2: Add `cleanup-build-archive` case to quick launcher with appropriate flags.
- C.3: Test dry-run (should list nothing if <10 builds) and verify output format.
- C.4: Verify script is executable (`chmod +x`).

### Phase D: Documentation Updates
- D.1: Update `TOOLS.md`:
   - Add a section "Meta-Agent Rate-Lock" describing the lock file and behavior.
   - Add "Build Archive Cleanup" describing the script and quick command.
   - Note that quiet hours are removed system-wide (already there maybe).
- D.2: Ensure `AGENTS.md` still accurate (no change likely).

### Phase E: Validation & Testing
- E.1: Run `./quick health` and confirm all subsystems OK.
- E.2: Run `./quick memory-reindex-check` and note status.
- E.3: Run `./quick voyage-status` to confirm no recent rate limit warnings (or handle accordingly).
- E.4: Run `bash ./scripts/cleanup-build-archive.sh` dry-run; ensure exit code 0 and sensible output.
- E.5: Check for any temporary files (e.g., lock file) and ensure they are either intended or cleaned.
- E.6: Verify that no agent is in a failed state: `openclaw sessions list` (optional).

### Phase F: Commit, Push, and Finalize
- F.1: Stage all changes: active-tasks.md, memory/2026-02-17.md (if modified), agents/meta-agent.sh, scripts/cleanup-build-archive.sh, quick (added command), TOOLS.md, and the new planning files (task_plan.md, findings.md, progress.md).
- F.2: Commit with message: `build: meta-agent rate-lock; add build-archive cleanup; prune active-tasks; update docs`
- F.3: Push to origin and verify success.
- F.4: Update active-tasks.md entry for this builder to status `validated` and add verification summary (new lines under the entry).
- F.5: Stage and push the active-tasks.md update: commit `build: validate workspace-builder` or similar.

## Dependencies & Risks
- Modifying meta-agent could introduce syntax errors; test with `bash -n` and keep changes minimal.
- Rate-lock skip logic should not suppress reindex indefinitely; use 1-hour TTL.
- Build cleanup script must sort timestamps correctly; directory names are `build-YYYY-MM-DD-HHMM` format.
- Risk: forgetting to add new files to git; verify with `git status` before commit.
- No impact on running services beyond meta-agent behavior.

## Notes
- This builder respects the 2-hour cron schedule. All changes should be backward-compatible.
- The rate-lock file is stored in `memory/` to persist across reboots but not clutter workspace root.
- Build archive retention: keep last 10 builds, remove older ones. This provides history without unbounded growth.
- All quick commands remain local; no external approvals needed.
