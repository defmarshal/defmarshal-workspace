#!/usr/bin/env python3
"""
Web Dashboard - A simple HTTP server showing workspace status
Serves on http://localhost:8000
"""

import http.server
import socketserver
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import threading
import time

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
HOLIDAYS_FILE = WORKSPACE / "indonesia-holidays-full-2026.md"

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def get_bangkok_time():
    try:
        out, _, rc = run_cmd("TZ='Asia/Bangkok' date '+%Y-%m-%d %H:%M:%S %Z'")
        if rc == 0:
            return out
    except:
        pass
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def get_weather():
    out, _, rc = run_cmd("curl -s 'https://wttr.in/Bangkok?format=%C+%t'")
    if rc == 0 and out:
        return out
    return "unavailable"

def parse_holidays():
    if not HOLIDAYS_FILE.exists():
        return None
    try:
        lines = HOLIDAYS_FILE.read_text().splitlines()
    except:
        return None

    today = datetime.now().date()
    nearest = None
    nearest_days = float('inf')

    for line in lines:
        if line.startswith("|") and "20" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 6:
                date_str = parts[2]
                try:
                    hdate = datetime.strptime(date_str, "%Y-%m-%d").date()
                    days_away = (hdate - today).days
                    if 0 <= days_away < nearest_days:
                        nearest_days = days_away
                        nearest = {
                            "date": date_str,
                            "day": parts[3],
                            "holiday_id": parts[4],
                            "holiday_en": parts[5],
                            "days": days_away
                        }
                except:
                    continue
    return nearest

def get_git_status():
    out, _, rc = run_cmd("git status --short")
    if rc != 0:
        return {"status": "error", "message": "not a repo or error"}
    changed = [line for line in out.splitlines() if line.strip()]
    return {"status": "ok", "changed": len(changed), "clean": len(changed) == 0}

def get_recent_commits(n=3):
    out, _, rc = run_cmd(f"git log --oneline -n {n}")
    if rc != 0:
        return []
    lines = out.splitlines()
    commits = []
    for line in lines:
        if line.strip():
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                commits.append({"hash": parts[0][:7], "message": parts[1]})
    return commits

def get_disk_usage():
    out, _, rc = run_cmd("df -h / | awk 'NR==2 {print $5}'")
    out_clean = out.rstrip('%')
    pct = int(out_clean) if out_clean.isdigit() else 0
    return {"used_pct": pct, "critical": pct >= 90, "warning": pct >= 80}

def get_load_avg():
    try:
        with open('/proc/loadavg', 'r') as f:
            parts = f.read().split()
            if len(parts) >= 3:
                return {"1m": parts[0], "5m": parts[1], "15m": parts[2]}
    except Exception:
        pass
    out, _, rc = run_cmd("uptime | awk -F'load average:' '{print $2}' | sed 's/^ *//'")
    if rc == 0 and out:
        load_str = out.strip()
        return {"raw": load_str}
    return {"error": "unavailable"}

def get_memory_usage():
    out, _, rc = run_cmd("free -m | awk '/Mem:/ {printf \"%s %s\", $3, $2}'")
    if rc == 0 and out:
        used, total = out.split()
        try:
            pct = int(used) * 100 // int(total)
            return {"used_mb": int(used), "total_mb": int(total), "pct": pct}
        except:
            return {"error": "parse error"}
    return {"error": "unavailable"}

def get_updates():
    out, _, rc = run_cmd("apt list --upgradable 2>/dev/null | tail -n +2 | wc -l")
    try:
        count = int(out.strip())
        return {"available": count}
    except:
        return {"available": 0}

def get_memory_stats():
    """Fetch memory system statistics using openclaw memory status."""
    try:
        import shlex
        cmd = "openclaw memory status --json"
        out, err, rc = run_cmd(cmd)
        if rc != 0 or not out:
            return {"error": "status command failed"}
        data = json.loads(out)
        if not isinstance(data, list) or len(data) == 0:
            return {"error": "unexpected JSON structure"}
        entry = data[0]
        status = entry.get("status", {})
        return {
            "files": status.get("files", 0),
            "chunks": status.get("chunks", 0),
            "dirty": status.get("dirty", False),
            "provider": status.get("provider", "unknown"),
            "cache_entries": status.get("cache", {}).get("entries", 0),
            "fts_enabled": status.get("fts", {}).get("enabled", False),
        }
    except Exception as e:
        return {"error": str(e)}

