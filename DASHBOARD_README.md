# Workspace Dashboard

A CLI dashboard for your OpenClaw workspace.

## Features

- **Bangkok time** (local timezone)
- **Weather** (wttr.in)
- **Next Indonesian holiday** (from `indonesia-holidays-full-2026.md`)
- **Git status** and recent commits
- **Memory search** (recent entries)

## Usage

```bash
python3 dashboard.py
```

Or add to your PATH:

```bash
# Option 1: run directly
python3 /path/to/workspace/dashboard.py

# Option 2: create symlink
ln -s /home/ubuntu/.openclaw/workspace/dashboard.py ~/bin/workspace-dash
chmod +x ~/bin/workspace-dash
workspace-dash
```

## Notes

- Requires `curl` for weather
- Uses `openclaw memory search` (via `quick search`) for memory retrieval
- Colors may not display on some terminals (disable escape codes if needed)

## Future Ideas

- Web version
- More detailed memory stats
- System health (disk, uptime)
- Customizable modules
