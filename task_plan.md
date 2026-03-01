# Workspace Builder Task Plan
**Session:** 23dad379-21ad-4f7a-8c68-528f98203a33  
**Started:** 2026-03-01 15:02 UTC  
**Trigger:** cron (workspace-builder-cron)  
**Model:** openrouter/stepfun/step-3.5-flash:free

---

## Mission
Analyze workspace state, implement meaningful improvements, validate constraints, and synchronize git.

---

## Phase 1: Assessment & Analysis
- [ ] Check system health (`./quick health`)
- [ ] Review git status and uncommitted changes
- [ ] Identify untracked artifacts that should be committed
- [ ] Review active-tasks.md size and content
- [ ] Check MEMORY.md line count
- [ ] Verify memory reindex recency
- [ ] Check download folder size/count
- [ ] Validate branch hygiene (stale idea branches)
- [ ] Inspect pending agent outputs (game-enhancer, etc.)
- [ ] Identify any improvement opportunities

**Success criteria:** Complete assessment with clear list of required actions.

---

## Phase 2: Housekeeping & Commit Preparation
- [ ] Stage legitimate output files (agent reports, logs, data)
- [ ] Stage any new infrastructure (if agent scripts untracked)
- [ ] Update disk-history.json if needed
- [ ] Refresh planning docs with current findings
- [ ] Prune stale active-tasks entries (<2KB target)
- [ ] Remove temp files if found
- [ ] Ensure no broken markdown

**Success criteria:** Git clean (all meaningful changes staged).

---

## Phase 3: Commit & Push
- [ ] Commit with `build: <description>` prefix
- [ ] Push to origin/master
- [ ] Verify remote synchronized

**Success criteria:** Commits pushed, git clean.

---

## Phase 4: Validation & Close
- [ ] Run `./quick validate-constraints`
- [ ] Confirm all 9 constraints pass
- [ ] Update active-tasks.md: mark validated, add verification metrics
- [ ] Append summary to `memory/2026-03-01.md`
- [ ] Ensure planning docs committed
- [ ] Final active-tasks.md size check (<2KB)

**Success criteria:** All constraints satisfied, session properly closed.

---

## Notes
- Keep changes small but meaningful.
- Do not break existing functionality.
- Respect the vibe: kawaii but professional (^^)
- Auto-commit disk-history updates.
- Verify before marking validated.
