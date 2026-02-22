# Workspace Builder Task Plan

**Started**: 2026-02-22 01:00 UTC  
**Session**: cron:23dad379-21ad-4f7a-8c68-528f98203a33  
**Goal**: Clean up noise commit, improve validation, commit pending content, update docs

---

## Phase 1: Analysis & Documentation

- [x] Read active-tasks.md, SOUL.md, USER.md, recent memory
- [x] Check git status, health, memory status
- [x] Inspect untracked files and idea pipeline status
- [ ] Create findings.md with identified issues
- [ ] Create task_plan.md (this file)

**Status**: ✅ Complete

---

## Phase 2: Fix Idea Validation Logic

**Problem**: Idea executor marked "build-a-cli-game-inside" as validated despite only touching `quick` with minimal changes (≤5 lines, launcher-only). This violates quality standards.

**Actions**:
- [ ] Locate idea-executor validation code (likely `agents/idea-executor/idea-executor-cycle.sh` or related)
- [ ] Verify current validation logic
- [ ] Enhance to reject:
  - Commits with ≤5 insertions/deletions
  - Commits that only modify launcher (`quick`) without substantive source files
  - Empty commits
- [ ] Test validation on existing noise commit (should be rejected)
- [ ] Update documentation if needed

**Dependencies**: None  
**Risk**: Low (validation is safety-critical but reversible)  
**Validation**: Run idea-executor on a test idea that only touches `quick`; should be rejected

---

## Phase 3: Clean Up Stale Branch & Noise Commit

**Problem**: Branch `idea/build-a-cli-game-inside` exists with a noise commit that shouldn't have passed validation.

**Actions**:
- [ ] Delete branch locally: `git branch -D idea/build-a-cli-game-inside`
- [ ] Delete remote: `git push origin --delete idea/build-a-cli-game-inside` (if exists)
- [ ] Verify removal: `git branch -a` should not list it
- [ ] Reset any local branch tracking

**Dependencies**: Phase 2 (to prevent recurrence)  
**Risk**: Low (branch has no valuable changes)  
**Validation**: Confirm branch deleted both locally and remotely

---

## Phase 4: Commit Pending Daily Digest

**Problem**: `content/2026-02-22-daily-digest.md` is untracked. Should be committed as part of content pipeline.

**Actions**:
- [ ] Review file content to ensure it's complete and correct
- [ ] Add to git: `git add content/2026-02-22-daily-digest.md`
- [ ] Commit with `content:` prefix: `git commit -m "content: daily digest - 2026-02-22"`
- [ ] Push: `git push origin <current-branch>` (likely master)
- [ ] Verify: `git status` clean

**Dependencies**: None  
**Risk**: Very low (standard content commit)  
**Validation**: File tracked and pushed; `git status` clean

---

## Phase 5: Update Documentation & Memory

**Problem**: MEMORY.md hasn't been updated since Feb 21; active-tasks.md needs current session added.

**Actions**:
- [ ] Read MEMORY.md to understand format (index-only, ~30 lines)
- [ ] Add entry for today's learnings: "Idea validation fix", "noise commit cleanup", "daily digest pipeline monitoring"
- [ ] Keep MEMORY.md concise; link to memory/2026-02-22.md for details
- [ ] Update active-tasks.md: add this session entry with proper format, status: running → validated after completion
- [ ] Archive old entries if needed to stay under 2KB

**Dependencies**: Phases 2-4 complete  
**Risk**: Low  
**Validation**: MEMORY.md ≤30 lines, active-tasks.md ≤2KB, formatted correctly

---

## Phase 6: Close the Loop Validation

**Problem**: Ensure all changes are correct and system healthy before final commit.

**Actions**:
- [ ] Run `./quick health` — all OK?
- [ ] Run `./quick git-status` — clean?
- [ ] Verify no temp files: `find . -name "*.tmp" -o -name "*~"` (should be empty)
- [ ] Check active-tasks.md size
- [ ] Verify idea pipeline: `cat agents/ideas/latest.json` — no pending ideas with only `quick` touches?
- [ ] Review all modified files for correctness

**Dependencies**: All previous phases  
**Risk**: Low  
**Validation**: All checks pass

---

## Phase 7: Final Commit & Push

**Problem**: Changes need to be committed and pushed.

**Actions**:
- [ ] If multiple commits already exist (e.g., content digest), ensure they're pushed
- [ ] Create a summary build commit for today's builder session with prefix `build:`
- [ ] Push all commits to GitHub
- [ ] Verify: `git log --oneline -5` shows recent commits

**Dependencies**: Phase 6 passes  
**Risk**: Low  
**Validation**: Commits visible on remote

---

## Success Criteria

- ✅ Idea validation rejects noise commits (launcher-only, ≤5 changes)
- ✅ Stale branch `idea/build-a-cli-game-inside` deleted locally and remotely
- ✅ Daily digest committed and pushed
- ✅ MEMORY.md updated with today's key learnings
- ✅ active-tasks.md accurate and within size limits
- ✅ System health: all green, no temp files, git clean
- ✅ All changes pushed to GitHub

---

## Notes

- Keep changes small and focused.
- Document decisions in findings.md.
- If any step fails, debug before proceeding; update progress.md with error details.
