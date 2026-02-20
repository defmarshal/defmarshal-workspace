# Workspace Builder Plan: Documentation Cleanup & Validation

**Session Key:** (will be assigned by active-tasks.md)
**Started:** 2026-02-20 05:00 UTC
**Goal:** Improve documentation clarity and fix structural issues in CRON_JOBS.md; ensure all metadata is accurate.

---

## Phase 1: Assessment & Planning

**Actions:**
- Read AGENTS.md, MEMORY.md, recent daily logs (2026-02-19, 2026-02-20)
- Review active-tasks.md → confirmed empty (no conflicts)
- Analyze system health → all OK
- Identify documentation issues:
  - CRON_JOBS.md "System Cron" section has malformed headings and mixed entries
  - TOOLS.md memory section notes are slightly outdated (mentions 15/15 files, 43 chunks vs current 16/16, 69)
  - Could add a note about the autonomous schedule validation script

**Verification:** Create task_plan.md, findings.md, progress.md and commit them early.

---

## Phase 2: Documentation Fixes

### Fix 1: Restructure System Cron section in CRON_JOBS.md

**Current problems:**
- Headings are adjacent: "### Agent Startup (Daemon Bootstrap)" followed by "### Gateway Watchdog (system crontab)" on next line, but the content that follows is misaligned.
- The hourly gateway watchdog entry appears first, then separator `---`, then the `@reboot` agent startup entry. It's confusing which heading goes with which.
- The description for "Agent Startup" actually says "Ensures all background agents and daemons (dev, content, research, torrent-bot, aria2) are running after system boot." That matches @reboot, not the hourly watchdog.

**Correct structure:**
```
## System Cron (user crontab)
(as of note...)

### Gateway Watchdog (system crontab)
- Schedule: Every hour (`0 * * * *`)
- Command: /path/to/gateway-watchdog.sh
- Description: Checks gateway, restarts if down. Runs outside OpenClaw.

### Agent Startup (Daemon Bootstrap)
- Schedule: `@reboot` with 60-second delay
- Command: start-background-agents.sh
- Description: Ensures agents (dev, content, research, torrent-bot, aria2) are running after boot.
```

**Action:** Edit CRON_JOBS.md to separate these clearly.

### Fix 2: Update TOOLS.md memory section

**Current:** States Voyage AI not in use due to rate limits; references "15/15 files indexed, 43 chunks" (likely old data). Should reflect current status: Voyage disabled, local FTS+ fallback active and healthy.

**Action:** Adjust wording to be accurate without specific numbers that drift. Mention that `quick memory-status` shows current health.

### Fix 3: Add note about schedule validation

The `scripts/validate-cron-schedules.sh` runs automatically and corrects drift. Document this in CRON_JOBS.md near the top or in a "Maintenance" section.

---

## Phase 3: Validation

- Run `./quick health` → must be clean
- Run `./quick cron-status` → ensure no errors
- Run `./quick validate` (if available) or manually check key aspects
- Verify that all changes are proper markdown (no broken formatting)
- Check `active-tasks.md` size (<2KB)

---

## Phase 4: Commit & Update

- Commit all changes with prefix `build:`
- Push to origin
- Update active-tasks.md: mark this workspace-builder session as `validated` and include verification notes
- Archive planning files (task_plan.md, findings.md, progress.md) to daily log or keep? They become part of the commit.

---

## Success Criteria

- CRON_JOBS.md System Cron section is clear, correctly paired, no ambiguity
- TOOLS.md memory section accurately reflects current state (Voyage disabled, fallback working)
- All files valid markdown; system health passes
- Changes pushed; active-tasks.md updated
