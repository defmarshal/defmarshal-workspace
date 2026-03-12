#!/usr/bin/env python3
"""Garden Dashboard Server - Serves static files + /api/stats"""

import http.server
import socketserver
import os
import signal
import sys
import json
import subprocess
from datetime import datetime, timezone

WORKSPACE = "/home/ubuntu/.openclaw/workspace"
PORT = 3002
PID_FILE = os.path.join(WORKSPACE, "garden-dashboard.pid")

class ReuseAddrServer(socketserver.TCPServer):
    allow_reuse_address = True

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            stats = get_system_stats()
            self.wfile.write(json.dumps(stats).encode('utf-8'))
        else:
            return super().do_GET()

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def get_disk_usage():
    out, _, rc = run_cmd("df -h . | awk 'NR==2 {print $5}'")
    if rc == 0:
        pct = out.rstrip('%')
        try:
            return float(pct) / 100.0
        except Exception:
            return 0.68  # fallback
    return 0.68

def get_cpu_usage():
    out, _, rc = run_cmd("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
    if rc == 0:
        try:
            return float(out) / 100.0
        except Exception:
            return 0.1
    return 0.1

def get_gateway_status():
    _, _, rc = run_cmd("openclaw gateway status >/dev/null 2>&1")
    return rc == 0

def get_uptime():
    out, _, rc = run_cmd("cat /proc/uptime | awk '{print $1}'")
    if rc == 0:
        try:
            return int(float(out))
        except Exception:
            return 0
    return 0

def get_active_agents():
    # Count active sessions for main agent
    out, _, rc = run_cmd("openclaw sessions list --activeMinutes 5 --json 2>/dev/null | jq -r '.sessions[] | select(.agentId==\"main\") | .sessionKey' | wc -l")
    if rc == 0:
        try:
            return int(out.strip())
        except Exception:
            return 0
    return 0

def get_error_count():
    # Approximate: count ERROR lines in recent logs
    out, _, rc = run_cmd("tail -100 memory/*.log 2>/dev/null | grep -ci 'ERROR\\|error\\|Rate limit' || echo 0")
    try:
        return int(out.strip())
    except Exception:
        return 0

def get_system_stats():
    return {
        "disk": round(get_disk_usage(), 3),
        "cpu": round(get_cpu_usage(), 3),
        "gateway": get_gateway_status(),
        "uptime": get_uptime(),
        "activeAgents": get_active_agents(),
        "errors": get_error_count(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def start():
    os.chdir(WORKSPACE)
    # Check if already running
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            old_pid = int(f.read().strip())
        try:
            os.kill(old_pid, 0)
            print(f"Garden Dashboard already running (PID {old_pid})")
            return
        except ProcessLookupError:
            pass  # stale pid file

    httpd = ReuseAddrServer(("", PORT), Handler)

    with httpd:
        # Write PID file
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
        print(f"✓ Garden Dashboard started (PID {os.getpid()})")
        print(f"  URL: http://localhost:{PORT}/organism-dashboard.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)

def stop():
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"✓ Garden Dashboard stopped (PID {pid})")
            os.remove(PID_FILE)
        except ProcessLookupError:
            print("Process not running (stale PID file)")
            os.remove(PID_FILE)
    else:
        print("Garden Dashboard not running (no PID file)")

def status():
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 0)
            print(f"Garden Dashboard is running (PID {pid})")
            print(f"  URLs:")
            print(f"    Garden: http://localhost:{PORT}/garden-dashboard.html")
            print(f"    Organism: http://localhost:{PORT}/organism-dashboard.html")
        except ProcessLookupError:
            print("Garden Dashboard process not found (stale PID file)")
    else:
        print("Garden Dashboard is NOT running")

def open_browser(page='garden'):
    url = f"http://localhost:{PORT}/{page}.html"
    if os.system(f"which xdg-open >/dev/null 2>&1") == 0:
        os.system(f"xdg-open '{url}'")
    elif os.system(f"which open >/dev/null 2>&1") == 0:
        os.system(f"open '{url}'")
    else:
        print(f"Please open manually: {url}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: garden-server.py {start|stop|status|open [garden|organism]}")
        sys.exit(1)
    cmd = sys.argv[1]
    page = sys.argv[2] if len(sys.argv) > 2 else 'garden'
    if cmd == "start":
        start()
    elif cmd == "stop":
        stop()
    elif cmd == "status":
        status()
    elif cmd == "open":
        open_browser(page)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
        sys.exit(1)
