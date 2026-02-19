# Task Plan: Sync CRON_JOBS.md with Actual Cron Jobs

**Session ID:** agent:main:cron:23dad379-21ad-4f7a-8c68-528f98203a33
**Started:** 2026-02-19 21:00 UTC (fresh run)
**Goal:** Ensure CRON_JOBS.md accurately reflects all scheduled cron jobs (OpenClaw + system) to maintain a reliable single source of truth.

---

## Context

- The system is healthy; all cron schedules as currently configured are functioning correctly.
- However, documentation (CRON_JOBS.md) is missing several cron jobs that exist in the system:
  - notifier-cron (every 2h UTC)
  - git-janitor-cron (every 6h UTC)
  - archiver-manager-cron (weekly Sunday 02:00 UTC)
- Additionally, the System Cron section incorrectly states gateway-watchdog runs every 5 minutes; actual schedule is hourly (`0 * * * *`).
- email-cleaner-cron is not present in the current cron list; it may have been removed or renamed; no action needed if absent.

---

## Phase 1: Analysis & Fact Gathering

- [ ] Run `./quick cron-status` and capture full JSON or list of all OpenClaw cron jobs
- [ ] Compare each job against CRON_JOBS.md entries
- [ ] List missing jobs: notifier-cron, git-janitor-cron, archiver-manager-cron
- [ ] Note any schedule/description mismatches

---

## Phase 2: Document Updates

- [ ] Edit CRON_JOBS.md:
  - Add notifier-cron entry under OpenClaw cron (schedule: every 2h UTC, payload description, log file)
  - Add git-janitor-cron entry (schedule: every 6h UTC, description)
  - Add archiver-manager-cron entry (schedule: weekly Sunday 02:00 UTC, description)
  - Update System Cron section: correct gateway-watchdog schedule to hourly and add `@reboot` agent startup hook
  - Ensure all entries follow existing format and style
- [ ] Preserve alphabetical/logical ordering (jobs appear roughly by frequency or purpose)

---

## Phase 3: Validation

- [ ] Run `./quick validate` to ensure workspace hygiene
- [ ] Check CRON_JOBS.md file size (reasonable)
- [ ] Verify no temporary files created
- [ ] Ensure active-tasks.md entry for this workspace-builder is marked running (added at start)

---

## Phase 4: Commit & Push

- [ ] Stage modified CRON_JOBS.md (and any other changed files if applicable)
- [ ] Commit with prefix `build:` and concise message (e.g., "build: sync CRON_JOBS.md with actual cron jobs; add missing entries; correct gateway-watchdog schedule")
- [ ] Push to origin
- [ ] Update active-tasks.md: status `validated` with verification notes

---

## Risks & Mitigations

- Low risk: Documentation only; no functional changes to cron jobs.
- Ensure added job details (schedules, descriptions) are accurate by cross-referencing `openclaw cron list` output.

---

## Success Criteria

- CRON_JOBS.md includes all currently registered cron jobs (OpenClaw + system cron)
- All schedules and descriptions match the actual system configuration
- Documentation is clear and consistent
- Commit pushed; active-tasks updated
