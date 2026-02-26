# Workspace Builder Task Plan
**Session**: workspace-builder-23dad379-21ad-4f7a-8c68-528f98203a33
**Time**: 2026-02-26 23:00 UTC
**Goal**: Clean workspace, commit pending changes, enforce constraints, validate health

---

## Phase 1: Assessment & Analysis
**Objective**: Understand the current workspace state and pending changes

- [ ] Read modified files: `apps/dashboard/data.json`, `apps/dashboard/vercel.json`, `content/INDEX.md`
- [ ] Check untracked file: `apps/dashboard/.gitignore` - determine if it should be added
- [ ] Run `git status -s` and `./quick health` to establish baseline
- [ ] Review recent daily logs for context on these changes
- [ ] Document findings in `findings.md`

**Success Criteria**: Clear understanding of all modifications and their intent

---

## Phase 2: Content INDEX.md Validation & Regeneration
**Objective**: Ensure content/INDEX.md is properly synchronized with actual content files

- [ ] Compare current INDEX.md against `./quick content-index-update` output (dry-run)
- [ ] If discrepancies found, regenerate INDEX.md using `./quick content-index-update` (with commit)
- [ ] Verify INDEX.md includes all recent content items (no missing entries)

**Success Criteria**: INDEX.md accurately reflects all content files

---

## Phase 3: .gitignore Review
**Objective**: Determine if `.gitignore` should be tracked and properly configured

- [ ] Read `apps/dashboard/.gitignore` contents
- [ ] Determine if it's appropriate to track (likely yes if it contains project-specific ignores)
- [ ] If needed, add to git and ensure no sensitive info is committed

**Success Criteria**: .gitignore appropriately configured and tracked if necessary

---

## Phase 4: Commit & Push Pending Changes
**Objective**: Commit all pending changes with proper build prefix, push to origin

- [ ] Stage all modified and new files (respecting .gitignore)
- [ ] Create commit with message: `build: workspace-builder session 20260226-2300 - commit pending changes, enforce constraints`
- [ ] Push to origin: `git push origin master`
- [ ] Verify push successful, no errors

**Success Criteria**: Git clean, remote synchronized, no uncommitted changes

---

## Phase 5: Constraint Validation
**Objective**: Run comprehensive validation to ensure all workspace constraints are satisfied

- [ ] Run `./quick health` - confirm all green
- [ ] Run `./quick validate-constraints` - confirm all constraints pass
- [ ] Check `active-tasks.md` size (<2KB)
- [ ] Check `MEMORY.md` lines (≤30)
- [ ] Verify no temp files exist (e.g., *.tmp)
- [ ] Verify no stale `idea/*` branches
- [ ] Check disk usage, gateway status, memory reindex age

**Success Criteria**: All constraints satisfied; ready for documentation

---

## Phase 6: Documentation & Active Tasks Update
**Objective**: Document session outcomes and update active-tasks.md

- [ ] Add validated entry to `active-tasks.md` with:
  - Session key: `workspace-builder-23dad379`
  - Verification metrics (active-tasks size, MEM30, health green, git clean)
- [ ] Prune oldest completed entry if active-tasks.md > 2KB
- [ ] Commit `active-tasks.md` updates: `build: mark workspace-builder session validated (2026-02-26 23:00 UTC)`
- [ ] Push commit

**Success Criteria**: active-tasks.md updated, all documentation committed and pushed

---

## Phase 7: Final Verification
**Objective**: Ensure workspace is fully clean and all systems operational

- [ ] Final `git status` - must be clean
- `./quick health` - final check
- [ ] Review `findings.md` and `progress.md` completeness
- [ ] If any step failed, debug and re-run before proceeding

**Success Criteria**: No remaining issues; session complete

---

## Error Handling
- If any validation fails, pause and debug before proceeding
- Document errors in `findings.md` with remediation steps
- Do not commit if constraints not satisfied

---

**Start Time**: 2026-02-26 23:00 UTC
**Status**: Ready to execute
