#!/usr/bin/env python3
"""Refresh dashboard data.json with latest info."""
import json, time, subprocess, os, glob, re
from datetime import datetime

WORKSPACE = "/home/ubuntu/.openclaw/workspace"

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30).stdout.strip()

def read_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default or {}

def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def get_system_stats():
    # disk_percent from df
    disk = run("df -h / | tail -1 | awk '{print $5}'").strip('%')
    load = run("cat /proc/loadavg | awk '{print $1,$2,$3}'")
    uptime = run("cat /proc/uptime | awk '{print $1}'")
    return {
        "disk_percent": int(disk) if disk.isdigit() else 0,
        "load": load,
        "uptime_seconds": int(float(uptime)) if uptime else 0,
        "os": os.uname().sysname,
        "arch": os.uname().machine
    }

def get_active_tasks():
    try:
        with open(f"{WORKSPACE}/active-tasks.md") as f:
            content = f.read()
        # Parse simple lines: - [ ] or - [x]
        tasks = []
        for line in content.splitlines():
            if line.startswith('- ['):
                tasks.append(line)
        return tasks[:20]
    except:
        return []

def get_latest_commits(limit=10):
    out = run(f"cd {WORKSPACE} && git log --oneline -{limit} --date=relative --pretty=format:'%h %s (%cd)'")
    commits = []
    for line in out.splitlines():
        if line:
            parts = line.split(' ', 1)
            if len(parts)>=2:
                commits.append({"hash": parts[0], "message": parts[1]})
    return commits

def get_heartbeat():
    hb = read_json(f"{WORKSPACE}/memory/heartbeat-state.json")
    with open(f"{WORKSPACE}/HEARTBEAT.md") as f:
        checks = f.read()
    return {"state": hb, "checks": checks}

def get_supervisor_log_tail(lines=20):
    try:
        with open(f"{WORKSPACE}/memory/supervisor.log") as f:
            all_lines = f.readlines()
        # Return last N lines as list, stripped of newlines
        return [line.rstrip('\n') for line in all_lines[-lines:]]
    except:
        return []

def get_outputs(limit=30):
    """Return recent output files (reports, content, research) with timestamps."""
    outputs = []
    # Scan reports/
    for root, dirs, files in os.walk(f"{WORKSPACE}/reports"):
        for fn in files:
            if fn.endswith('.md'):
                p = os.path.join(root, fn)
                try:
                    st = os.stat(p)
                    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                        first = f.readline().strip().lstrip('#').strip()[:80]
                    outputs.append({
                        'ts': int(st.st_mtime * 1000),
                        'title': first or fn,
                        'file': os.path.relpath(p, WORKSPACE),
                        'size': st.st_size
                    })
                except:
                    pass
    # Scan content/
    for root, dirs, files in os.walk(f"{WORKSPACE}/content"):
        for fn in files:
            if fn.endswith('.md'):
                p = os.path.join(root, fn)
                try:
                    st = os.stat(p)
                    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                        first = f.readline().strip().lstrip('#').strip()[:80]
                    outputs.append({
                        'ts': int(st.st_mtime * 1000),
                        'title': first or fn,
                        'file': os.path.relpath(p, WORKSPACE),
                        'size': st.st_size
                    })
                except:
                    pass
    outputs.sort(key=lambda x: x['ts'], reverse=True)
    return outputs[:limit]

def get_agent_outputs():
    # Backwards compatibility: return outputs array (recent content/reports)
    return get_outputs()

