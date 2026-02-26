# Workspace Builder Plan
**Session:** 2026-02-26 09:10 UTC (cron:23dad379)
**Goal:** Push pending commits, cleanup stale branches, validate constraints, document session

## Current State Analysis
- Git: Ahead of origin by 6 commits (content + dev work)
- active-tasks.md: ~1900 bytes (<2KB, healthy)
- MEMORY.md: 30 lines (exactly at target)
- Stale idea branch detected: `idea/create-an-agent-that-autonomously` (appears old, needs age verification)
- No untracked files, no temp files
- System health: green (disk 70%, gateway healthy, memory clean)
- Memory reindex age: ~2.2 days (fresh; weekly cron on Sunday)
- Previous planning docs exist but will be overwritten per workflow

## Constraints to Enforce
- active-tasks.md must be ≤2KB (will add entry, so prune oldest first)
- MEMORY.md must be ≤35 lines (currently 30, safe)
- Git must be clean and up-to-date with origin after push
- No stale branches (idea/* older than threshold, typically >1 day)
- Health must be green
- All changes must be committed and pushed with 'build:' prefix

## Proposed Phases

### Phase 1: Push Pending Commits
**Why:** Synchronize local repository with remote; maintain backup and collaboration readiness.
- Step 1.1: List ahead commits: `git log origin/master..HEAD --oneline`
- Step 1.2: Push to origin: `git push origin master`
- Step 1.3: Verify: `git status` should show "up to date"
- Step 1.4: If push fails, diagnose and retry

### Phase 2: Stale Branch Cleanup
**Why:** Keep repository tidy; remove abandoned experimental branches.
- Step 2.1: List all idea branches with dates: `git for-each-ref --format='%(refname:short) %(committerdate:relative)' refs/heads/idea/`
- Step 2.2: Identify stale branches (older than ~1 day, or from old dates like "X days ago")
- Step 2.3: Delete local branches: `git branch -D <branch>`
- Step 2.4: Attempt remote deletions: `git push origin --delete <branch>` (may no-op if not remote)
- Step 2.5: Verify none remain: `git branch | grep 'idea/'`

### Phase 3: active-tasks.md Maintenance
**Why:** Add this session's entry while respecting 2KB limit.
- Step 3.1: Read current file to assess size and entries
- Step 3.2: Prune oldest completed workspace-builder entry to make room (target removal of 1-2 entries)
- Step 3.3: After validation (Phase 5), add validated entry with:
  - Session key: `workspace-builder-20260226-0910`
  - Goal, started time, verification metrics (health, size, memory lines, etc.)
- Step 3.4: Final size check: must be <2KB

### Phase 4: Planning Documentation
**Why:** Follow planning-with-files workflow for traceability and audit.
- Write `task_plan.md` (this file)
- Write `findings.md` with analysis snapshot and decisions
- Write `progress.md` with execution log (update after each phase)

### Phase 5: Close the Loop Validation
**Why:** Ensure workspace meets all constraints before marking success.
- Run `./quick health` — all metrics green
- Run `./quick validate-constraints` — all checks pass
- Check `git status` — clean and up-to-date
- Verify no temp files in workspace root
- Verify active-tasks.md size <2KB and MEMORY.md ≤35 lines
- Check no stale idea branches remain

### Phase 6: Commit and Push
**Why:** Record all changes in version control.
- Stage changes: `git add -A` (active-tasks.md, task_plan.md, findings.md, progress.md)
- Commit with message: `build: enforce constraints - push commits, cleanup branches, update active-tasks, document session (20260226-0910)`
- Push to origin: `git push origin master`
- Verify remote includes new commit

### Phase 7: Update active-tasks.md Status
- After commit and push, verify everything is clean
- This entry will already be in active-tasks.md as "validated" with verification metrics
- No further action needed if committed with metrics

## Success Criteria
✅ Remote origin up-to-date (no ahead/behind)
✅ active-tasks.md <2KB and contains this validated session entry
✅ All constraints satisfied (health, git, memory, no temp files, no stale branches)
✅ Planning docs created and committed
✅ Changes pushed to GitHub

## Risk Mitigation
- Each phase validated before proceeding to next
- If `git push` fails, check network/auth and retry once; if still fails, abort and log error
- Prune active-tasks carefully: only remove oldest completed workspace-builder entries; never remove running agents
- Keep planning docs concise (<10KB each) and focused
- If stale branch deletion fails (protected or remote-only), document and continue

## Notes
- This plan will be updated incrementally during execution
- All steps correspond to documented best practices from AGENTS.md and TOOLS.md
- The validate-constraints command will be used as the final gate
- Session key format: workspace-builder-YYYYMMDD-HHMM (UTC)
