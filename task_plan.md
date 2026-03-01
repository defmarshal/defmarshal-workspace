# Task Plan — Strategic Workspace Builder

**Session:** workspace-builder-20260301-0111
**Time:** 2026-03-01 01:11 UTC
**Mode:** Routine maintenance with strategic improvements

---

## Phase 1: Assessment & Baseline

**Goal:** Capture current state, identify immediate needs.

### Step 1.1 — System Health Snapshot
- Run `./quick health` — note disk warnings, updates, memory status
- Run `./quick validate-constraints` — confirm all green
- Run `git status` — check for any pending changes
- Run `./quick agents` — verify no conflicting agents

**Expected:** Baseline captured; constraints green; git clean

### Step 1.2 — Workspace Analysis
- Check `active-tasks.md` size (`wc -c`) — must be <2KB
- Check `MEMORY.md` line count (`wc -l`) — must be ≤35
- Check memory index health: `quick memory-status`
- Count downloads: `ls downloads/ | wc -l`; size: `du -sh downloads/`
- Check for untracked files: `git status --porcelain`
- List idea branches: `git branch -a | grep 'idea/'` for stale branch check
- Review recent daily logs: `memory/2026-02-28.md` completeness

**Expected:** Clear picture of workspace health and any action items

---

## Phase 2: Strategic Cleanup (If Needed)

**Goal:** Prevent resource issues, maintain hygiene.

### Step 2.1 — Downloads Cleanup (Qualified)
- If downloads count >25 OR size >10GB:
  - Run dry‑run: `./quick cleanup-downloads --dry-run --verbose`
  - Analyze output: if >5 files OR >1GB removable, proceed to execute
  - Execute: `./quick cleanup-downloads --execute --verbose`
- Else: skip, monitor next cycle

**Constraint:** Respect retention policy (default 30 days). No manual deletions outside tool.

**Expected:** Disk pressure relieved; downloads within thresholds

### Step 2.2 — Stale Branch Hygiene
- For each `idea/*` branch:
  - Check age: `git log -1 --format=%ct <branch>` (convert to days)
  - If >30 days old AND fully merged (check with `git branch --merged`), delete:
    - `git branch -d <branch>`
    - `git push origin --delete <branch>` (if present)
- If unmerged or uncertain, skip and note in progress.md

**Expected:** No stale idea branches; branch list clean

### Step 2.3 — Track Valuable Artifacts
- Scan for untracked files that are not temp/cache (e.g., research reports in `research/`, scripts in `scripts/`, planning docs)
- If found, stage them: `git add <paths>`
- Verify with `git status --cached`

**Expected:** All substantive artifacts tracked

---

## Phase 3: Documentation & Memory

**Goal:** Keep documentation current and memory healthy.

### Step 3.1 — Daily Log Finalization (Feb 28)
- Open `memory/2026-02-28.md`
- Ensure it has a proper header and chronological entries
- Add a closing note summarizing the day's health and any notable events (keep concise)
- Check formatting (valid markdown)

**Expected:** Completed daily log for archive

### Step 3.2 — Create Today's Log (Mar 1)
- Create `memory/2026-03-01.md` with header:
  ```markdown
  # 2026-03-01 — Daily Log

  ## Cron & Supervisor Activity

  ## System Status

  ## Active Agents

  ## Notes
  ```
- Add initial entry: workspace builder started at 01:11 UTC

**Expected:** Today's log initialized

### Step 3.3 — MEMORY.md Line Count Check
- Count lines: `wc -l < MEMORY.md`
- If >30 lines, review and condense: remove outdated entries, keep index pointers only
- Ensure MEMORY.md points to detailed files, no raw logs

**Expected:** MEMORY.md ≤30 lines

---

## Phase 4: Validation & Commit

**Goal:** Ensure all constraints satisfied and push changes.

### Step 4.1 — Full Validation Suite
- Run `./quick validate-constraints` — expect all ✅
- Run `./quick health` — expect green (disk warning OK if <85%)
- Run `./quick verify` if available — comprehensive check

**Expected:** All systems green

### Step 4.2 — Commit Build Changes
- If git dirty (staged or unstaged build-related changes), commit with prefix `build: `
- Commit message format: `build: <summary>` (e.g., "cleanup downloads, prune branches, initialize daily log")
- Push to origin: `git push origin master`

**Expected:** Remote up to date

### Step 4.3 — active‑tasks Registry Update
- Find or add entry: `[workspace-builder-20260301-0111]`
- Status: `running` initially; after completion change to `validated`
- Add verification block:
  ```
  - Verification: active-tasks <2KB, MEMORY.md ≤30, health green, reindex fresh, git clean & pushed, [specific actions taken]
  ```
- Stage, commit, push

**Expected:** Registry reflects current state and verification

### Step 4.4 — Final Checks
- Verify no temp files left: `find . -maxdepth 2 -name "*.tmp" -o -name "*~"` should return nothing
- Verify markdown validity: quick scan for broken formatting in touched files
- Ensure all `git push` completed successfully

**Expected:** Clean workspace, all changes deployed

---

## Error Handling

**If validation fails:**
- Log error in `progress.md`, attempt fix
- Re‑run validation before committing
- Do not push incomplete state

**If cleanup thresholds not met:**
- Document decision to skip in `progress.md`
- Continue with other phases

**If branch deletion fails:**
- Log reason (unmerged, remote only) and continue

---

## Success Criteria (Checklist)

- [ ] Phase 1: Baseline captured, all metrics recorded
- [ ] Phase 2: Downloads cleanup (if needed), stale branches pruned, artifacts tracked
- [ ] Phase 3: Daily logs updated (Feb 28 closed, Mar 1 started), MEMORY.md ≤30 lines
- [ ] Phase 4: All constraints ✅, git clean & pushed, active‑tasks validated
- [ ] No temp files, no broken markdown, no uncommitted build artifacts

---

**Plan prepared:** 2026-03-01 01:11 UTC
**Ready for execution:** Yes
