# OpenClaw RPG Dashboard

A Final Fantasy ATB‑style dashboard visualizing OpenClaw cron jobs as quests and agents as party members.

## Features

- **Pixel‑art UI:** Press Start 2P font, stone panels, gold accents
- **Job classes:** Each agent has an FF role (White Mage, Thief, Guardian, etc.)
- **ATB gauge:** Fills between runs; indicates time until next execution
- **Morale (HP) & Magic (MP) bars**
- **Battle sound** on hover (classic ATB chime)
- **Victory fanfare** when all jobs are healthy (100%)
- **Party Health** meter at top (color‑coded)
- **Tooltips:** Full schedule and status details on hover
- **Auto‑refresh** every 10 s

## Quick Start

```bash
# Use the manager script (recommended)
./quick dashboard start

# Or manually:
node dashboard/server.js &
```

Then open: **http://localhost:3000**

## Quick Commands

```bash
./quick dashboard status   # Check if running
./quick dashboard stop    # Stop server
./quick dashboard open    # Open browser (default http://localhost:3000)
```

## Data Source

Reads `~/.openclaw/cron/jobs.json` directly; no API needed.

## Customization

- Edit `dashboard/rpg-dashboard.html` to tweak sprites, colors, bars.
- Job class mapping in `JOB_CLASSES` (agentId → role/icon/color).
- ATB interval estimation logic in `calculateATB` and schedule parsing.

## Autostart

Already included in `start-background-agents.sh` (starts on boot).

## Files

- `dashboard/server.js` — Node server (binds 0.0.0.0:3000)
- `dashboard/rpg-dashboard.html` — Main UI (self‑contained)
- `dashboard/dashboard` — Manager script (start/stop/status/open)

Enjoy your Final Fantasy–themed system monitor! (◕‿◕)✨
