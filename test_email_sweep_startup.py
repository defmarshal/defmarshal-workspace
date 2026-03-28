#!/usr/bin/env python3
import os, sys, json, time

# Load .env
env_path = '.env'
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, _, value = line.partition('=')
                os.environ[key.strip()] = value.strip()

BATCH_SIZE = int(os.getenv('BATCH_SIZE', '1000'))
PAGES_PER_RUN = int(os.getenv('PAGES_PER_RUN', '4'))
API_KEY = os.getenv('MATON_API_KEY')
if not API_KEY:
    print("MATON_API_KEY not set")
    sys.exit(1)

STATE_FILE = 'memory/email-categorizer.state'
LOG_FILE = 'memory/email-categorizer.log'
LABEL_MAP_FILE = 'memory/label_mapping.json'
LABEL_CACHE_FILE = 'memory/email_labels.json'

def log(msg):
    t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
    line = f"[{t}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def load_state():
    try:
        with open(STATE_FILE) as f:
            exec(compile(f.read(), STATE_FILE, 'exec'), {}, state)
        return state.get('NEXT_PAGE_TOKEN', '')
    except Exception as e:
        print(f"load_state error: {e}")
        return ''

def load_sender_mapping():
    try:
        with open(LABEL_MAP_FILE) as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"load_sender_mapping error: {e}")
        return {}

print("About to load sender mapping...", flush=True)
SENDER_MAP = load_sender_mapping()
print(f"SENDER_MAP loaded, entries: {len(SENDER_MAP)}", flush=True)

print("About to log 'Starting sweep'...", flush=True)
log("Starting sweep")
print("Logged starting sweep", flush=True)

token = load_state()
print(f"Token loaded: {token}", flush=True)