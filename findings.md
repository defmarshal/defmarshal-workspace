# Findings & Decisions

## Requirements
- The web dashboard (web-dashboard.py) currently shows time, weather, holidays, git status, system health, and recent commits.
- It lacks any display of memories from the memory system.
- The CLI dashboard (dashboard.py) already includes a "Recent memory mentions" section using `openclaw memory search`.
- Goal: Add similar memory display to web dashboard for consistency and accessibility.

## Research Findings
- CLI dashboard's `search_memory` function uses: `openclaw memory search --json --max-results <limit> <query>` and parses JSON.
- It then formats each result as "file: snippet".
- The web dashboard's `/status` endpoint returns JSON consumed by the frontend. We can add a "memory" field to that JSON.
- The existing `collect_status` function runs shell commands via `run_cmd`; we can reuse that pattern.
- The web dashboard already auto-refreshes every 60s; memory will update along with other data.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Add `get_recent_memories(limit=3)` function mirroring CLI approach | Keeps code consistent and maintainable |
| Query with string "recent" | Same as CLI; relies on openclaw-memory's semantic search to surface relevant memories (including the word "recent" in context) |
| Return list of dicts with file (basename) and snippet (first line, truncated 100 chars) | Simple structure for frontend rendering |
| Add new card in HTML with id "memory-card" | Follows existing card pattern |
| In JS, fetch `data.memory` and populate card | Minimal changes to refresh logic |

## Issues Encountered
- neural-memory context was empty (`nmem context` returned "No memories stored yet."). This is expected as the brain is new. Proceeding without this context, using MEMORY.md for historical decisions.

## Resources
- CLI dashboard: `dashboard.py` (function `search_memory`)
- Web dashboard: `web-dashboard.py` (functions `collect_status`, HTML, JS)
- OpenClaw memory CLI: `openclaw memory search --help`

## Visual/Browser Findings
N/A (no browser used)
