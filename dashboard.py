#!/usr/bin/env python3
"""
Workspace Dashboard - Your personal CLI dashboard
Shows: weather, next holiday, git status, recent memory, and more.
"""

import subprocess
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Config
WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
MEMORY_FILE = WORKSPACE / "MEMORY.md"
HOLIDAYS_FILE = WORKSPACE / "indonesia-holidays-full-2026.md"

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def get_bangkok_time():
    # Asia/Bangkok is UTC+7
    try:
        out, err, rc = run_cmd("TZ='Asia/Bangkok' date '+%Y-%m-%d %H:%M:%S %Z'")
        if rc == 0:
            return out
    except:
        pass
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def get_weather():
    out, err, rc = run_cmd("curl -s 'https://wttr.in/Bangkok?format=%C+%t'")
    if rc == 0 and out:
        return f"Weather (Bangkok): {out}"
    return "Weather: unavailable"

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
            if len(parts) >= 5:
                date_str = parts[1]
                try:
                    hdate = datetime.strptime(date_str, "%Y-%m-%d").date()
                    days_away = (hdate - today).days
                    if 0 <= days_away < nearest_days:
                        nearest_days = days_away
                        nearest = (parts[2], parts[3], parts[4], date_str)
                except:
                    continue
    return nearest, nearest_days

def get_git_status():
    out, err, rc = run_cmd("git status --short")
    if rc != 0:
        return "Git: not a repo or error"
    changed = [line for line in out.splitlines() if line.strip()]
    if not changed:
        return "Git: clean ✓"
    return f"Git: {len(changed)} file(s) changed/untracked"

def get_recent_commits(n=3):
    out, err, rc = run_cmd(f"git log --oneline -n {n}")
    if rc != 0:
        return []
    lines = out.splitlines()
    commits = []
    for line in lines:
        if line.strip():
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                commits.append(f"{parts[0][:7]} {parts[1]}")
    return commits

def search_memory(query="recent", limit=3):
    out, err, rc = run_cmd(f"./msearch '{query}'")
    if rc != 0 or not out:
        return []
    results = []
    count = 0
    for line in out.splitlines():
        if count >= limit:
            break
        if ':' in line:
            parts = line.split(':', 2)
            if len(parts) >= 3:
                file = Path(parts[0]).name
                content = parts[2][:100] + ("..." if len(parts[2]) > 100 else "")
                results.append(f"{file}: {content}")
                count += 1
    return results

def color(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def main():
    print(color("=== Workspace Dashboard ===\n", "1;34"))
    print(f"Time (Bangkok): {get_bangkok_time()}")
    print(get_weather())
    print()

    # Holidays
    holiday_info = parse_holidays()
    if holiday_info and holiday_info[0]:
        day, holiday_en, holiday_id, date = holiday_info[0]
        print(f"Next holiday: {holiday_en} ({holiday_id}) on {date} ({day})")
    else:
        print("No upcoming holiday found")
    print()

    # Git
    print(get_git_status())
    commits = get_recent_commits(2)
    if commits:
        print("Recent commits:")
        for c in commits:
            print(f"  {c}")
    print()

    # Memory search
    print("Recent memory mentions:")
    mem = search_memory("today", 2)
    if mem:
        for m in mem:
            print(f"  {m}")
    else:
        print("  (no recent hits)")

    print()
    print(color("Have a productive day!\n", "1;32"))

if __name__ == "__main__":
    main()
