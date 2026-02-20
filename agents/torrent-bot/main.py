#!/usr/bin/env python3
"""
Torrent Bot — OpenClaw sub-agent for slash-command torrent management.
Handles: /torrent add|search|top|status|pause|resume|remove|watch|watchlist|help

Uses existing quick launcher (torrent-add, nyaa-search, nyaa-top, downloads).
"""

import os
import sys
import json
import subprocess
from pathlib import Path

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
QUICK = WORKSPACE / "quick"
WATCHLIST_FILE = WORKSPACE / "memory" / "torrent-watchlist.json"

def run_quick(cmd_parts):
    """Run a quick command and return output."""
    full_cmd = [str(QUICK)] + cmd_parts
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def cmd_add(args):
    if not args:
        return "Usage: /torrent add <magnet_or_url>"
    # quick torrent-add expects the magnet or file path
    out, err, rc = run_quick(["torrent-add"] + args)
    if rc == 0:
        return f"✅ Added to download queue:\n{out}"
    else:
        return f"❌ Failed: {err}"

def cmd_search(args):
    if not args:
        return "Usage: /torrent search <query>"
    out, err, rc = run_quick(["nyaa-search"] + args)
    if rc == 0:
        return f"🔍 Search results:\n{out}"
    else:
        return f"❌ Search failed: {err}"

def cmd_top(args):
    # forward all args (--limit, --max-size, --pick, --add)
    out, err, rc = run_quick(["nyaa-top"] + args)
    if rc == 0:
        return f"🏆 Top torrents:\n{out}"
    else:
        return f"❌ Failed: {err}"

def cmd_status(args):
    out, err, rc = run_quick(["downloads"])
    if rc == 0:
        return f"📥 Active downloads:\n{out}"
    else:
        return f"❌ Could not fetch status: {err}"

def cmd_pause(args):
    if not args:
        return "Usage: /torrent pause <gid>"
    gid = args[0]
    # Call quick torrent-pause
    out, err, rc = run_quick(["torrent-pause", gid])
    if rc == 0:
        return out
    else:
        return f"❌ Pause failed: {err}"

def cmd_resume(args):
    if not args:
        return "Usage: /torrent resume <gid>"
    gid = args[0]
    # Call quick torrent-resume
    out, err, rc = run_quick(["torrent-resume", gid])
    if rc == 0:
        return out
    else:
        return f"❌ Resume failed: {err}"

def cmd_remove(args):
    if not args:
        return "Usage: /torrent remove <gid>"
    gid = args[0]
    # Call quick torrent-remove
    out, err, rc = run_quick(["torrent-remove", gid])
    if rc == 0:
        return out
    else:
        return f"❌ Remove failed: {err}"

def load_watchlist():
    if WATCHLIST_FILE.exists():
        try:
            return json.loads(WATCHLIST_FILE.read_text())
        except:
            return []
    return []

def save_watchlist(wl):
    WATCHLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    WATCHLIST_FILE.write_text(json.dumps(wl, indent=2))

def cmd_watch(args):
    """Add a query to the watchlist. Usage: /torrent watch <query> [--add]"""
    if not args:
        return "Usage: /torrent watch <query>"
    query = " ".join([a for a in args if not a.startswith("--")])
    if not query:
        return "Provide a search query."
    wl = load_watchlist()
    if query in wl:
        return f"🔄 Query already in watchlist: {query}"
    wl.append(query)
    save_watchlist(wl)
    return f"👀 Added to watchlist: {query}\nWatchlist size: {len(wl)}"

def cmd_watchlist(args):
    wl = load_watchlist()
    if not wl:
        return "📋 Watchlist is empty."
    entries = "\n".join(f"{i+1}. {q}" for i, q in enumerate(wl))
    return f"📋 Watchlist ({len(wl)} items):\n{entries}"

def cmd_help(args):
    help_text = """📚 Torrent Bot Commands:
/torrent add <magnet_or_url>     Add a torrent
/torrent search <query>         Search Nyaa
/torrent top [opts]             List top torrents (--limit N, --max-size SIZE, --pick N, --add)
/torrent status                 Show active downloads
/torrent pause <gid>            Pause download
/torrent resume <gid>           Resume download
/torrent remove <gid>           Remove from queue
/torrent watch <query>          Add query to watchlist (auto-daily)
/torrent watchlist              Show watchlist
/torrent help                   Show this help

Examples:
/torrent top --limit 10 --max-size 2G
/torrent watch \"One Piece 2025\" --add
"""
    return help_text

def handle_message(message_text):
    """Handle incoming slash command message."""
    parts = message_text.strip().split()
    if not parts:
        return "Send /torrent help for commands."
    if parts[0] != "/torrent":
        return "Unknown command. Use /torrent help"
    cmd = parts[1] if len(parts) > 1 else "help"
    args = parts[2:]

    handlers = {
        "add": cmd_add,
        "search": cmd_search,
        "top": cmd_top,
        "status": cmd_status,
        "pause": cmd_pause,
        "resume": cmd_resume,
        "remove": cmd_remove,
        "watch": cmd_watch,
        "watchlist": cmd_watchlist,
        "help": cmd_help,
    }
    handler = handlers.get(cmd, cmd_help)
    return handler(args)

# OpenClaw agent entrypoint
if __name__ == "__main__":
    # OpenClaw sends one JSON message per line on stdin.
    for input_line in sys.stdin:
        input_line = input_line.strip()
        if not input_line:
            continue
        try:
            msg = json.loads(input_line)
            text = msg.get("content", "")
        except json.JSONDecodeError:
            text = input_line
        except Exception:
            text = input_line
        try:
            response = handle_message(text)
        except Exception as e:
            response = f"Internal error: {e}"
        print(response)
        sys.stdout.flush()
