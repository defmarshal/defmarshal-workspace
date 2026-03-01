# Game Enhancer Agent

An autonomous OpenClaw agent that continuously enhances the Anime Studio Tycoon game using Qwen Code (for implementation) and Gemini CLI (for research/design).

## Description

This agent runs enhancement cycles on the game, focusing on different areas:
- **Balance**: Adjust economy, difficulty curves, upgrade costs
- **Features**: Add new mechanics (events, systems, UI)
- **Content**: New events, upgrades, items, scenarios
- **Polish**: Bug fixes, UX improvements, code quality

It uses a two-phase approach:
1. **Research** (Gemini CLI) — Analyze current state, suggest improvements, design new content
2. **Implementation** (Qwen Code) — Write actual code changes, tests, refactors

## Prerequisites

- Qwen Code installed and authenticated (`npm install -g @qwen-code/qwen-code` + `qwen auth`)
- Gemini CLI installed and authenticated (`npm install -g @google/gemini-cli` + `gemini auth`)
- Both skills available in `~/openclaw/workspace/skills/`

## Usage

```bash
# Run one enhancement cycle
./agents/game-enhancer/game-enhancer.sh --once

# Run as daemon (every 6 hours)
./agents/game-enhancer/game-enhancer.sh --daemon

# Check status/last report
./agents/game-enhancer/game-enhancer.sh --status
```

## Schedule (optional)

Register as OpenClaw cron job to run automatically:

```bash
openclaw cron add --name "game-enhancer-cron" \
  --cron "0 */6 * * *" --tz "UTC" \
  --message "Execute game enhancer: bash -c 'cd /home/ubuntu/.openclaw/workspace && ./agents/game-enhancer/game-enhancer.sh --once >> memory/game-enhancer.log 2>&1'" \
  --session isolated --no-deliver
```

## Output

- Log: `memory/game-enhancer.log`
- Latest report: `games/anime-studio-tycoon/enhancement-report-latest.md`
- State: `memory/game-enhancer-state.json`
- Code changes: automatically committed with `[game-enhancer]` prefix

## Policies

- Always use `qwen-code` for coding tasks (refactoring, bug fixes, new features)
- Use `gemini-cli` for research, design, content generation, and analysis
- Validate changes by running the game (syntax check, smoke test)
- Never break existing functionality — maintain backward compatibility

## Enhancement Cycle

1. Load state (last focus, enhancement count)
2. Determine next focus area (cycles: balance → features → content → polish)
3. Research: Gemini analyzes current codebase and suggests specific improvements
4. Implement: Qwen Code writes the actual code changes
5. Validate: Run the game to ensure it starts without errors
6. Commit and push changes
7. Update state and generate report

## Example Improvements

- Balance: tweak upgrade costs, fan growth rates, event probabilities
- Features: add new upgrade tiers, staff roles, episode production phases
- Content: new random events (20+), viral moments, industry trends
- Polish: improve text formatting, add color codes, fix edge cases
