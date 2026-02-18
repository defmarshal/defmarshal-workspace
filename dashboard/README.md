# OpenClaw RPG Dashboard

A retro-styled HTML dashboard that visualizes cron jobs as quests and agents as NPCs.

## Features

- Agents shown as RPG characters with icons
- Cron jobs as "quests" with health bars (based on last run vs schedule)
- Status badges (OK, FAILURE, DISABLED)
- Auto-refresh every 10 seconds
- Single-page app, no dependencies

## How to Run

```bash
# Start the server (listens on http://localhost:3000)
node dashboard/server.js

# Or use nohup to run in background:
nohup node dashboard/server.js > /dev/null 2>&1 &
```

Then open in browser: **http://localhost:3000**

## Data Source

The dashboard reads `~/.openclaw/cron/jobs.json` directly to get job status. No API calls needed.

## Customization

- Edit `dashboard/rpg-dashboard.html` to change icons, colors, or stats.
- Icons map: `ICONS` object in script section (`main`, `torrent-bot`, `cron-supervisor`, etc.)
- HP bar calculation is a rough estimate based on schedule interval.

## Optional: Autostart

Add to `start-background-agents.sh`:

```bash
start_if_missing "rpg-dashboard" "dashboard/server.js"
```

## Screenshot

(Design: dark theme, card grid, circular sprite emojis, health bars)
