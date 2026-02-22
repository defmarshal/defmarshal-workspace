# Workspace Builder Task Plan

**Session:** workspace-builder (cron: 23dad379-21ad-4f7a-8c68-528f98203a33)  
**Triggered:** 2026-02-22 17:00 UTC (next run 19:00 UTC)  
**Goal:** Commit uncommitted production work and maintain workspace hygiene

## Current State Analysis

**Git status:** Dirty (3 modified, 2 untracked)
**Health:** All OK (Disk 65%, Gateway healthy, Memory clean)
**Active tasks:** None running

### Uncommitted Changes Identified

1. **Security fix** - `apps/research-hub/app/feed/route.ts` 
   - Added XML escaping for RSS feed titles/descriptions (prevents XML injection)
   - Valid improvement, production-ready

2. **New research report** - `apps/research-hub/public/research/2026-02-22-liquidity-gap-calculation-banking.md` (193 lines)
   - Comprehensive report on banking liquidity gap calculations
   - High-quality content, should be committed

3. **Documentation** - `docs/OPTION_1_PUBLISH_RESEARCH.md` (2.7KB)
   - Documents research publishing pipeline (auto-deploy, auto-tweet, newsletter, analytics)
   - Should be committed to docs

4. **Watchlist updates** - `research/watchlist-priority-gaps-2026-02-15.md` (and public copy)
   - Added new research item for the liquidity gap report
   - Must commit both copies to maintain consistency

## Plan Phases

### Phase 1: Validation & Quality Check
- [ ] Verify research report completeness (no placeholders)
- [ ] Ensure watchlist entries match report metadata
- [ ] Confirm RSS feed fix doesn't break RSS validation
- [ ] Check for any stray temp files in workspace
- [ ] Run `quick health` baseline

### Phase 2: Organization & Consistency
- [ ] Add new research to research index (`./quick content-index-update`)
- [ ] Verify Research Hub build would succeed (check imports, routing)
- [ ] Ensure documentation follows project standards
- [ ] Confirm no sensitive data in any files

### Phase 3: Commit & Push
- [ ] Stage all changes (git add)
- [ ] Commit with prefix `build:`
- [ ] Push to origin
- [ ] Verify push succeeded

### Phase 4: Close the Loop
- [ ] Run `quick health` post-commit
- [ ] Verify git status clean
- [ ] Check active-tasks.md size (<2KB)
- [ ] Update planning docs (task_plan.md, findings.md, progress.md)
- [ ] Archive any completed tasks if needed

## Error Handling

- If validation fails: log to findings.md, abort commit, notify via session
- If push fails: check network/auth, retry once, else abort and log
- If health check fails after commit: investigate immediately, may need rollback

## Success Criteria

- ✅ All uncommitted production work committed with meaningful commit message
- ✅ Git working tree clean
- ✅ Health status OK
- ✅ active-tasks.md <= 2KB
- ✅ No temp files left behind
- ✅ Changes pushed to GitHub

---
**Status:** TODO (not started)
