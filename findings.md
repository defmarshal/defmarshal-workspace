# Findings: Memory System Enhancement Design

**Date**: 2026-02-15
**Phase**: Phase 2 - Design
**Status**: complete

## Current State Analysis

The openclaw-memory system is operational:
- 5 memory files indexed (all in `memory/` directory)
- 39 chunks created from those files
- Dirty flag: true (recent changes not yet indexed)
- Cache: 138 entries (enabled)
- Full-text search (FTS): available and enabled
- Vector search: disabled (due to Voyage rate limits)
- Database: `~/.openclaw/memory/main.sqlite`

## Identified Gaps

1. **Visibility**: `quick mem` and `quick search` work, but there's no dedicated command to show memory system health and stats.
2. **Dashboard**: Web dashboard shows recent memory snippets but doesn't show indexing status, file count, or whether memory is up-to-date (dirty flag).
3. **Management**: No easy way to see if memory needs reindexing or check cache size.

## Proposed Enhancements (Small & Meaningful)

### 1. Add `quick memory-stats` command
- Reads JSON from `openclaw memory status`
- Displays: files indexed, chunks, dirty status, cache entries, FTS status
- Human-readable format with color codes (if terminal)
- Also supports `--json` flag for scripting

### 2. Enhance Web Dashboard Memory Card
- Current: shows 3 recent memory snippets
- Add: stats line below title: "Indexed: 5 files, 39 chunks (dirty: yes/no)"
- Keep layout clean and consistent with other cards

### 3. Document new commands in README/quick help
- Update `quick help` output to include `memory-stats`
- Add brief description in MEMORY.md under Tools & Skills

## Implementation Plan

- Create `memory-stats` executable script (Python or bash) in workspace root
- Modify `quick` launcher to add `memory-stats` case
- Update `web-dashboard.py` to fetch memory status and include in HTML
- Update HTML template to show stats in memory card
- Test locally with `quick memory-stats` and web dashboard
- Validate with `quick health`, `git status`
- Commit and push

## Rationale

These improvements provide better visibility into the memory system without changing its core behavior. Users can quickly check if memory is indexed or if reindexing is needed. The web dashboard becomes more informative. All changes are additive and backward-compatible.

## Risks & Mitigations

- Risk: `openclaw memory status` output format may change. Mitigation: Use stable JSON output (--json) which is less likely to break.
- Risk: Voyage rate limits could be hit if we trigger indexing. Mitigation: We only read status, not modify index.
- Risk: Web dashboard error handling if memory status fails. Mitigation: Graceful fallback to "unavailable" message.

## Alternatives Considered

- Adding a memory pruning command: Too complex for now; requires careful curation. Defer to future.
- Automatic reindexing on dirty: Could cause rate limit issues; better to let user decide via `quick memory-index`.
- Full memory admin panel: Too heavy; keep it simple.

## Next Steps

- Move to Phase 3: Implementation
- Create `memory-stats` script
- Update `quick` launcher
- Update web-dashboard.py and HTML
- Test and validate
