# Long-term Memory Index

*Last updated: 2026-02-23*

## Personal
def, UTC+7, mewmew assistant; anime, tech

## Projects
Memory System, Workspace Health & Automation, Idea pipeline, openclaw-idle-rpg, Research Hub, Torrent System

## Links
- `active-tasks.md` (current work)
- `memory/YYYY-MM-DD.md` (daily logs)
- `lessons.md` (patterns)
- `TOOLS.md` (config)
- `CRON_JOBS.md` (schedules)

## Resources
- Voyage AI: https://dashboard.voyageai.com
- OpenClaw: https://docs.openclaw.ai
- GitHub: defmarshal/defmarshal-workspace

## Notes
- Gateway: port 18789; Memory: local FTS+ only (Voyage disabled); systemd linger recommended: `sudo loginctl enable-linger ubuntu`

## Learnings (latest)
- 2026-02-23: Idea generator overhaul: slug deduplication, substantive file creation via single-line `printf`, executor validation now reliable (tested success).
- 2026-02-23: Notifier agent fixed: defined `log()` function, filtered OpenClaw CLI JSON warnings; executor bug: heredoc caused hang, replaced with `printf`.
- 2026-02-22: Autonomous idea pipeline: generator (6h UTC) proposes, executor (2h UTC) implements; validation rejects placeholder commits (≥5 lines, substantive changes).
- 2026-02-21: Meta-agent robustness (find vs ls with set -euo pipefail), Research Hub Vercel deployment (server reads public/), polyglot TTS (Kokoro + Edge, 96.7% coverage), capability evolver skills-assessment outcomes.
- 2026-02-20: Earlier patterns archived in `lessons.md`