def get_cron_jobs():
    # Use openclaw cron list JSON
    try:
        raw = run("openclaw cron list --json")
        # Strip any non-JSON prefix lines
        start = raw.find('{')
        end = raw.rfind('}') + 1
        if start >=0 and end > start:
            cron_data = json.loads(raw[start:end])
            jobs = []
            for job in cron_data['jobs']:
                st = job['state']
                sched = job['schedule']
                if 'expr' in sched:
                    schedule_str = sched['expr']
                    tz = sched.get('tz','UTC')
                elif 'everyMs' in sched:
                    ms = sched['everyMs']
                    sec = ms/1000
                    if sec < 60:
                        schedule_str = f"every {sec:.0f}s"
                    elif sec < 3600:
                        schedule_str = f"every {sec/60:.0f}m"
                    else:
                        schedule_str = f"every {sec/3600:.0f}h"
                    tz = sched.get('tz','UTC')
                else:
                    schedule_str = 'once'
                    tz = 'UTC'
                jobs.append({
                    'name': job['name'],
                    'schedule': schedule_str,
                    'tz': tz,
                    'enabled': job['enabled'],
                    'last_run': st.get('lastRunAtMs'),
                    'next_run': st.get('nextRunAtMs'),
                    'status': st.get('lastStatus','ok'),
                    'last_error': st.get('lastError','')
                })
            return jobs
    except Exception as e:
        print(f"Error getting cron jobs: {e}", file=sys.stderr)
    return []

def get_active_tasks_sessions():
    # Use openclaw sessions list JSON
    try:
        raw = run("openclaw sessions --json")
        # Might have warnings; strip
        start = raw.find('{')
        end = raw.rfind('}') + 1
        if start>=0:
            sessions = json.loads(raw[start:end])
            # Sessions list format? It may be array or object with sessions key
            if isinstance(sessions, dict) and 'sessions' in sessions:
                sessions = sessions['sessions']
            # Return basic info
            simple = []
            for s in sessions:
                simple.append({
                    "sessionKey": s.get('sessionKey',''),
                    "kinds": s.get('kinds',[]),
                    "lastMsg": s.get('lastMsg','')[:100],
                    "activeSec": s.get('activeSec',0)
                })
            return simple[:20]
    except Exception as e:
        print(f"Error getting sessions: {e}", file=sys.stderr)
    return []

def get_content_stats():
    total = 0
    today = 0
    latest_title = ""
    content_dir = f"{WORKSPACE}/content"
    if os.path.exists(content_dir):
        md_files = glob.glob(f"{content_dir}/**/*.md", recursive=True)
        total = len(md_files)
        # today's date UTC
        today_str = datetime.utcnow().strftime('%Y-%m-%d')
        for fpath in md_files:
            try:
                mtime = os.path.getmtime(fpath)
                if datetime.utcfromtimestamp(mtime).strftime('%Y-%m-%d') == today_str:
                    today += 1
            except:
                pass
        # latest by mtime
        if md_files:
            latest = max(md_files, key=os.path.getmtime)
            with open(latest) as f:
                first = f.readline().strip().lstrip('#').strip()
            latest_title = first
    return {"total": total, "today": today, "latest_title": latest_title}

def get_chat_history(limit=50):
    # Use openclaw chat history? Might be easier to read from sessions file.
    chat_file = f"{WORKSPACE}/memory/chat.json"
    # If there's no central chat store, we can skip or use empty
    if os.path.exists(chat_file):
        try:
            with open(chat_file) as f:
                data = json.load(f)
            msgs = data.get('chat', [])
            return msgs[-limit:]
        except:
            pass
    # Fallback: use last session's chat from sessions.json
    sess_path = "/home/ubuntu/.openclaw/agents/main/sessions/sessions.json"
    if os.path.exists(sess_path):
        try:
            with open(sess_path) as f:
                sessions = json.load(f)
            # Find most recent session with messages
            if sessions:
                latest = sessions[-1]
                msgs = latest.get('messages', [])
                return msgs[-limit:]
        except:
            pass
    return []

def main():
    now = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    out = {
        "generated_at": now,
        "system": get_system_stats(),
        "agents": get_active_tasks_sessions(),
        "research": [],  # placeholder
        "recent_commits": get_latest_commits(10),
        "heartbeat": get_heartbeat(),
        "supervisor_log": get_supervisor_log_tail(20),
        "agent_outputs": get_agent_outputs(),
        "cron_jobs": get_cron_jobs(),
        "active_tasks": get_active_tasks(),
        "content_stats": get_content_stats(),
        "chat": get_chat_history(50)
    }
    write_json(f"{WORKSPACE}/apps/dashboard/data.json", out)
    print(f"✅ Dashboard data refreshed ({now})")

if __name__ == "__main__":
    main()
