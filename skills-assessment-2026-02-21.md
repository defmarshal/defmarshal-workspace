# Skill Usefulness Assessment — 2026-02-21

**Scanned:** 20 installed skills in `skills/`

---

## 🟢 Core / Highly Useful (Keep)

| Skill | Value | Use Case |
|-------|-------|----------|
| `developer` | Essential | Code quality, debugging, architecture — used by dev-agent |
| `cli-developer` | Essential | Building CLI tools and argument parsing — complements developer |
| `planning-with-files` | Essential | Complex multi-step tasks; creates task_plan.md, findings.md, progress.md |
| `tavily` | Essential | Comprehensive web research; better than Brave for AI consumption |
| `perplexity` | Valuable | Alternative web search with citations; batch queries |
| `exa-web-search-free` | Free backup | No API key needed; good for code search |
| `gmail` | Important | Email automation (Inbox zero, welcome labels) — user has Gmail |
| `humanizer` | Useful | Remove AI markers from text; improves content quality |
| `edge-tts` | Fun | Text-to-speech with various voices; aligns with anime/kawaii vibe |
| `anime` / `anime-lookup` | Relevant | Anime info via Jikan API; user likes anime |
| `stock-analysis` | Niche | User interest in finance? Possibly useful for research |
| `self-improvement` | Meta | Captures learnings/errors; enables continuous improvement |
| `neural-memory` / `openclaw-memory` | Deprecated? | Local memory providers; currently disabled due to Voyage rate limits |
| `simple-memory-search` | Utility | Grep-based memory search fallback |
| `capability-evolver` | Active | Self-evolution agent now running every 6h UTC |
| `aria2` | System | Torrent downloads; used by torrent-bot |
| `game-cog` | Game Dev | Deep game design reasoning; useful for OpenClaw Idle RPG expansion |
| `games` / `gaming` | Generic | Game recommendations; less critical but harmless |

---

## 🟡 Redundant / Duplicate

- `anime` vs `anime-lookup` — both same description; likely install conflict. Keep one.
- `neural-memory` vs `openclaw-memory` vs `simple-memory-search` — memory system fragmentation. Currently using local SQLite FTS/grep; these may be legacy.
- `games` vs `gaming` — similar; could consolidate.

---

## 🔴 Low Value / Unclear

- `fivem-dev` — FiveM RP server engineering; unless user is into FiveM, this is unused.
- `clawaifu-selfie` — no description; likely anime-related but unclear.

---

## Recommendations

1. **Consolidate duplicates:**
   - Remove either `anime` or `anime-lookup` (keep whichever is more feature-complete).
   - Remove legacy memory skills if not in use (check which provides actual functionality).
2. **Trim niche skills:**
   - `fivem-dev` removal candidate unless user expresses interest.
3. **Prioritize review:**
   - `self-improvement` should be integrated into all agents to auto-capture learnings.
   - `capability-evolver` is now active; monitor its proposals.
4. **Documentation:**
   - Add skill usage notes to `TOOLS.md` for skills with environment-specific setup (e.g., Gmail OAuth, Tavily API key).

---

*Assessment conducted by dev-agent at 2026-02-21 15:17 UTC*
