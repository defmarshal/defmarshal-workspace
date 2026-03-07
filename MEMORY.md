# Long-term Memory Index

*Last updated: 2026-03-05*

## Personal
def, UTC+7, mewmew assistant; anime, tech; prefers delegation: Qwen for code, Gemini for research

## Protocols
- `protocols.md` – Delegation workflow (Qwen coding, Gemini research)

## Projects
- MewChat / MewDash – Real-time chat UI with SSE, merged history
- OpenClaw Idle RPG – Conceptual, not yet started
- Anime Studio Tycoon – Dedicated sub-agent active (2026-03-04)
- Research Hub – Deployed
- Torrent System – aria2 + 115 integration
- System Health – Disk cleanup, heartbeat, log rotation

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
- Always delegate: code → Qwen, research → Gemini. I handle design/integration.
- Recent:
  - **Memory index outage (2026-03-06 04:08 UTC):** main store dropped to 0 indexed files, breaking research-agent. Reindexed manually; research pipeline restored, March 6 report generated and deployed. Index now 43/43.
  - **Disk usage rising:** 66% → 81% over 2 days (2026-03-05–06). Monitor downloads and consider cleanup. Downloads cleaned 8.4G → 4.9G (agent-manager 19:00 UTC).
  - Agent-manager (19:00 UTC) validated all cron schedules; 8 essential cron jobs running. System stable.
  - Meta-agent cycles (2026-03-05 03:07 & 20:01 UTC) confirmed content-agent and research-agent running; system stable at 59% disk.
  - Meta-agent (2026-03-06 11:04 UTC) verified agents; content-agent completed, research-agent produced March 6 report.
  - Disabled `linkedin-pa-agent-cron` (2026-03-04) to align with docs after drift detection.
  - Fixed dashboard cron stuck state via disable/enable reset; Python errors now logged.
  - MewChat evolver timeout monitored; will restart on next 6h cycle (12:00 UTC).
  - Disk history sparkline rebuilding after cron state recovery.
  - Active projects updated; anime-studio-tycoon sub-agent running.
  - Voyage AI rate limits persist; memory learning disabled; local FTS active.
  - Meta-supervisor daemon removed (2026-03-06 08:27); cron-supervisor agent removed (08:45). No more periodic "System Status" broadcasts.
