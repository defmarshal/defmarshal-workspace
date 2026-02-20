# Findings Report: Strategic Workspace Improvements (2026-02-20)

**Session:** workspace-builder-cron  
**Timestamp:** 2026-02-20 21:00 UTC  
**Assessor:** Strategic Workspace Builder

---

## Executive Summary

The workspace is in excellent health: all systems operational, memory clean, cron validated, git clean. However, three meaningful improvements are identified:

1. **Research Hub deployment is incomplete** due to missing exec allowlist (blocking git/gh/vercel)
2. **Build archive clutter** – 15 old planning files (76KB) serving no purpose
3. **Orphaned agent detection** – no proactive tool for stale session cleanup

These improvements will enhance deployment readiness, workspace cleanliness, and self-monitoring capability.

---

## Detailed Findings

### 1. Research Hub Deployment Blocker

**Status:**
- Next.js app scaffolded in `apps/research-hub/`
- Deployment commands (`quick vercel`, `research-hub-deploy`) exist
- **Blocker:** `exec-approvals.json` does not allow `git`, `gh`, or `vercel`

**Evidence:**
- README mentions deployment but lacks prerequisite troubleshooting
- No automated check for allowlist status
- User must manually add entries and restart gateway (referenced in daily logs)

**Impact:** High – deployment path exists but is unreachable without manual config

**Recommendation:** Add a prerequisite check command (`quick vercel-prereq`) that inspects `exec-approvals.json` and provides actionable instructions. Enhance deployment docs with clear steps.

---

### 2. Build Archive Accumulation

**Status:**
- Directory `build-archive/` contains 15 files (~80KB total)
- Files are planning docs from Feb 15-17 (task_plan, findings, progress)
- Pattern: Each workspace-builder run previously preserved these; newer runs now document only in daily logs and MEMORY.md

**Evidence:**
```bash
$ ls build-archive/
findings-2026-02-15-1100.md findings-2026-02-16-0514.md ...
progress-2026-02-15-1100.md progress-2026-02-16-0514.md ...
task_plan-2026-02-15-1100.md task_plan-2026-02-16-0514.md ...
```

**Impact:** Low-Medium – minor clutter, violates workspace minimalism principle

**Recommendation:** Compress and archive these files as a single backup tarball, then remove the directory. Ensure no references remain.

---

### 3. Missing Orphaned Agent Detection

**Status:**
- `active-tasks.md` is currently clean (no running agents)
- Past incidents (2026-02-19) showed stale entries persisting
- `agent-manager-cron` runs cleanup every 30 minutes, but manual check is useful

**Evidence:**
- Daily log entry: "Stale Active Task Cleanup" – orphaned entry required manual removal
- No standalone command to quickly inspect session health

**Impact:** Medium – orphaned sessions can indicate instability or improper cleanup

**Recommendation:** Create `scripts/check-orphaned-agents.sh` that uses `openclaw sessions list --json` to identify stale running sessions. Expose via `quick orphan-check`.

---

## System Health Baseline

| Metric | Status |
|--------|--------|
| Disk usage | 49% (healthy) |
| Git status | Clean |
| Memory index | 18f/81c (local FTS+, clean) |
| Gateway | Healthy |
| Downloads | 4.0G (14 files, all <30 days) |
| Cron jobs | 22 scheduled, all documented in CRON_JOBS.md |
| active-tasks.md | 889 bytes (<2KB) |
| Temp files | None (normal openclaw temp dirs only) |

All baseline metrics are green. No urgent issues.

---

## Scope Definition

**In Scope:**
- Research Hub deployment docs & prerequisite check
- Build archive cleanup
- Orphaned agent detection tool
- Standard validation and commit procedure

**Out of Scope:**
- Modifying exec-approvals.json (user action required)
- Changing Research Hub code structure
- Altering agent-manager cleanup logic (already exists)
- Modifying user's interest alignment (content already tech-focused)

---

## Verification Plan

### After Implementation:

1. `./quick health` → all OK
2. `quick vercel-prereq` → prints clear guidance
3. `quick orphan-check` → runs without error, exits 0
4. `build-archive/` removed, backup tarball exists
5. `git status` clean, no untracked files
6. `active-tasks.md` < 2KB
7. Commit pushed with `build:` prefix

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Broken references after build-archive removal | Low | Medium | Grep for references before removal |
| New command syntax errors | Low | Low | Test commands before final commit |
| Research Hub docs become outdated | Medium | Medium | Keep instructions generic; reference allowlist docs |
| Orphan check false positives | Low | Low | Use conservative heuristics (stale threshold >2h) |

Overall risk: **Low**

---

## Conclusion

Three focused improvements are recommended and feasible without disrupting system stability. Execution should follow standard workspace-builder workflow: implement, validate, commit, update active-tasks.
