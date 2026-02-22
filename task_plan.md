# Workspace Builder Plan - 2026-02-22 23:00 UTC

**Session:** workspace-builder (cron:23dad379-21ad-4f7a-8c68-528f98203a33)
**Model:** openrouter/stepfun/step-3.5-flash:free

---

## Mission

Analyze workspace state (files, MEMORY.md, active-tasks.md, git, cron) and implement meaningful improvements. Keep changes small but valuable.

---

## Analysis Phase

**Tasks:**
1. Review active-tasks.md for conflicts
2. Check system health (`quick health`)
3. Check memory status (`quick memory-status`)
4. Check cron job health (`quick cron-status`)
5. Identify stale git branches (`git branch -a | grep idea/`)
6. Review MEMORY.md for required updates
7. Check for temp files/artifacts (agents/ideas logs, etc.)
8. Verify daily logs completeness

**Expected outcome:** Complete picture of workspace health and improvement opportunities.

---

## Implementation Phase

**Tasks:**
1. Delete stale idea branches (if any):
   - idea/add-a-new-quick-utility (executed, rejected)
   - idea/create-an-agent-that-autonomously (executed, rejected)
   - idea/write-a-rudra-safe-fix-pattern (executed, rejected)
2. Update MEMORY.md with key learnings from Feb 21-22:
   - Idea generator/executor pipeline
   - Meta-agent robustness (find vs ls)
   - Research Hub deployment pitfalls
   - Capability evolver first cycle insights
   - Polyglot TTS architecture
3. (Optional) Add note about executor branch cleanup pattern to lessons.md if needed

**Constraints:**
- Keep MEMORY.md under ~30 lines (index only)
- active-tasks.md remains <2KB
- No temp files left behind

---

## Validation Phase

**Tasks:**
1. Run `quick health` - all OK?
2. Verify git status clean (0 changed)
3. Check active-tasks.md size (<2KB)
4. Confirm no temp files (e.g., leftover branches, temp scripts)
5. Review MEMORY.md line count and content
6. Verify branches deleted locally and remotely (if needed)

---

## Close The Loop

1. Commit changes with `build:` prefix
2. Push to origin
3. Update active-tasks.md with this session entry (status: validated)
4. Include verification notes in active-tasks.md entry
5. Ensure git clean after commit

---

## Error Handling

- If branch deletion fails, document reason and skip
- If MEMORY.md update would exceed line limit, summarize more concisely
- If any check fails, debug before proceeding (e.g., memory reindex if dirty)

---

## Timeline

Target completion: within 30 minutes (before next builder run at 01:00 UTC)
