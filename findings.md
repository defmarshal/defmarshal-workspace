# Workspace Builder Findings

**Assessment Date:** 2026-02-19 15:00 UTC  
**Evaluator:** workspace-builder (coid: 23dad379-21ad-4f7a-8c68-528f98203a33)

---

## System Overview

- **OpenClaw Gateway:** Healthy, running on port 18789
- **Memory System:** 16 files, 63 chunks, clean; Voyage AI rate-limited (3 RPM), fallback active
- **Git:** 1 dirty file (`content/INDEX.md`)
- **Disk:** 43% used
- **Active Tasks:** `active-tasks.md` 1521 bytes (<2KB limit)
- **Cron Jobs:** 20 jobs documented, schedules valid
- **Security:** 1 CRITICAL finding (credentials dir writable by others)

---

## Detailed Findings

### 1. Security: Credentials Directory Permissions (CRITICAL)

**Finding:**  
`/home/ubuntu/.openclaw/credentials` mode is `775` (writable by group and others). This allows any local user to drop or modify credential files, leading to potential credential theft or misuse.

**Recommendation:**  
Set to `700` (owner-only) or at minimum `750` (owner + group, if group is trusted).

**Impact:** High — credentials could be compromised.

**Fix Command:**
```bash
chmod 700 /home/ubuntu/.openclaw/credentials
```

**Verification:**
```bash
ls -ld /home/ubuntu/.openclaw/credentials  # should show drwx------
```

---

### 2. Git Status: Uncommitted Changes

**Finding:**  
One file modified but not committed: `content/INDEX.md`. This likely contains recent content updates.

**Recommendation:**  
Commit and push to keep repository clean and backups current.

**Action:**
```bash
git add content/INDEX.md
git commit -m "build: update content index with latest entries"
git push origin master
```

---

### 3. Active Tasks Registry

**Status:** Healthy
- Size: 1521 bytes (well under 2KB limit)
- Format: Correct (sessionKey, agent-name, goal, started, status, verification)
- Entries: One validated workspace-builder entry from earlier today; no orphaned running agents

**Notes:**  
The file is properly maintained. No cleanup required at this time.

---

### 4. Cron Job Integrity

**Status:** Healthy
- All schedules match CRON_JOBS.md documentation
- No misconfigurations detected
- Recent fix (2026-02-18) corrected over-frequent hourly schedules; now all run at intended intervals

**Notes:**  
The agent-manager cron runs every 30 minutes to validate schedules; this prevents future drift.

---

### 5. Memory System Observability

**Status:** Healthy
- `quick memory-status` shows clean main store (16/16 files indexed)
- Two secondary stores (torrent-bot, cron-supervisor) show dirty=True but are benign (unused)
- `memory-dirty` command exists for visibility
- Reindex is deferred due to Voyage rate limits (correct behavior)

**Notes:**  
Documentation in TOOLS.md is up-to-date. No action needed.

---

### 6. Recent Learnings (Already Documented)

The workspace-builder run from earlier today documented:
- Token optimization experiment and automatic revert
- Lesson: aggressive token caps break output; use gentle constraints
- Comprehensive notes added to `lessons.md`

No gaps identified.

---

## Conclusion

**Priority 1:** Fix credentials directory permissions (security)
**Priority 2:** Commit pending changes (`content/INDEX.md`)
**Priority 3:** Validate system health
**Priority 4:** Update active-tasks.md with validation record

The workspace is in good overall health. The twoPriority items are quick wins that improve security and maintain repository hygiene.
