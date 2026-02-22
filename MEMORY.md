# Long-term Memory Index

*Last updated: 2026-02-22*

## Personal
def, UTC+7, mewmew assistant; interests: anime, tech

## Projects
Memory System, Workspace Health & Automation, Anime Companion, Torrent System, Idea pipeline, openclaw-idle-rpg, research-hub

## Links
- `active-tasks.md` current work
- `memory/YYYY-MM-DD.md` daily logs
- `lessons.md` patterns
- `projects.md` status
- `TOOLS.md` config
- `CRON_JOBS.md` schedules

## Resources
- Voyage AI: https://dashboard.voyageai.com
- OpenClaw: https://docs.openclaw.ai
- GitHub: defmarshal/defmarshal-workspace

## Notes
- Memory: local FTS+ only (Voyage disabled)
- Gateway: port 18789
- systemd linger recommended: `sudo loginctl enable-linger ubuntu`

## Learnings (latest)
- 2026-02-22: Autonomous idea pipeline: generator (6h UTC) proposes, executor (2h UTC) implements; latest.json tracks state; executor validation rejects placeholder commits (≥5 lines, substantive changes).
- 2026-02-21: Meta-agent robustness (use find not ls with set -euo pipefail), Research Hub Vercel deployment (server component reads public/; project must be public), polyglot TTS (Kokoro English + Edge TTS Japanese, auto-detect via Unicode, 96.7% coverage), capability evolver skills-assessment leading to duplicate skill consolidation.
- 2026-02-19: token optimization caps break output → gentle constraints
- 2026-02-18: agent-manager auto-commit must detect untracked files; quick syntax fix; enforce task registry limits
