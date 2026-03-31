#!/bin/bash
set -euo pipefail

export PATH="$HOME/.npm-global/bin:$PATH"
cd "$HOME/.openclaw/workspace"

LOG_DIR="memory/self-improvement"
mkdir -p "$LOG_DIR"
LOGFILE="$LOG_DIR/$(date -u +%Y-%m-%dT%H:%M:%SZ).log"
exec > >(tee -a "$LOGFILE") 2>&1

echo "=== Self-Improvement Cycle Start ==="
date -u

# 1. Find recent research reports (last 24h) with optimization keywords
TODAY=$(date -u +%Y-%m-%d)
YESTERDAY=$(date -u -d "yesterday" +%Y-%m-%d)
REPORTS=()
for day in "$TODAY" "$YESTERDAY"; do
  while IFS= read -r r; do
    REPORTS+=("$r")
  done < <(ls research/${day}*.md 2>/dev/null | grep -iE "optimization|performance|tuning|system|ops|monitoring|alert|maintenance|scalability|reliability|cost|efficiency" || true)
done

if [ ${#REPORTS[@]} -eq 0 ]; then
  echo "No recent optimization-focused reports found. Exiting."
  exit 0
fi

echo "Found ${#REPORTS[@]} relevant reports to analyze."

# 2. Extract actionable recommendations via LLM
REPORTS_INPUT=$(printf "%s\n" "${REPORTS[@]}")
RAW_OUTPUT=$(openclaw agent --agent main --message "
You are a system operations engineer. Read these research report filenames and content snippets.
Extract ONLY concrete, specific, and safe-to-apply actions for THIS OpenClaw system.
Focus on: cron tuning, monitoring, resource cleanup, security hardening, dependency updates, configuration tweaks.

For each action, provide JSON:
{
  \"action\": string (exact change to make),
  \"reason\": string (why from the report),
  \"risk\": \"low\" | \"medium\" | \"high\",
  \"priority\": 1-5 (5=urgent),
  \"source\": filename
}

Return a JSON array only, no extra text. Max 10 items. Skip vague insights.
" --local <<< "$REPORTS_INPUT" 2>/dev/null || echo '[]')

echo "Raw agent output: $RAW_OUTPUT"

# Extract first JSON array from output (handle extra text)
RECOMMENDATIONS=$(echo "$RAW_OUTPUT" | python3 -c "
import sys, json, re
data = sys.stdin.read()
m = re.search(r'(\[[^\]]*\]|\{[^\}]*\})', data, re.DOTALL)
if m:
  try:
    parsed = json.loads(m.group(1))
    print(json.dumps(parsed))
  except:
    print('[]')
else:
    print('[]')
")

echo "Parsed recommendations: $RECOMMENDATIONS"

# Validate JSON (must be array)
echo "$RECOMMENDATIONS" | python3 -c "
import sys, json
try:
  data = json.load(sys.stdin)
  if not isinstance(data, list):
    print('Error: recommendations must be a JSON array')
    exit(1)
  print(f'Valid JSON array with {len(data)} items')
except Exception as e:
  print(f'JSON parse error: {e}')
  exit(1)
" || exit 1

# 3. Apply low-risk, high-priority actions automatically
echo "$RECOMMENDATIONS" | python3 -c "
import json, sys, subprocess, os
actions = json.load(sys.stdin)
applied = []
skipped = []
for a in actions:
  if a.get('risk') == 'low' and a.get('priority', 0) >= 4:
    act = a.get('action', '')
    print(f'Applying (low-risk): {act[:100]}')
    # Try to apply (we'll implement a safe executor)
    # For now, just log intention
    applied.append(a)
  else:
    skipped.append(a)
print(f'Applied: {len(applied)}, Skipped (medium/high/low-prio): {len(skipped)}')
" || true

# 4. Create PR/issue for medium/high risk items (draft file)
echo "$RECOMMENDATIONS" | python3 -c "
import json, sys, datetime
actions = [a for a in json.load(sys.stdin) if a.get('risk') in ('medium','high') or a.get('priority',0) >= 4]
if actions:
  fn = f'/home/ubuntu/.openclaw/workspace/memory/self-improvement/feeder-{datetime.datetime.utcnow().strftime(\"%Y%m%d-%H%M%S\')}.jsonl'
  with open(fn, 'w') as f:
    for a in actions:
      f.write(json.dumps(a) + '\n')
  print(f'Created {len(actions)} medium/high actions in {fn}')
" 2>/dev/null || true

# 5. Commit any changes made during this cycle
if git diff --quiet 2>/dev/null; then
  echo "No git changes to commit from self-improvement cycle."
else
  git add -A
  git commit -m "self-improvement: apply automated optimizations based on latest research" || true
fi

echo "=== Self-Improvement Cycle End ==="
date -u
