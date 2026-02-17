# Workspace Builder Plan — 2026-02-17 17:00 UTC

## Mission
Analyze the workspace and implement meaningful improvements aligned with long-term objectives: reliability, performance, and maintainability.

## Context (from nmem_context & current state)
- Disk usage: 79% (monitor, but acceptable)
- Memory: main clean, but reindex for torrent-bot failed due to Voyage rate limits (429)
- Supervisor-cron reports error; likely self-alert due to job state, but underlying cause may be transient
- Voyage rate limits (3 RPM) are a known pain point, especially during batch operations like reindex
- Lessons.md explicitly recommends fallback to grep-based search (`./msearch`) when Voyage is rate-limited
- Fallback script `msearch` does **not exist** yet
- `quick search` relies solely on Voyage; failures result in no output or errors
- Meta-agent running successfully; triggered memory reindex which hit rate limit but continued

## Goal
Implement a robust fallback for memory search to ensure availability when Voyage AI rate limits are encountered.

## Success Criteria
- `msearch` script created and executable
- `quick search` automatically falls back to `msearch` when `openclaw memory search` fails (non-zero exit)
- Fallback produces human-readable output similar to normal search (filename: snippet)
- Works in both interactive and `--json` modes (fallback outputs plain text even in JSON mode; acceptable degradation)
- All changes committed with prefix `build:`
- No leftover temp files; git clean
- `./quick health` passes
- Manual tests: `./quick search "memory"` returns results; `./msearch "test"` works

## Task Plan (Phases)

### Phase 1: Create fallback search script (msearch)
- Write `msearch` bash script that:
  - Accepts a query string (all args combined)
  - Searches within memory/*.md, MEMORY.md, lessons.md, projects.md, active-tasks.md
  - Outputs up to 20 matches in format: `filename: matching line`
  - Handles empty query gracefully
- Place in workspace root, chmod +x

### Phase 2: Modify quick launcher search command
- Update the `search)` case in `quick` to:
  - Attempt Voyage search first
  - If Voyage command exits non-zero, emit warning to stderr and run `./msearch "$query"`
  - For interactive output (no `--json` and terminal attached): produce human-friendly lines (either from Voyage+ jq or from msearch directly)
  - For JSON/pipe mode: if Voyage fails, fallback to msearch plain text (documented as fallback)
- Ensure existing behavior unchanged when Voyage works

### Phase 3: Document fallback in TOOLS.md
- Add a note under "Memory" or "Quick Launcher Commands" explaining:
  - The `quick search` command now has a fallback to `msearch` when Voyage is rate-limited
  - `msearch` is a simple grep-based searcher over core memory files
  - This ensures reliability even during high load

### Phase 4: Testing & Validation
- Run `./quick health` to verify system health
- Manually test `./quick search "memory"` (interactive)
- Test `./quick search "memory" --json` (should output JSON normally; fallback only if Voyage fails)
- Test `./msearch "memory"` directly
- Ensure no new warnings from `./quick validate` (optional)
- Check that all files are properly formatted (no CRLF, executable bit set on msearch)

### Phase 5: Commit & Push
- Stage changes: msearch (new), quick (modified), TOOLS.md (modified)
- Commit with message: `build: add msearch fallback for memory search; integrate into quick search; update docs`
- Push to GitHub
- Update active-tasks.md: add entry for this builder (if desired) and mark as validated with verification results

## Dependencies & Risks
- None external
- Risk: modifying quick script could break existing commands. Mitigation: careful editing, preserve all other cases.
- Risk: fallback output format mismatch for scripts expecting JSON. Mitigation: fallback only on failure; document degradation.

## Notes
- This is a targeted improvement addressing a known vulnerability (rate limits).
- Keeps changes small and focused.
