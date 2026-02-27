# Workspace Builder Task Plan
**Session**: workspace-builder-20260227-0109
**Time**: 2026-02-27 01:09 UTC
**Goal**: Commit pending changes, enforce constraints, maintain active-tasks.md, validate health

---

## Phase 1: Assessment & Analysis
**Objective**: Understand current workspace state and identify violations

- [ ] Run `git status -s` and `git diff` to see modified files
- [ ] Run `./quick health` and `./quick validate-constraints` to capture baseline
- [ ] Analyze the dirty file (apps/research-hub/INDEX.md) to understand modification
- [ ] Review active-tasks.md structure: note validated entry under "Running" section (should be moved to Completed)
- [ ] Check active-tasks.md size and need for pruning
- [ ] Document findings in `findings.md`

**Success Criteria**: Clear picture of all issues and required actions

---

## Phase 2: Commit Pending Changes
**Objective**: Stage and commit the modified INDEX.md with appropriate message

- [ ] Verify change is legitimate (timestamp update for research-hub index)
- [ ] Stage file: `git add apps/research-hub/INDEX.md`
- [ ] Commit: `git commit -m "build: update research-hub index timestamp (workspace-builder session 20260227-0109)"`
- [ ] Push: `git push origin master`
- [ ] Verify push succeeded and git is clean

**Success Criteria**: Git clean, remote synchronized

---

## Phase 3: active-tasks.md Organization
**Objective**: Reorganize active-tasks.md entries and add current session

- [ ] Move validated entry `[workspace-builder-20260226-2300]` from "Running" to "Completed (recent)" section
- [ ] Add new running entry for current session with session key `workspace-builder-20260227-0109`
- [ ] Check file size: if >2KB, prune oldest completed entry (likely workspace-builder-23dad379)
- [ ] Verify active-tasks.md remains valid markdown and <2KB

**Success Criteria**: active-tasks.md properly structured, size within limit

---

## Phase 4: Constraint Validation
**Objective**: Ensure all workspace constraints are satisfied

- [ ] Run `./quick health` - must be all green
- [ ] Run `./quick validate-constraints` - must pass all checks
- [ ] Verify: active-tasks.md size <2KB, MEMORY.md ≤30 lines, no temp files, no stale branches, memory reindex age fresh

**Success Criteria**: All constraints passing

---

## Phase 5: Documentation & Final Commit
**Objective**: Commit planning docs and active-tasks updates

- [ ] Stage planning files: task_plan.md, findings.md, progress.md (once updated)
- [ ] Stage updated active-tasks.md
- [ ] Commit: `git commit -m "build: mark workspace-builder session validated (2026-02-27 01:09 UTC)"`
- [ ] Push to origin
- [ ] Verify push successful

**Success Criteria**: All documentation committed, remote up-to-date

---

## Phase 6: Final Verification
**Objective**: Confirm workspace fully clean and healthy

- [ ] Final `git status` - clean
- [ ] Final `./quick health` - green
- [ ] Final `./quick validate-constraints` - all pass
- [ ] Review progress.md completeness

**Success Criteria**: Session complete with no remaining issues

---

## Error Handling
- If validation fails at any point, debug and document in findings.md before proceeding
- Do not mark session validated until all constraints satisfied

---

**Start Time**: 2026-02-27 01:09 UTC
**Status**: Ready to execute
