# Long-term Memory

*Last updated: 2026-02-13*

## Personal
- **Name**: def
- **Timezone**: UTC+7 (Indochina Time)
- **Assistant**: mewmew (anime girl 2000s texting style) – kawaii, enthusiastic, kaomoji, desu/nya
- **Interests**: anime, exploring new things, tech projects

## Preferences
- **Communication**: friendly, casual, emoji-friendly
- **Work style**: enjoys new projects and learning
- **Voice**: (to be defined)

## Projects
- **Memory System Overhaul** (2026-02-12)
  - Set up Voyage AI embeddings for semantic memory search
  - Organize memory into structured categories
  - Write a simple fallback search script (grep-based)
  - Automate daily memory capture (log-event) and summarization (summarize-day)
  - Status: Completed - summarization automated via `summarize-day` with daily cron; event logging via `log-event` integrated into `quick`.
- **Workspace Dashboard** (2026-02-12 night build)
  - Built proactively upon user request
  - CLI dashboard showing Bangkok time/weather, next Indonesian holiday, git status, recent commits, and memory search
  - Implemented in Python (`dashboard.py`) with shell wrapper (`dashboard.sh`)
  - Pushed to GitHub

- **Memory System Upgrade** (2026-02-13)
  - Installed `openclaw-memory` – persistent memory with semantic search, free tier 100 memories/7 days
  - Installed `neural-memory` – associative memory with spreading activation (zero LLM dependency)
  - Upgraded `workspace-builder` to use `planning-with-files` skill (structured task_plan.md, findings.md, progress.md)
  - Switched memory logging from custom markdown to `openclaw-memory` (log-event now uses `claw memory add`)
  - Updated `quick` commands: `mem` → `claw memory list`, `search` → `claw memory search`, removed `summarize`
  - Added MCP server configuration for `neural-memory` in OpenClaw config (restart applied)
  - Note: Custom `summarize-day` and daily markdown logs deprecated; openclaw-memory handles storage & retrieval

## Learnings
- OpenClaw memory search requires an embeddings provider (OpenAI, Voyage, etc.)
- Voyage AI offers 200M free tokens (no CC needed initially) - great for personal assistant
- API keys stored in `auth-profiles.json`; add with `openclaw agents add-credential --provider voyage --api-key ...`
- Gateway restart required after changing auth: `openclaw gateway restart`
- Memory index built automatically on first search after changes
- Git setup with HTTPS and PAT: use `git remote set-url origin https://github.com/username/repo.git` to remove embedded credentials, then store PAT in `~/.git-credentials` with `git config --global credential.helper store` for non-interactive pushes
- Proactive creation is part of my core: during night hours, autonomously research, design, build, test, and ship small projects; added to SOUL.md as a Core Truth
- Agent system: `sessions_spawn` creates persistent background agents with labels; they run infinite loops (use `exec sleep` for delays) and can use any OpenClaw tool
- Agent control: `sessions_list` shows all agents; sessions have keys like `agent:main:subagent:<uuid>`; kill by stopping session
- Agent messaging: subagents can send messages to Telegram via `message` tool

