# Workspace Builder Task Plan

**Session:** workspace-builder-20260224-0505
**Goal:** Analyze workspace, implement meaningful improvements, validate, and commit

---

## Phase 1: State Analysis & Health Check

- Run `./quick health` and review all metrics
- Check git status for uncommitted changes
- Verify active-tasks.md size constraint (≤2KB)
- Verify MEMORY.md line constraint (≤30 lines)
- Review recent daily logs (today + yesterday)
- Check for stale idea branches
- Check for orphaned agent artifacts

## Phase 2: Identify Improvement Opportunities

Based on state analysis, select 1-3 meaningful improvements:
- Document gaps or outdated info
- Script robustness issues
- Automation enhancements
- Documentation cleanup
- New quick commands (if needed)
- Memory system optimization

## Phase 3: Implementation

For each improvement:
- Make surgical, well-tested changes
- Update related documentation
- Log progress in `progress.md`

## Phase 4: Validation & Close the Loop

- Run `./quick health` → must be OK
- Test affected commands
- Verify no temp files left behind
- Confirm active-tasks.md <2KB and MEMORY.md ≤30 lines
- Ensure git clean after final push

## Phase 5: Commit & Document

- Commit all changes with `build:` prefix
- Push to origin
- Update active-tasks.md with validated entry
- Archive findings in `findings.md`

---

**Constraints:**
- Changes small but meaningful
- Never leave uncommitted production changes
- Keep markdown files pristine
