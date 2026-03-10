#!/usr/bin/env python3
import json, glob, os
from datetime import datetime

WORKSPACE = "/home/ubuntu/.openclaw/workspace"
os.chdir(WORKSPACE)

files = []
# content/*.md
for f in sorted(glob.glob('content/*.md')):
    files.append(f)
# research/*.md  
for f in sorted(glob.glob('research/*.md')):
    files.append(f)

with open('outputs-manifest.json', 'w') as out:
    json.dump(files, out, indent=2)

print(f"✅ Generated outputs-manifest.json with {len(files)} files")
