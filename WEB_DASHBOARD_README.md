# Web Dashboard

A simple web-based workspace status dashboard. Runs a tiny HTTP server that serves a single-page app with real-time stats.

## Features

- Bangkok time & weather (via wttr.in)
- Next Indonesian holiday (with countdown)
- Git status and recent commits
- System health: disk, load average, memory, updates
- Auto-refresh every 60s

## Usage

```bash
# Start the server
./web-dashboard.sh
# or
python3 web-dashboard.py
```

Then open your browser to: **http://localhost:8800**

Press `Ctrl+C` to stop the server.

## Notes

- Server listens on port 8800 (change in `web-dashboard.py` if needed)
- Weather may be unavailable depending on network/firewall
- No authentication — bind only to localhost

## Screenshot

Dark theme with cards:

```
+---------------------------------------+
|      Workspace Web Dashboard         |
|           [Refresh Now]              |
+---------------------------------------+
| Time & Weather | Next Holiday        |
| ...            | ...                 |
+----------------+---------------------+
| Git Status     | Disk                |
| ...            | ...                 |
+----------------+---------------------+
| Load Average   | Memory              |
| ...            | ...                 |
+----------------+---------------------+
| Updates                          ... |
+---------------------------------------+
```
