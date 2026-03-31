#!/usr/bin/env python3
import json, sys

path = '/home/ubuntu/.openclaw/cron/jobs.json'
with open(path, 'r') as f:
    data = json.load(f)

cleared = 0
for job in data['jobs']:
    if 'runningAtMs' in job['state']:
        del job['state']['runningAtMs']
        cleared += 1

with open(path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Cleared runningAtMs from {cleared} cron jobs")
