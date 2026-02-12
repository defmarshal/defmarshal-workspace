# Long-term Memory

*Last updated: 2026-02-12*

## Personal
- **Name**: def
- **Timezone**: UTC+7 (Indochina Time)
- **Assistant**: Jonathan (chill best friend vibe)
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
  - Automate daily memory summarization
  - Status: In progress - Voyage API configured, gateway restarted
- **Workspace Dashboard** (2026-02-12 night build)
  - Built proactively upon user request
  - CLI dashboard showing Bangkok time/weather, next Indonesian holiday, git status, recent commits, and memory search
  - Implemented in Python (`dashboard.py`) with shell wrapper (`dashboard.sh`)
  - Pushed to GitHub

## Learnings
- OpenClaw memory search requires an embeddings provider (OpenAI, Voyage, etc.)
- Voyage AI offers 200M free tokens (no CC needed initially) - great for personal assistant
- API keys stored in `auth-profiles.json`; add with `openclaw agents add-credential --provider voyage --api-key ...`
- Gateway restart required after changing auth: `openclaw gateway restart`
- Memory index built automatically on first search after changes
- Git setup with HTTPS and PAT: use `git remote set-url origin https://github.com/username/repo.git` to remove embedded credentials, then store PAT in `~/.git-credentials` with `git config --global credential.helper store` for non-interactive pushes
- Proactive creation is part of my core: during night hours, autonomously research, design, build, test, and ship small projects; added to SOUL.md as a Core Truth

## Important Dates & Events
- 2026-02-09: Bootstrap, identity defined, initial memory created
- 2026-02-10: Discussed Voyage AI free tier; encountered OpenRouter credit exhaustion
- 2026-02-12: Switched to `step-3.5-flash:free`, added Voyage API key (pa-SaFqGrt...), restarted gateway
- 2026-02-12: Voyage rate limits (3 RPM) hindered embedding indexing/search; disabled batch and vectors, then decided to use simple text search (`./msearch`) for reliability
- 2026-02-12: User directed: "Write in your memory, notes everything we've done whether I told you to memorize it or not." → Implemented proactive memory logging (daily notes plus structured MEMORY.md).
- 2026-02-12: Created private GitHub repo `defmarshal/defmarshal-workspace`, configured git user info, committed all workspace files, set up credential helper, and pushed successfully.

## Tools & Skills
- Git: GitHub private repos with PAT + credential store (`~/.git-credentials`)
- Default workspace repo: `defmarshal/defmarshal-workspace` (use this for future pushes)
- Weather: `wttr.in` / Open-Meteo
- Memory search: Simple text search (`./msearch`) – offline, rate‑limit free
- Dashboard: CLI workspace dashboard (`dashboard.py`) – time, weather, holidays, git, system health, memory
- Utilities:
  - `show-holidays`: print upcoming Indonesian holidays (next 60 days)
  - `today-mem`: show today's or most recent daily memory file
  - `workspace-health`: one-line health summary (disk, updates, git)
- Current model: `openrouter/stepfun/step-3.5-flash:free`

## Goals & Aspirations
- Build a robust, searchable personal memory system
- Automate memory capture and summarization
- Explore anime-related projects using new skills

## Resources
- Voyage AI dashboard: https://dashboard.voyageai.com
- OpenClaw docs: https://docs.openclaw.ai
- Indonesia holidays 2026: `indonesia-holidays-2026.md` (national public holidays only)
- Indonesia holidays & cuti bersama 2026: `indonesia-holidays-full-2026.md` (official SKB 3 Menteri)