def get_recent_memories(limit=3):
    """Fetch recent memory snippets using openclaw memory search."""
    try:
        import shlex
        cmd = f"openclaw memory search --json --max-results {limit} {shlex.quote('recent')}"
        out, err, rc = run_cmd(cmd)
        if rc != 0 or not out:
            return []
        data = json.loads(out)
        results = []
        for item in data.get("results", [])[:limit]:
            file = Path(item["path"]).name
            snippet = item["snippet"].strip().split('\n')[0]
            snippet = snippet[:100] + ("..." if len(snippet) > 100 else "")
            results.append({"file": file, "snippet": snippet})
        return results
    except Exception as e:
        return [{"error": str(e)}]

def collect_status():
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "bangkok_time": get_bangkok_time(),
        "weather": get_weather(),
        "holiday": parse_holidays(),
        "git": get_git_status(),
        "recent_commits": get_recent_commits(2),
        "disk": get_disk_usage(),
        "load": get_load_avg(),
        "memory": get_memory_usage(),
        "updates": get_updates(),
        "memory_stats": get_memory_stats(),
        "recent_memories": get_recent_memories(3),
    }

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = collect_status()
            self.wfile.write(json.dumps(status, indent=2).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # suppress logs
        return

HTML = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Workspace Web Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; background: #0f172a; color: #e2e8f0; }
    .container { max-width: 960px; margin: 0 auto; padding: 20px; }
    header { text-align: center; padding: 20px 0; margin-bottom: 20px; border-bottom: 1px solid #334155; }
    h1 { margin: 0; font-size: 1.8rem; color: #38bdf8; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
    .card { background: #1e293b; border-radius: 12px; padding: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .card h2 { margin-top: 0; font-size: 1.1rem; color: #93c5fd; border-bottom: 1px solid #334155; padding-bottom: 8px; }
    .row { display: flex; justify-content: space-between; margin: 8px 0; }
    .label { color: #94a3b8; }
    .value { font-weight: 500; }
    .good { color: #86efac; }
    .warn { color: #fcd34d; }
    .crit { color: #f87171; }
    footer { text-align: center; margin-top: 24px; color: #64748b; font-size: 0.9rem; }
    #refresh { text-align: center; margin: 16px 0; }
    button { background: #38bdf8; color: #0f172a; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; }
    button:hover { background: #0ea5e9; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Workspace Web Dashboard</h1>
    </header>
    <div id="refresh"><button onclick="refresh()">Refresh Now</button></div>
    <div class="grid">
      <div class="card">
        <h2>Time & Weather</h2>
        <div class="row"><span class="label">Bangkok:</span><span class="value" id="bangkok-time">...</span></div>
        <div class="row"><span class="label">Weather:</span><span class="value" id="weather">...</span></div>
      </div>
      <div class="card">
        <h2>Next Holiday</h2>
        <div class="row"><span class="label">Holiday:</span><span class="value" id="hol-name">...</span></div>
        <div class="row"><span class="label">Date:</span><span class="value" id="hol-date">...</span></div>
        <div class="row"><span class="label">In:</span><span class="value" id="hol-days">...</span></div>
      </div>
      <div class="card">
        <h2>Git Status</h2>
        <div class="row"><span class="label">Status:</span><span class="value" id="git-status">...</span></div>
        <div class="row"><span class="label">Changed:</span><span class="value" id="git-changed">...</span></div>
        <div class="row"><span class="label">Recent Commits:</span></div>
        <div id="git-commits" style="margin-top:8px;"></div>
      </div>
      <div class="card">
        <h2>Recent Memories</h2>
        <div id="mem-stats" style="font-size:0.9em; color:#94a3b8; margin-bottom:8px;"></div>
        <div id="mem-list"></div>
      </div>
      <div class="card">
        <h2>Disk</h2>
        <div class="row"><span class="label">Used:</span><span class="value" id="disk-pct">...</span></div>
      </div>
      <div class="card">
        <h2>Load Average</h2>
        <div class="row"><span class="label">1 min:</span><span class="value" id="load-1">...</span></div>
        <div class="row"><span class="label">5 min:</span><span class="value" id="load-5">...</span></div>
        <div class="row"><span class="label">15 min:</span><span class="value" id="load-15">...</span></div>
      </div>
      <div class="card">
        <h2>Memory</h2>
        <div class="row"><span class="label">Used:</span><span class="value" id="mem-used">...</span></div>
        <div class="row"><span class="label">Total:</span><span class="value" id="mem-total">...</span></div>
      </div>
      <div class="card">
        <h2>Updates</h2>
        <div class="row"><span class="label">Available:</span><span class="value" id="updates-count">...</span></div>
      </div>
    </div>
    <footer>
      <p>Auto-refresh every 60s | Data from OpenClaw Workspace</p>
    </footer>
  </div>
  <script>
    function refresh() {
      fetch('/status').then(r => r.json()).then(data => {
        document.getElementById('bangkok-time').textContent = data.bangkok_time;
        document.getElementById('weather').textContent = data.weather;

        if (data.holiday) {
          document.getElementById('hol-name').textContent = data.holiday.holiday_en + ' (' + data.holiday.holiday_id + ')';
          document.getElementById('hol-date').textContent = data.holiday.date;
          const days = data.holiday.days;
          document.getElementById('hol-days').textContent = days === 0 ? 'today' : days + ' day' + (days===1?'':'s');
        } else {
          document.getElementById('hol-name').textContent = 'None';
          document.getElementById('hol-date').textContent = '-';
          document.getElementById('hol-days').textContent = '-';
        }

        const git = data.git;
        document.getElementById('git-status').textContent = git.clean ? 'clean' : git.changed + ' changed';
        document.getElementById('git-status').className = 'value ' + (git.clean ? 'good' : 'warn');
        document.getElementById('git-changed').textContent = git.changed;

        const commitsDiv = document.getElementById('git-commits');
        if (data.recent_commits && data.recent_commits.length) {
          commitsDiv.innerHTML = data.recent_commits.map(c => `<div class="row"><span class="value">${c.hash}</span> ${c.message}</div>`).join('');
        } else {
          commitsDiv.textContent = 'none';
        }

        // Memory
        // Memory stats line
        const mstats = data.memory_stats || {};
        const memStatsDiv = document.getElementById('mem-stats');
        if (mstats.error) {
          memStatsDiv.textContent = 'stats unavailable';
        } else {
          const files = mstats.files || 0;
          const chunks = mstats.chunks || 0;
          const dirty = mstats.dirty ? 'dirty' : 'clean';
          const provider = mstats.provider || 'n/a';
          memStatsDiv.textContent = `${files} files, ${chunks} chunks (${dirty}) · ${provider}`;
        }

        // Recent memories list
        const memData = data.recent_memories || [];
        const memDiv = document.getElementById('mem-list');
        if (memData.length && !memData[0].error) {
          memDiv.innerHTML = memData.map(m => `<div class="row"><span class="label">${m.file}:</span><span class="value">${m.snippet}</span></div>`).join('');
        } else if (memData[0].error) {
          memDiv.textContent = 'error: ' + memData[0].error;
        } else {
          memDiv.textContent = 'none';
        }

        const disk = data.disk;
        const diskPct = disk.used_pct;
        document.getElementById('disk-pct').textContent = diskPct + '% used';
        const diskClass = disk.crit ? 'crit' : (disk.warning ? 'warn' : 'good');
        document.getElementById('disk-pct').className = 'value ' + diskClass;

        if (data.load && data.load['1m']) {
          document.getElementById('load-1').textContent = data.load['1m'];
          document.getElementById('load-5').textContent = data.load['5m'];
          document.getElementById('load-15').textContent = data.load['15m'];
        } else {
          document.getElementById('load-1').textContent = 'unavailable';
        }

        const mem = data.memory;
        if (!mem.error) {
          document.getElementById('mem-used').textContent = mem.used_mb + ' MB';
          document.getElementById('mem-total').textContent = mem.total_mb + ' MB';
        } else {
          document.getElementById('mem-used').textContent = 'unavailable';
          document.getElementById('mem-total').textContent = '-';
        }

        document.getElementById('updates-count').textContent = data.updates.available;
      }).catch(err => {
        console.error('Failed to fetch status', err);
      });
    }
    setInterval(refresh, 60000);
    refresh();
  </script>
</body>
</html>
'''

def main():
    PORT = 8800
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Web Dashboard running on http://localhost:{PORT}", flush=True)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nShutting down.", flush=True)
                httpd.server_close()
    except Exception as e:
        print(f"Server error: {e}", flush=True)
        raise

if __name__ == "__main__":
    main()