# Task Plan: Strategic Workspace Improvements (2026-02-20)

**Session:** workspace-builder-cron  
**Goal:** Implement meaningful improvements with focused changes  
**Constraints:** Keep changes small but impactful; validate before commit; use `build:` prefix

---

## Phase 1: Research Hub Deployment Completion

**Why:** The Research Hub is scaffolded but not deployable due to missing exec allowlist grants (git, gh, vercel). We need to make it deployment-ready by adding prerequisite checks and comprehensive documentation.

**Tasks:**
1. Add `quick vercel-prereq` command to check:
   - Whether `git`, `gh`, `vercel` binaries exist in PATH
   - Whether they are allowlisted in `~/.openclaw/exec-approvals.json`
   - Provide clear instructions for user to enable deployment
2. Enhance `apps/research-hub/README.md` with:
   - Deployment prerequisites section (allowlist, tokens, repo setup)
   - Step-by-step manual deployment guide
   - Troubleshooting tips
3. Update `docs/research-hub-deployment.md` (if exists) or create it with complete instructions
4. Test the new `quick vercel-prereq` command locally

**Success criteria:** User can run `quick vercel-prereq` and receive actionable guidance; deployment steps clearly documented.

---

## Phase 2: Build Archive Cleanup

**Why:** The `build-archive/` directory contains 15 old planning files (task_plan, findings, progress) from Feb 15-17. These have been superseded by daily logs and MEMORY.md. Keeping them clutters the workspace and violates the principle of minimalism.

**Tasks:**
1. Review contents of `build-archive/` to ensure no critical historical data
2. Create a compressed tarball backup: `build-archive-backup-YYYY-MM-DD.tar.gz` in workspace root
3. Remove the `build-archive/` directory entirely
4. Update any references to these files (if found in docs or scripts)
5. Document the cleanup in today's daily log (`memory/2026-02-20.md`)

**Success criteria:** Workspace free of old planning files; backup safely stored; no broken references.

---

## Phase 3: Enhanced System Validation (Orphaned Agent Detection)

**Why:** While active-tasks.md is currently clean, there have been incidents of orphaned agents leaving stale entries. A proactive check can detect sessions that are marked running but have no active process.

**Tasks:**
1. Create script `scripts/check-orphaned-agents.sh` that:
   - Lists all sessions via `openclaw sessions list --json`
   - Identifies sessions with status "running" but no recent activity (stale)
   - Reports findings with suggestions
   - Exit 0 if none, 1 if issues found
2. Add `quick orphan-check` command to invoke this script
3. Test the command to ensure it works
4. Optionally: integrate into `supervisor.sh` as an additional health check

**Success criteria:** `quick orphan-check` runs successfully and provides useful output.

---

## Phase 4: Validation & Commit

**Tasks:**
1. Run `./quick health` - ensure all systems OK
2. Test each modified/new command:
   - `quick vercel-prereq`
   - `quick orphan-check`
3. Verify no temp files were created
4. Confirm `active-tasks.md` size < 2KB
5. If all pass: commit changes with `build:` prefix and push to origin
6. Update `active-tasks.md` with this session's verification status

---

## Risk Mitigation

- **Backup before deletion:** `build-archive/` will be tar'd before removal
- **Command testing:** All new commands will be tested before final commit
- **Documentation updates:** Any new features will be reflected in `quick` help
- **No aggressive changes:** Stick to housekeeping and non-invasive improvements

---

**Estimated impact:** Medium (cleaner workspace, better deployment readiness, improved monitoring)

**Estimated token usage:** <50k (planning + execution)
