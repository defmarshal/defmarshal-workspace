# Task Plan — Strategic Workspace Builder

**Session:** workspace-builder-23dad379
**Time:** 2026-02-28 23:01 UTC
**Mode:** Autonomous maintenance with human‑grade validation

---

## Phase 1: Preliminary Hygiene & Assessment

**Goal:** Establish clean baseline, understand current state.

### Step 1.1 — Capture System Snapshot
- Run `./quick health` to get current health summary
- Run `./quick validate-constraints` to check all constraints
- Run `git status --short` to see pending changes
- Run `./quick agents` to confirm no conflicting agents

**Expected:** Baseline metrics recorded; constraints green (except git dirty)

### Step 1.2 — Stage Pending Changes
- Stage `memory/disk-history.json` (telemetry)
- Run `git status` to confirm staged

**Expected:** 1 file staged, ready for commit

---

## Phase 2: Deep Cleanup & Maintenance

**Goal:** Proactive cleanup to prevent resource issues.

### Step 2.1 — Stale Branch Pruning
- List branches: `git branch -a | grep 'idea/'`
- Identify branches older than 30 days (use `git log -1 --format=%ct <branch>`)
- Delete stale branches locally: `git branch -d <branch>`
- Delete stale remote branches: `git push origin --delete <branch>`

**Constraint:** Only delete if branch >30d old and fully merged; if unmerged, note in progress.md and skip with reason

**Expected:** Reduced clutter; prevent branch accumulation

### Step 2.2 — Downloads Folder Review
- Count downloads: `ls -1 downloads/ | wc -l`
- Total size: `du -sh downloads/`
- If count > 25 or size > 10GB, consider cleanup
- Review `quick cleanup-downloads` policy (retains 30 days by default)
- If thresholds exceeded, run dry‑run: `./quick cleanup-downloads --dry-run` and log findings
- If significant space can be freed, run `./quick cleanup-downloads --execute`

**Expected:** Disk usage stayed under control; cleanup if needed

### Step 2.3 — Active Tasks Pruning (if needed)
- Check `active-tasks.md` size: `wc -c < active-tasks.md`
- If >1800 bytes, archive old validated entries to daily log and prune
- Ensure size <2KB after operations

**Expected:** active-tasks.md remains under 2KB

---

## Phase 3: Documentation & Memory Health

**Goal:** Keep documentation crisp and up‑to‑date.

### Step 3.1 — Memory Index Check
- Verify memory reindex freshness (today already OK)
- Run `quick memory-status` to confirm no dirty stores
- If dirty >1 day, run `quick memory-index` and wait for completion

**Expected:** Memory healthy and searchable

### Step 3.2 — MEMORY.md Line Count
- Count lines: `wc -l < MEMORY.md`
- If >30 lines, review for outdated entries; condense or remove
- Keep only index pointers (files, projects, notes); no raw logs

**Expected:** MEMORY.md ≤30 lines

### Step 3.3 — Daily Log Finalization
- Review memory/2026-02-28.md for completeness
- Add any missing notable events (if warranted) — but keep concise
- Ensure proper markdown formatting

**Expected:** Daily log complete and accurate

---

## Phase 4: Final Validation & Commit

**Goal:** Ensure all constraints satisfied and push changes.

### Step 4.1 — Run Full Validation Suite
- `./quick validate-constraints` — expect all ✅
- `./quick health` — expect green (disk warning OK if <85%)
- `./quick verify` — comprehensive check (if available)

**Expected:** All systems green

### Step 4.2 — Commit Changes
- If git dirty (uncommitted staged or unstaged build changes), commit with prefix `build: `
- Commit message format: `build: <description>` (e.g., "track disk-history.json, prune stale idea branches, cleanup downloads")
- Push to origin: `git push origin master`

**Expected:** Git clean, remote updated

### Step 4.3 — Update active-tasks.md
- Find current running entry: `[workspace-builder-23dad379]`
- Update status to `validated`
- Add verification block with outputs:
  ```
  - Verification: active-tasks <2KB, MEMORY.md ≤30, health green, reindex fresh, git clean & pushed, [any specific actions taken]
  ```
- Optionally archive to daily log if extensive changes

**Expected:** active-tasks entry closed properly

### Step 4.4 — Push Active Tasks Update
- `git add active-tasks.md`
- `git commit -m "build: workspace‑builder validation close‑the‑loop"`
- `git push origin master`

**Expected:** All documentation up to date

---

## Error Handling & Iteration

**If any step fails:**
1. Log the error in progress.md with timestamp
2. Attempt recovery or skip with documented reason
3. Re‑run validation before proceeding
4. Do not commit until constraints satisfied

**Phase fallback:**
- If Phase 2 fails (e.g., branch deletion issues), document and continue
- If validation fails repeatedly, abort and flag for manual review

---

## Success Checklist

- [ ] Phase 1: Baseline captured, pending file staged
- [ ] Phase 2: Stale branches reviewed/pruned; downloads within thresholds; active-tasks <2KB
- [ ] Phase 3: Memory healthy, MEMORY.md ≤30, daily log complete
- [ ] Phase 4: All constraints ✅, git clean & pushed, active-tasks validated entry
- [ ] No temp files, no broken markdown, no uncommitted build artifacts

---

**Plan prepared:** 2026-02-28 23:01 UTC
**Ready for execution:** Yes