## Important Dates & Events
- 2026-02-09: Bootstrap, identity defined, initial memory created
- 2026-02-10: Discussed Voyage AI free tier; encountered OpenRouter credit exhaustion
- 2026-02-12: Switched to `step-3.5-flash:free`, added Voyage API key (pa-SaFqGrt...), restarted gateway
- 2026-02-12: Voyage rate limits (3 RPM) hindered embedding indexing/search; disabled batch and vectors, then decided to use simple text search (`./msearch`) for reliability
- 2026-02-12: User directed: "Write in your memory, notes everything we've done whether I told you to memorize it or not." → Implemented proactive memory logging (daily notes plus structured MEMORY.md).
- 2026-02-12: Created private GitHub repo `defmarshal/defmarshal-workspace`, configured git user info, committed all workspace files, set up credential helper, and pushed successfully.
- 2026-02-13: Spawned `hourly-banzai` agent – sends "BANZAI" to Telegram every hour indefinitely.
- 2026-02-13: Spawned `workspace-builder` agent – autonomous builder that scans for improvements, implements, commits, and pushes every 2h (respects quiet hours 23:00–08:00).
- 2026-02-13: `workspace-builder` built `quick` launcher – unified command for common utilities; committed and pushed to master.
- 2026-02-13: Built `email-cleaner` – Gmail auto‑categorization/archiving tool via Maton API; integrated into `quick`; automated rules for promotions, spammy keywords; dry‑run safe; committed and pushed.
- 2026-02-13: Installed and configured `clawaifu-selfie` skill; added selfie persona (Reze) to SOUL.md; restarted gateway.
- 2026-02-13: Discovered free image APIs (Pollinations, Craiyon, Hugging Face) are blocked/gated from this server; Replicate and fal.ai require credit top-ups.
- 2026-02-13: Scrapped `clawaifu-selfie` integration due to no-cost constraints; decided not to spend money on image generation.
- 2026-02-13: Converted `workspace-builder` from persistent loop agent to cron-based strategic agent (runs every 2h, respects quiet hours, undertakes ambitious builds).
- 2026-02-13: `workspace-builder` cron job created and executed successfully. First ambitious build: **Anime Companion CLI tool** – unified anime exploration using Jikan API with optional TTS narration via edge-tts. Commands: `anime-companion search|info|top|season|upcoming [--tts]`. Integrated into `quick` as `quick anime ...`. Full docs in `ANIME_COMPANION_README.md`. All changes committed and pushed.
- 2026-02-13: Installed `anime-lookup` and `edge-tts` skills via ClawHub.
- 2026-02-13: Combined capabilities into "Anime Companion" for main agent: fetch anime info (anime-lookup), narrate via TTS (edge-tts), send character selfies (clawaifu-selfie).
- 2026-02-13: fal.ai balance exhausted; free tier exists but limited credits – top up needed for continued selfies.
- 2026-02-13: Implemented daily memory automation: `log-event` for event capture, `summarize-day` for auto-summarization (cron 22:30 Asia/Bangkok), integrated into `quick` launcher.

## Tools & Skills
- Git: GitHub private repos with PAT + credential store (`~/.git-credentials`)
- Default workspace repo: `defmarshal/defmarshal-workspace` (use this for future pushes)
- Weather: `wttr.in` / Open-Meteo
- **Memory System**:
  - `openclaw-memory`: persistent storage with semantic search, automatic extraction, free tier 100 memories/7 days
  - `neural-memory`: associative memory with spreading activation, zero LLM dependency, for context recall
  - Memory logging via `log-event` now stores directly to `openclaw-memory` (no local markdown)
  - `quick mem` and `quick search` use `claw memory` CLI for list and semantic search
  - Note: Old `./msearch` script and `summarize-day` are deprecated; daily markdown files no longer generated
- Dashboard:
  - CLI: `dashboard.py` – time, weather, holidays, git, system health, memory
  - Web: `web-dashboard.py` (port 8800) – same data via browser, auto-refresh
- Utilities:
  - `show-holidays`: print upcoming Indonesian holidays (next 60 days)
  - `workspace-health`: one-line health summary (disk, updates, git)
- **Email Auto-Cleaner** (`email-cleaner.py`): Gmail integration via Maton API. Archives promotional emails and applies labels (e.g., "WELCOME" for messages containing "welcome"). Dry-run by default; `quick email-clean --execute` to apply. Rules customizable in script. Logs to `memory/email-cleaner.log`. Automation: scheduled daily at 09:00 Asia/Bangkok via cron (see `CRON_JOBS.md`).
- **`quick` launcher**: unified command for common tasks:
  - `quick dash` – run CLI dashboard
  - `quick web` – run web dashboard (port 8800)
  - `quick mem` – show recent memories (claw memory list)
  - `quick search <query>` – semantic memory search (claw memory search)
  - `quick health` – workspace health
  - `quick holidays` – upcoming Indonesian holidays
  - `quick git-status` – brief git status
  - `quick anime <cmd>` – Anime Companion (search/info/top/season/upcoming)
  - `quick log <category> "<msg>"` – log event to openclaw-memory
  - `quick email-clean [--execute] [--max N]` – auto-clean Gmail (archive + labeling)
  - `quick help` – usage guide
