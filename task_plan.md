# Workspace Builder Task Plan

**Session Key:** workspace-builder-20260224-0107
**Trigger:** Cron schedule (every 2h UTC)
**Timestamp:** 2026-02-24 01:07 UTC

---

## Mission

Analyze workspace health, enforce constraints, and implement meaningful improvements.

---

## Constraints

- active-tasks.md must be ≤ 2KB (2048 bytes)
- MEMORY.md must be ≤ 30 lines
- Git must be clean after validation
- No temp files
- All planning docs must be committed with `build:` prefix
- Close the loop: run `quick health`, verify changes, then commit

---

## Current State (Pre-Analysis)

- **Git status:** Clean (master up-to-date with origin)
- **Disk usage:** 68% (healthy)
- **Gateway:** Healthy
- **Memory index:** Clean, 22 files, 261 chunks, stale (7d) but acceptable (weekly reindex)
- **MEMORY.md:** 30 lines (optimal)
- **active-tasks.md:** 1857 bytes, 36 lines — ✅ <2KB
- **Stale branches:** None
- **Temp files:** None
- **CRLF warning:** One MP3 file flagged (false positive; binary file)
- **Critical bug:** `quick agent-status` fails with jq parse error due to Doctor warnings in `openclaw cron list --json` output
- **Affected commands:** agent-status, cron-runs, cron-health, cron-failures, show-cron

---

## Phase 1: Analysis & Findings

**Goal:** Document current state and identify all issues.

**Tasks:**
1.1 Check which quick commands parse `openclaw cron list --json`
1.2 Verify the JSON filtering needed (strip Doctor warnings)
1.3 Check CRLF warning source (workspace-hygiene-check.sh)
1.4 Validate active-tasks.md and MEMORY.md constraints
1.5 Check git status for any untracked/modified files
1.6 Record findings in `findings.md`

---

## Phase 2: Implementation

**Goal:** Fix the identified issues.

**Planned actions:**

2.1 **Fix JSON parsing in quick script** (critical)
   - Add `sed -n '/^{/,$p'` filter before piping to jq in all affected commands
   - Commands to fix: agent-status, cron-runs, cron-health, cron-failures
   - Also fix external script `scripts/show-cron.sh` if needed
   - Test each command after fix to ensure they work

2.2 **Address CRLF warning (false positive)**
   - Option A: Modify workspace-hygiene-check.sh to skip binary files (check file type)
   - Option B: Add binary attribute in .gitattributes for .mp3 files
   - Option C: Accept as benign warning (MP3 is binary, CRLF check not meaningful)
   - Decision: Implement Option A for robustness; skip non-text files during CRLF check

2.3 **Validate constraints**
   - active-tasks.md size remains <2KB
   - MEMORY.md remains ≤30 lines
   - If needed, prune active-tasks entries slightly to maintain buffer

2.4 **Close the loop validation**
   - Run `./quick health`, `./quick agent-status`, `./quick hygiene`
   - Verify all commands succeed
   - Ensure no temp files, git clean

---

## Phase 3: Finalization

**Actions:**
3.1 Create/update progress.md throughout
3.2 Commit all changes with `build:` prefix
3.3 Update active-tasks.md with validated entry for this session
3.4 Push to origin
3.5 Final verification

---

## Success Criteria

- `quick agent-status` displays cron job table without error
- `quick hygiene` passes without CRLF false positive warnings
- active-tasks.md ≤ 2KB, MEMORY.md ≤ 30 lines
- All validation checks pass
- Commits pushed, active-tasks updated

---

**Plan created:** 2026-02-24 01:15 UTC
**Estimated duration:** 10-15 minutes
