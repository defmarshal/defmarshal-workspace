# Torrent Bot (slash-command agent)

A Telegram slash-command bot for managing aria2 downloads via Nyaa search.

## Files

- `agent.json` — Agent definition (tools, allowlists)
- `main.py` — Slash command handler
- `loop.sh` — Daemon loop (respects quiet hours)
- `run.sh` — One-shot spawn

## Commands

`/torrent add <magnet_or_url>` — Add torrent  
`/torrent search <query>` — Search Nyaa  
`/torrent top [--limit N] [--max-size SIZE] [--pick N] [--add]` — Top seeds  
`/torrent status` — Show active downloads  
`/torrent watch <query>` — Add to daily watchlist  
`/torrent watchlist` — List saved queries  
`/torrent help` — Show help

## Setup

1. Ensure `quick` launcher includes:
   - `torrent-add`
   - `nyaa-search`
   - `nyaa-top`
   - `downloads`

2. Add to startup: edit `start-background-agents.sh` to include `start_if_missing "torrent-bot" "agents/torrent-bot/loop.sh"`

3. Manual start:
   ```bash
   ./agents/torrent-bot/run.sh
   ```

4. Approved Telegram senders: set `allowlists` in agent.json or use global pairing.

## Notes

- Uses `shell.exec` tool with restricted commands via the agent's allowlist.
- Watchlist stored in `memory/torrent-watchlist.json` (auto-created).
- Quiet hours: 23:00–08:00 Asia/Bangkok (daemon will not spawn new sessions).
- Logs: agent session logs appear in `~/.openclaw/agents/torrent-bot/*/sessions/*.jsonl`
