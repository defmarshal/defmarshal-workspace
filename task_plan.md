# Workspace Build Plan — 2026-02-18 Evening

**Builder:** mewmew (workspace-builder cron)
**Trigger:** Scheduled run (Asia/Bangkok 02:00 UTC = 09:00 local)
**Goal:** Strategic improvements aligned with long-term system integrity

---

## Phase 1: Pre-Flight Checks

- [ ] Read active-tasks.md (ensure no conflict)
- [ ] Check git status (untracked/dirty files)
- [ ] Verify memory health (quick memory-status)
- [ ] Confirm cron schedules (quick cron-schedules)
- [ ] Review active projects and recent lessons

**Validation criteria:** All checks green before proceeding.

---

## Phase 2: active-tasks.md Size Enforcement

**Problem:** active-tasks.md currently ~4.0KB, exceeds 2KB hard limit.

**Actions:**
1. Read current content and parse entries
2. Remove stale validated entries older than 7 days (archive to memory/YYYY-MM-DD.md)
3. Keep only:
   - Currently running agents
   - Very recent validated entries (last 24h) for audit trail
4. Ensure file remains valid markdown
5. Update MEMORY.md index if major changes

**Verification:**
- `ls -lh active-tasks.md` shows ≤2KB
- File content remains syntactically correct

---

## Phase 3: System Updates — Safe Application

**Problem:** 18 APT updates pending. Could include security fixes.

**Actions:**
1. Run `./quick updates-check` to list updates
2. Categorize: security vs regular
3. Dry-run: `./quick updates-apply --dry-run`
4. If dry-run looks safe (no large kernels, no removed packages), execute: `./quick updates-apply --execute`
5. If updates applied, reboot if required (kernel updates)
6. Log outcome to active-tasks and memory

**Risk mitigation:**
- Never auto-apply if dry-run shows critical changes (e.g., package removals, held packages)
- If uncertain, stop and ask user

**Verification:**
- `./quick health` shows "Updates: 0"
- No pending reboot required (or reboot performed)

---

## Phase 4: Memory Reindex Robustness Enhancement

**Problem:** Voyage AI free tier = 3 RPM; full reindex of ~15 files can take ~20min if we space calls. Current meta-agent uses 1s delay which may still hit burst limits. Weekly cron at Sunday 04:00 Asia/Bangkok may sometimes fail due to rate limits.

**Actions:**
1. Inspect `agents/meta-agent.sh` memory reindex logic
2. Consider adaptive backoff: if rate-lock present, skip until next day
3. Or, batch index with larger delay (3s between calls) to stay under 3 RPM
4. Improve rate-lock detection in `quick memory-reindex-check` to be more accurate
5. Update TOOLS.md with current reindex status and manual trigger instructions

**Goal:** Make memory reindex more reliable; avoid repeated 429 errors.

**Verification:**
- `./quick memory-reindex-check` correctly defers when rate-limited
- Manual `./quick memory-index` completes without hitting rate limit (test on small batch if cautious)

---

## Phase 5: Agent Health Monitoring Dashboard

**Problem:** Quick health summary is terse but lacks visibility into agent-specific health (e.g., when was last successful run of each cron?).

**Actions:**
1. Create `quick agent-status` command (or enhance existing) to show:
   - List of OpenClaw cron jobs
   - Last run time and status (from `openclaw cron runs <jobId>`)
   - Next scheduled run
2. Add to quick launcher script and help
3. Document in TOOLS.md

**Verification:**
- `./quick agent-status` outputs a readable table
- Shows useful info for supervisor and meta-agent runs

---

## Phase 6: Validation & Close-the-Loop

Standard checklist:
- [ ] Run `./quick health` — all systems green
- [ ] Test new commands (`./quick agent-status`, `./quick memory-dirty`)
- [ ] Check `git status` — clean or only expected changes
- [ ] No temp files left in workspace root
- [ ] active-tasks.md ≤2KB
- [ ] All changes committed with appropriate prefix (`build:`)

---

## Phase 7: Commit & Push

- Create git commit with message prefix `build:`
- Include all modified files (new scripts, updated docs, cleaned active-tasks)
- Push to origin/master
- Update active-tasks.md entry for this build with verification results

---

## Notes

- Keep changes small but meaningful; prefer incremental improvements over big rewrites.
- If any step fails or requires manual intervention, document in `findings.md` and ask user before proceeding.
- Respect boundaries: no external actions without explicit need.
