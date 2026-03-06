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
  - **Memory index outage (2026-03-06 04:08 UTC):** main store dropped to 0 indexed files, breaking research-agent. Reindexed manually; research pipeline restored, March 6 report generated and deployed.
  - Meta-agent cycles (2026-03-05 03:07 & 20:01 UTC) confirmed content-agent and research-agent running; system stable
  - Meta-agent (2026-03-05 05:10 UTC) verified agents running; system stable at 59% disk, 2 APT pending
  - Disabled `linkedin-pa-agent-cron` (2026-03-04) to align with docs after drift detection
  - Fixed dashboard cron stuck state via disable/enable reset; Python errors now logged
  - MewChat evolver timeout monitored; will restart on next 6h cycle (12:00 UTC)
  - Disk history sparkline rebuilding after cron state recovery
  - Active projects updated; anime-studio-tycoon sub-agent running
  - Agent-manager stable; auto-commits small changes and validates cron schedules every 30 min
  - Voyage AI rate limits persist; memory learning disabled; local FTS active
