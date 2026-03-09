# AI Garden — Self‑Extending Research & Content Farm

**Vision:** A workspace that autonomously discovers ideas, grows them into reports/code, and delivers daily harvests — an intelligent garden that tends itself.

## Current State (2026-03-09)

All core agents are complete and scheduled via cron. The garden is self-sustaining.

### Completed ✅

- **Seed Gatherer** (`agents/seed-gatherer.py`):
  - Pulls unread emails (Maton) + RSS feeds (arXiv cs.AI, cs.CL, cs.LG, cs.SE, TechCrunch, The Verge)
  - Writes seeds to `memory/seeds.jsonl` (JSON Lines)
  - Cron: `seed-gatherer-cron` every 6 hours
  - Model: OpenRouter via gateway

- **Research Gardener** (`agents/research-gardener.py`):
  - Consumes seeds, performs web search (Tavily if key set), generates markdown reports via **OpenRouter direct API** (`stepfun/step-3.5-flash:free`)
  - Outputs to `research/`; updates `memory/graph.json` with seed→output edges (type: `output`)
  - Cron: `research-gardener-cron` hourly
  - Requires `OPENROUTER_API_KEY` in `.env` (free model, rate-limited)

- **Content Gardener** (`agents/content-gardener.py`):
  - Consumes seeds, generates blog posts via direct OpenRouter call (`stepfun/step-3.5-flash:free`)
  - Outputs to `content/`; updates graph (type: `content`)
  - Cron: `content-gardener-cron` hourly

- **Code Gardener** (`agents/code-gardener.py`):
  - Consumes seeds, generates small Python scripts via OpenRouter
  - Outputs to `apps/`; updates graph (type: `app`)
  - Cron: `code-gardener-cron` hourly
  - Falls back to placeholder script if generation fails

- **Harvester** (`agents/harvester.py`):
  - Daily (06:00 UTC) creates `reports/daily-harvest-YYYY-MM-DD.md` summarizing seeds gathered and outputs produced (counts nodes of type `output`, `content` with today's date prefix)
  - Cron: `harvest-cron` daily
  - Can be run manually with `-t <dest>`

- **Planner** (`agents/planner.py`):
  - Weekly (Sun 02:00 UTC) analyzes knowledge graph tag distribution; suggests new seeds for under‑represented categories
  - Writes suggestions to `memory/planner_suggestions.jsonl` which seed-gatherer consumes
  - Cron: `planner-cron` weekly

- **Knowledge Graph** (`memory/graph.json`):
  - Nodes: seeds, outputs (research), content (blog posts), apps (scripts)
  - Edges: `seed → output/content/app` (type: `produced`)

### Technical Details

- **LLM Integration**: Bypasses gateway for reliability in cron; uses `curl` to OpenRouter API with `stepfun/step-3.5-flash:free`. Environment `OPENROUTER_API_KEY` loaded from `.env` (workspace root). Model may be rate-limited; failures fall back to placeholder content.
- **Node Identification**: Harvester determines "today's outputs" solely by filename date prefix (`YYYY-MM-DD-...`) inside `research/` and `content/`. `apps/` are not date-prefixed and are excluded from daily counts.
- **Cron Scheduling**: All jobs defined in `CRON_JOBS.md`; validated every 30 min by `agent-manager-cron`.

## Architecture

```
[Sources] → Seed Gatherer → seeds.jsonl
   ↓
[Queue] → Gardener Agents → outputs (research/, content/, apps/)
   ↓
[Knowledge Graph] ← links seeds/outputs/tags
   ↓
Harvester → daily report (reports/)
Planner → weekly suggestions (memory/planner_suggestions.jsonl)
```

## Seeds Format

```json
{
  "id": "uuid",
  "title": "Short title",
  "snippet": "Brief excerpt",
  "source": "email:someone@example.com | rss:https://...",
  "tags": ["ai", "research", "email"],
  "ts": "2026-03-09 08:52:00 UTC"
}
```

## Graph Node Types

- `seed` – original idea from gatherer/planner
- `output` – research reports (`research/`)
- `content` – blog posts (`content/`)
- `app` – scripts (`apps/`)

## Cron Jobs

| Job Name                   | Schedule       | Command |
|----------------------------|----------------|---------|
| `seed-gatherer-cron`       | every 6h       | `python3 agents/seed-gatherer.py` |
| `research-gardener-cron`   | hourly         | `python3 agents/research-gardener.py` |
| `content-gardener-cron`    | hourly         | `python3 agents/content-gardener.py` |
| `code-gardener-cron`       | hourly         | `python3 agents/code-gardener.py` |
| `harvest-cron`             | daily 06:00 UTC| `python3 agents/harvester.py -t reports/daily-harvest-$(date +%Y-%m-%d).md` |
| `planner-cron`             | weekly Sun 02:00 UTC | `python3 agents/planner.py` |
| `agent-manager-cron`       | every 30 min   | validates cron schedules against this doc |

## Environment

- `.env` must include `OPENROUTER_API_KEY` for gardeners to generate real content. Without it, they write placeholders.
- Optional: `TAVILY_API_KEY` for research-gardener to include fresh web snippets; otherwise uses OpenRouter summary.

## Manual Testing

```bash
cd /home/ubuntu/.openclaw/workspace
python3 agents/research-gardener.py   # generates one research report
python3 agents/content-gardener.py   # generates one blog post
python3 agents/code-gardener.py      # generates one script (may fallback)
python3 agents/harvester.py -t reports/test-harvest.md
```

View recent seeds:

```bash
tail -5 memory/seeds.jsonl
```

View graph:

```bash
python3 -m json.tool memory/graph.json | head -50
```

## Notes

- Free model `stepfun/step-3.5-flash:free` may hit rate limits; 429 errors are logged and fallbacks used.
- Node IDs in graph may be absolute or relative paths; harvester uses `Path(node_id).name` to extract filename for date check.
- Planner suggestions are seeds with `source: "planner"`.