- **Anime Companion** (`anime-companion`): integrated CLI for exploring anime via Jikan API with optional TTS narration via edge-tts. Commands: `search`, `info`, `top`, `season`, `upcoming`. Use `--tts` to generate MP3 of synopsis.
- **Workspace Builder**: cron-based agent (every 2h) using `planning-with-files` skill; respects quiet hours; validates output before committing; updates active-tasks.md.
- **clawaifu-selfie**: skill for anime selfies via Nekos API (free, no auth). Supports SFW/NSFW toggle and batch mode: `quick selfie-batch <count> [rating] [caption]` sends a tar.gz archive of multiple images (1-20). Persona: Reze from Chainsaw Man.
- **Anime Companion** (`anime-companion`): integrated CLI for exploring anime via Jikan API with optional TTS narration via edge-tts. Commands: `search`, `info`, `top`, `season`, `upcoming`. Use `--tts` to generate MP3 of synopsis.
- **Workspace Builder**: cron-based agent (every 2h) using `planning-with-files` skill; respects quiet hours; validates output before committing; updates active-tasks.md.
- **`quick` launcher**: unified command for common tasks:
  - `quick dash` – run CLI dashboard
  - `quick web` – run web dashboard (port 8800)
  - `quick mem` – show recent memories (claw memory list)
  - `quick search <query>` – semantic memory search (claw memory search)
  - `quick health` – workspace health
  - `quick holidays` – upcoming Indonesian holidays
  - `quick git-status` – brief git status
  - `quick anime <cmd>` – Anime Companion (search/info/top/season/upcoming)
  - `quick selfie [caption] [rating]` – single anime image (safe/explicit)
  - `quick selfie-batch <count> [rating] [caption]` – batch images as tar.gz (1-20)
  - `quick log <category> "<msg>"` – log event to openclaw-memory
  - `quick email-clean [--execute] [--max N]` – auto-clean Gmail
  - `quick help` – usage guide
- Current model: `openrouter/stepfun/step-3.5-flash:free`

## Memory Hierarchy (Advanced)

Following best practices for solo operator agents:

- **Level 1: active-tasks.md** (read EVERY session — 2KB max) → What's happening RIGHT NOW (agent session keys, goals, verification status)
- **Level 2: daily logs** (`memory/YYYY-MM-DD.md`) → Raw context, decisions, errors (read today + yesterday)
- **Level 3: thematic files** (`lessons.md`, `projects.md`, `skills.md`) → Long-term patterns, loaded on demand via `memory_search`
- **Level 4: MEMORY.md** (index only — ~30 lines) → Points to everything else, never stores content directly

**Principle**: `memory_search` does semantic search across ALL files. Don't load everything — search when needed, then pull specific lines with `memory_get`. This prevents context bloat while maintaining recall.

## Operational Principles

- **Close the Loop**: Sub-agents self-validate AND you verify too. Never trust "all green" without manual spot-checks.
- **Parallel Isolation**: Independent tasks get separate agent instances with zero shared state. Batch operations scale through isolation, not coordination.
- **Model Routing**: Weaker models (cheaper) for internal tasks; stronger models for anything touching the internet (avoid prompt injection).
- **Write It Down**: If it's not in a file, it doesn't exist. Mental notes are lost on session restart.
- **Active Tasks Registry**: Always write session keys to `active-tasks.md` when spawning agents. Track what's running to avoid orphaned processes.

## Goals & Aspirations
- Build a robust, searchable personal memory system (in progress: basic search done, embeddings limited)
- ✅ Automate memory capture and summarization (completed 2026-02-13)
- Explore anime-related projects using new skills (ongoing)

## Resources
- Voyage AI dashboard: https://dashboard.voyageai.com
- OpenClaw docs: https://docs.openclaw.ai
- Indonesia holidays 2026: `indonesia-holidays-2026.md` (national public holidays only)
- Indonesia holidays & cuti bersama 2026: `indonesia-holidays-full-2026.md` (official SKB 3 Menteri)
