#!/usr/bin/env python3
"""Garden Dashboard Server - Serves static files from workspace root on port 3001"""

import http.server
import socketserver
import os
import signal
import sys

WORKSPACE = "/home/ubuntu/.openclaw/workspace"
PORT = 3002
PID_FILE = os.path.join(WORKSPACE, "garden-dashboard.pid")

class ReuseAddrServer(socketserver.TCPServer):
    allow_reuse_address = True

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

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = ReuseAddrServer(("", PORT), Handler)

    with httpd:
        # Write PID file
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
        print(f"✓ Garden Dashboard started (PID {os.getpid()})")
        print(f"  URL: http://localhost:{PORT}/garden-dashboard.html")
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
            print(f"  URL: http://localhost:{PORT}/garden-dashboard.html")
        except ProcessLookupError:
            print("Garden Dashboard process not found (stale PID file)")
    else:
        print("Garden Dashboard is NOT running")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: garden-server.py {start|stop|status}")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "start":
        start()
    elif cmd == "stop":
        stop()
    elif cmd == "status":
        status()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
