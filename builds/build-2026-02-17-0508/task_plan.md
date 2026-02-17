# Workspace Builder Plan

**Session**: `cron:23dad379-21ad-4f7a-8c68-528f98203a33`
**Started**: 2026-02-17 05:00 UTC
**Goal**: Implement small but meaningful improvements to workspace hygiene and automation

---

## Phase 1: Cleanup Temporary Memory Index Files

**Why**: `~/.openclaw/memory/` contains old `.tmp-*.sqlite` files from previous reindex operations. These are safe to remove and reduce clutter.

**Steps**:
- Find all `.tmp-*.sqlite` files older than 7 days
- Delete them
- Verify removal

**Success criteria**:
- No `.tmp-*.sqlite` files older than 7 days remain
- Disk space reclaimed (minimal, but principle matters)

---

## Phase 2: Schedule Weekly Agent Artifact Cleanup

**Why**: Lock files and empty plan files can accumulate. The `cleanup-agent-artifacts.sh` script exists but is not automated. Adding a cron job ensures regular maintenance.

**Steps**:
- Choose schedule: Weekly on Sunday at 06:00 Asia/Bangkok (after log-rotate at 05:00)
- Create OpenClaw cron job with `payload.kind: agentTurn` running `./quick cleanup-agent-artifacts --execute`
- Document in `CRON_JOBS.md`
- Test by running manually dry-run to verify no errors

**Success criteria**:
- Cron job added and listed
- CRON_JOBS.md updated with job entry
- Manual dry-run shows findable artifacts or clean state

---

## Phase 3: Update active-tasks.md

**Why**: Track this builder session's work and verification.

**Steps**:
- Add entry under "Current Active Tasks" with status `running`
- After completion, update entry to `validated` with verification notes

---

## Phase 4: Validation & Commit

**Steps**:
- Run `quick health` to ensure system health
- Run `quick memory-status` to confirm memory clean
- Run `openclaw cron list` to verify new job appears
- Run `./quick cleanup-agent-artifacts` dry-run manually to sanity-check
- Git commit with `build:` prefix
- Push to GitHub
- Update active-tasks.md entry with verification results

---

## Notes

- All changes small, low-risk
- No modifications to core functionality
- Respect quiet hours not needed (daytime)
