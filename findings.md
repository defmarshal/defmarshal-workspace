# Findings & Decisions

## Requirements
- Enhance monitoring of openclaw-memory system
- Integrate memory health metrics into existing health check (workspace-health)
- Integrate memory system stats into CLI dashboard (dashboard.py)
- Keep changes small and focused

## Research Findings
- `openclaw memory status --json` returns structured status: provider, model, files, chunks, dirty, cache, fts, vector, batch, dbPath, workspaceDir
- `openclaw memory search` used for recent memories
- workspace-health is a Python script outputting a one-line summary
- CLI dashboard already shows system metrics (disk, load, memory RAM, git, updates, holidays, recent memory)
- Web dashboard already shows memory stats line: "Files: X, Chunks: Y, Dirty: Z · Provider"
- Memory stats script (`memory-stats`) exists and formats the JSON nicely; can reuse its logic

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Modify workspace-health to append memory metrics | Centralized health; used in cron alerts |
| Show in workspace-health: "Memory: <files> files, <chunks> chunks (<dirty>), provider: <provider>" | Concise, informative |
| Modify dashboard.py to add a stats line before recent memories | Parity with web dashboard, quick glance |
| Use same style in dashboard: "X files, Y chunks (dirty/clean) · provider" | Consistency |
| Handle errors gracefully: show "unavailable" or "error" if memory command fails | Robustness |

## Issues Encountered
| Issue | Resolution |
|-------|------------|

## Resources
- openclaw memory CLI: `/home/ubuntu/.npm-global/bin/openclaw`
- Workspace health: `/home/ubuntu/.openclaw/workspace/workspace-health`
- CLI dashboard: `/home/ubuntu/.openclaw/workspace/dashboard.py`
- Web dashboard reference: `/home/ubuntu/.openclaw/workspace/web-dashboard.py` (get_memory_stats function)

## Visual/Browser Findings
N/A

---
*Update after every 2 view/browser/search operations*
*This prevents visual information from being lost*
