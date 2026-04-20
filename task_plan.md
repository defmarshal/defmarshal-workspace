# Workspace Builder Task Plan

**Session:** workspace-builder (cron: 23dad379-21ad-4f7a-8c68-528f98203a33)
**Triggered:** 2026-02-22 21:00 UTC (next run 23:00 UTC)
**Goal:** Perform comprehensive hygiene, validation, and small improvements

## Current State Analysis

**Git status:** Clean (0 changed)
**Health:** OK (Disk 66%, Gateway healthy, Memory clean, No updates)
**Active tasks:** None running
**Idea executor:** Idle (last idea rejected)
**Cron jobs:** All green, no failures
**Logs:** aria2.log 403MB (needs rotation)
**Research Hub:** research/ and public/research/ both 25M (likely in sync)
**Content index:** Unknown freshness (last cron: 2026-02-22 22:30 UTC? Actually 05:30 Bangkok = 22:30 UTC previous day; needs check)
**Memory index:** Clean, 21/21 files indexed

## Identified Opportunities

1. **Log rotation**: aria2.log exceeds 100MB threshold; rotate proactively
2. **Content index refresh**: ensure new research reports are included if any appeared since last index update
3. **Hygiene check**: run `./quick hygiene` to catch any subtle issues
4. **Research sync verification**: confirm public/research/ matches research/ (inode counts, timestamps)
5. **Cron schedule validation**: verify schedules match CRON_JOBS.md (even though auto-validation runs, we double-check)
6. **Documentation currency**: check if MEMORY.md needs today's learnings distilled from daily log
7. **Active tasks sanity**: ensure active-tasks.md is clean and <2KB

## Plan Phases

### Phase 1: Maintenance Actions
- [ ] Rotate aria2.log using `./quick log-rotate` (or direct script)
- [ ] Regenerate content index: `./quick content-index-update`
- [ ] Run hygiene check: `./quick hygiene` and address any findings

### Phase 2: Verification
- [ ] Compare research/ vs apps/research-hub/public/research/ file counts and sizes
- [ ] Validate cron schedules: `./quick cron-schedules` (should report all match)
- [ ] Check memory status: `./quick memory-status` (should show clean)
- [ ] Verify active-tasks.md size (<2KB) and format

### Phase 3: Documentation
- [ ] Review MEMORY.md: is last updated date current? Does it include key learnings from recent runs (e.g., today's workspace-builder success patterns)?
- [ ] If needed, append a concise learning bullet with today's date

### Phase 4: Close the Loop
- [ ] Run `quick health` baseline post-maintenance
- [ ] Verify git status (expect some changes from maintenance)
- [ ] Stage, commit (with prefix 'build:' for hygiene, 'docs:' for MEMORY updates), push
- [ ] Update active-tasks.md: add entry for this session, mark validated, include verification notes
- [ ] Final health check

## Error Handling

- If log rotation fails: log error, continue; may need manual intervention
- If content index fails: capture output, abort commit until resolved
- If hygiene check finds serious issues: escalate, pause and ask user
- If git push fails: check network/auth, retry once, else abort and log
- If verification fails: do not commit; log to findings and notify

## Success Criteria

- ✅ aria2.log rotated (old archived, new empty)
- ✅ Content/INDEX.md updated with latest content
- ✅ Hygiene check passes with no critical findings
- ✅ Research sync verified (both directories in sync)
- ✅ Cron schedules validated (all match CRON_JOBS.md)
- ✅ Memory index clean
- ✅ active-tasks.md <= 2KB
- ✅ MEMORY.md updated if needed
- ✅ Git working tree clean after commit and push
- ✅ Session entry added to active-tasks.md with verification output

---
**Status:** In Progress (starting Phase 1)
