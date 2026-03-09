# AI Garden — Self‑Extending Research & Content Farm

**Vision:** A workspace that autonomously discovers ideas, grows them into reports/code, and delivers daily harvests — an intelligent garden that tends itself.

## Current State (2026-03-09)

### Completed ✅

- **Seed Gatherer** (`agents/seed-gatherer.py`):
  - Pulls unread emails (Maton) + RSS feeds (arXiv cs.AI, cs.CL, cs.LG, cs.SE, TechCrunch, The Verge)
  - Writes seeds to `memory/seeds.jsonl` (JSON Lines)
  - Cron: `seed-gatherer-cron` every 6 hours
  - First run: 50 seeds collected

- **Research Gardener** (`agents/research-gardener.py`):
  - Consumes seeds, performs web search (via Tavily/openclaw), generates markdown reports
  - Outputs to `research/`; updates `memory/graph.json` with seed→output edges
  - Cron: `research-gardener-cron` hourly
  - First report: `research/2026-03-09-eigendata-a-self-evolving-multi-agent-platform-fo.md`

- **Content Gardener** (`agents/content-gardener.py`):
  - Consumes seeds, generates blog posts via `openclaw agent ask`
  - Outputs to `content/`; updates graph; shares processed seeds tracking
  - Cron: `content-gardener-cron` hourly
  - First post: `content/2026-03-09-tool-genesis:-a-task-driven-tool-creation-benchmark-for-self-evolving-language-a.md`

- **Harvester** (`agents/harvester.py`):
  - Daily (06:00 UTC) creates `reports/daily-harvest-YYYY-MM-DD.md` summarizing seeds gathered and outputs produced
  - Also sends Telegram summary (CLI flag tweak pending)
  - Cron: `harvest-cron` daily

- **Knowledge Graph** (`memory/graph.json`) initialized with seed→output edges.

### In Progress 🛠️

- Telegram delivery from harvester (CLI args)
- Possibly refine gardener selection (prioritization)

### Completed ✅

- **Planner** (`agents/planner.py`):
  - Weekly analysis of tag profile; suggests new seeds for under‑represented categories
  - Cron: `planner-cron` Sundays 02:00 UTC
  - Initial suggestions: 6 seeds added (ai, space, quantum, web, infra, tech)

### Planned (Roadmap)

1. **Code Gardener** – generate small scripts/apps from seeds
2. **Refine prioritization** – better seed scoring (freshness, relevance, diversity)
3. **Full harvest Telegram** – fixed delivery (CLI flag tweak pending)


## Architecture

```
[Sources] → Seed Gatherer → seeds.jsonl
   ↓
[Queue] → Gardener Agents → outputs (research/, content/, apps/)
   ↓
[Knowledge Graph] ← links seeds/outputs/tags
   ↓
Harvester → daily Telegram summary
Planner → weekly adjustments
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

## Cron Jobs

| Name                  | Schedule | Task |
|-----------------------|----------|------|
| `seed-gatherer-cron`  | every 6h | run `agents/seed-gatherer.py` |
| *(gardener cron TBD)* | TBD      | dispatch gardener workers |
| `harvest-cron`        | daily 06:00 UTC | generate daily-harvest report |
| `planner-cron`        | weekly Sun 02:00 UTC | adjust priorities |

## How to Run Manually

```bash
cd /home/ubuntu/.openclaw/workspace
python3 agents/seed-gatherer.py
```

View seeds:

```bash
tail -5 memory/seeds.jsonl
```

## Next Immediate Tasks

- [ ] Design gardener agent loop (how to select seeds, produce outputs)
- [ ] Implement basic research-gardener using existing research-agent pattern
- [ ] Add output metadata linking back to seed ID
- [ ] Create `memory/graph.json` with seed→output edges
- [ ] Add gardener cron (runs hourly?)
- [ ] Build harvester script to produce daily summary and Telegram blast

---

*Document will be updated after each milestone.*
