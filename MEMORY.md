# Long-term Memory Index

*Last updated: 2026-02-17*

## Personal
- **Name**: def
- **Timezone**: UTC+7 (Indochina Time)
- **Assistant**: mewmew (anime girl 2000s texting style) – kawaii, enthusiastic, kaomoji, desu/nya
- **Interests**: anime, exploring new things, tech projects

## Current Projects (See projects.md for full status)
- Memory System Maintenance (Voyage AI + openclaw-memory + neural-memory)
- Workspace Health & Automation (cron agents, email cleaner, dashboard)
- Anime Companion (anime info + TTS + selfies)
- Torrent System (aria2 + nyaa integration)
- Ongoing improvements via workspace-builder

## Quick Links
- **Full history**: `MEMORY_HISTORY.md` (detailed timeline & learnings)
- **Active tasks**: `active-tasks.md`
- **Daily logs**: `memory/YYYY-MM-DD.md`
- **Lessons learned**: `lessons.md`
- **Project details**: `projects.md`
- **Tools & config**: `TOOLS.md`, `CRON_JOBS.md`

## Important Resources
- Voyage AI dashboard: https://dashboard.voyageai.com
- OpenClaw docs: https://docs.openclaw.ai
- GitHub repo: `defmarshal/defmarshal-workspace`

## Notes
- Memory search uses Voyage AI embeddings (FTS enabled). Status: `openclaw memory status`
- Gateway runs on port 18789; health: `quick health` (if quick command available)
- systemd linger recommended: `sudo loginctl enable-linger ubuntu` for service persistence
