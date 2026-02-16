# Game Dev Agent Duo — Vishwakarma & Kṛṣṇa

**Vishwakarma** (planner) and **Kṛṣṇa** (builder) form an autonomous game development pipeline, inspired by Agni & Rudra.

## How It Works

1. **Vishwakarma** runs every 4 hours (via cron)
2. Scans for game development opportunities (e.g., missing games, requested features)
3. Creates a structured game design plan in `agents/vishwakarma/plans/gameplan-<timestamp>.md`
4. Spawns **Kṛṣṇa** as an isolated OpenClaw sub-agent
5. **Kṛṣṇa** reads the plan, implements the game, tests, commits, and writes a completion report
6. Cycle repeats

## Files

- `agents/vishwakarma-cycle.sh` — planner script (cron‑triggered)
- `agents/krishna-builder.sh` — builder script (run by spawned agent)
- `agents/vishwakarma/` — logs, plans
- `agents/krishna/` — logs, reports
- `games/` — built games (each in own subdirectory)

## Current Plan (v0.1)

**Game:** Anime Studio Tycoon (CLI management sim)
- Manage an anime studio: money, staff, reputation, fan count
- Weekly decisions, random events, win/lose conditions
- Pure Python 3, no dependencies
- Target: ~200–300 lines

## Installation

Add cron job:

```bash
openclaw cron add --name vishwakarma-cron --expr "0 */4 * * *" --tz "Asia/Bangkok" \
  --payload '{"kind":"agentTurn","message":"You are the Vishwakarma cron job. Your task: run one game planning cycle. Execute: bash -c \'cd /home/ubuntu/.openclaw/workspace && ./agents/vishwakarma-cycle.sh >> agents/vishwakarma/vishwakarma.log 2>&1\'. Use the exec tool."}' \
  --sessionTarget isolated
```

(Or add to crontab directly.)

## Status

- Planner: ready to spawn builder
- Builder: ready to implement plans
- First game (Anime Studio Tycoon) will be created on first run

## Notes

This is a custom agent pair built on OpenClaw. They operate independently of regular content/research/dev agents.

*Built 2026-02-16 by mewmew (◕‿◕)♡*
