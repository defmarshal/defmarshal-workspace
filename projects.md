# Projects Registry

Overview of active and completed projects. Used for context and status tracking.

## Active Projects

- **Workspace System** (2026-02-12 — present)
  - Owner: def + mewmew
  - Status: Active maintenance
  - Components: memory system, dashboard, quick launcher, email-cleaner, anime companion
  - Repo: defmarshal/defmarshal-workspace

- **Anime Companion** (2026-02-13 — present)
  - CLI tool for anime exploration via Jikan API + TTS narration
  - Skills used: anime-lookup, edge-tts
  - Commands: `anime search|info|top|season|upcoming [--tts]`
  - Status: Stable, integrated into quick

## Completed Projects

- **Memory System Overhaul** (2026-02-12)
  - Installed Voyage AI, created fallback search, automated logging & summarization
  - Status: Completed

- **Workspace Dashboard** (2026-02-12 night)
  - CLI + web dashboard with time, weather, holidays, git, memory
  - Status: Completed, proactively built

- **Email Auto-Cleaner** (2026-02-13)
  - Gmail auto-categorization/archiving via Maton API
  - Cron: daily 09:00 Asia/Bangkok
  - Status: Completed

- **Workspace Builder Agent** (2026-02-13)
  - Autonomous improvement agent using planning-with-files
  - Cron: every 2h, respects quiet hours
  - Status: Running

## Future Ideas

- Multi-agent orchestration: separate content, research, dev agents (see tweet analysis)
- Active tasks dashboard: web UI for `active-tasks.md`
- Automatic parallel spawning: when workspace-builder finds multiple independent tasks, spawn separate agents
- Lessons-triggered automation: e.g., if Voyage rate limit detected, auto-switch to grep fallback and log to `lessons.md`
