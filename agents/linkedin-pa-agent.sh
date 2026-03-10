#!/usr/bin/env bash
set -euo pipefail
# LinkedIn Content Agent - IBM Planning Analytics (Analyst-Report v10)
# Dynamic LLM-generated queries + topic bucket rotation (CREATIVE MODE)

LOGFILE="/home/ubuntu/.openclaw/workspace/memory/linkedin-pa-agent.log"
WORKSPACE="/home/ubuntu/.openclaw/workspace"
OUTPUT_DIR="$WORKSPACE/content"
RESEARCH_DIR="$WORKSPACE/research"

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"
}

# Load .env if present to get OPENROUTER_API_KEY
if [ -f ".env" ]; then
  set -a
  . .env
  set +a
fi

log "Starting LinkedIn PA analyst-report cycle (v11 — creative queries)"

DATE=$(date -u +%Y-%m-%d)
TIME_STAMP=$(date -u +%H%M)

# Content types (6 buckets)
CONTENT_TYPES=("market-positioning" "technical-performance" "comparative-analysis" "implementation-decoder" "roadmap-brief" "developer-tips")

# Dedup: avoid recent research topics
RECENT_TOPICS="$RESEARCH_DIR/INDEX.md"
if [ -f "$RECENT_TOPICS" ]; then
  RECENT_QUERIES=$(grep -oE 'Title: .+' "$RECENT_TOPICS" 2>/dev/null | tail -20 | sed 's/Title: //' | tr '[:upper:]' '[:lower:]' | sort -u || true)
else
  RECENT_QUERIES=""
fi

# Select content type by hour rotation (ensures each appears 4x/day)
HOUR=$((10#$(date -u +%H)))
DAY_OF_WEEK=$(date -u +%u)
INDEX=$(( (DAY_OF_WEEK * 24 + HOUR) % 6 ))
SELECTED_TYPE="${CONTENT_TYPES[$INDEX]}"

# Static fallback query pool (high-quality, authoritative)
STATIC_QUERIES=(
  "IBM Planning Analytics Gartner Magic Quadrant 2026 site:gartner.com OR site:ibm.com"
  "IBM Planning Analytics TM1 engine architecture whitepaper site:ibm.com OR site:developer.ibm.com"
  "IBM Planning Analytics vs Oracle Hyperion comparison site:ibm.com OR site:oracle.com"
  "IBM Planning Analytics Cloud Pak for Data integration best practices site:ibm.com OR site:developer.ibm.com"
  "IBM Planning Analytics 2026 roadmap upcoming features site:ibm.com OR site:developer.ibm.com"
  "TM1 modeling optimization rules processes developer tips site:ibm.com OR site:developer.ibm.com"
)

# Dynamic query generation via LLM (preferred) — using direct OpenRouter API
log "Generating dynamic search query for: $SELECTED_TYPE"
PROMPT="You are a creative tech researcher focusing on IBM Planning Analytics (PA) and TM1. Generate a Google-style search query (20-150 chars) for: $SELECTED_TYPE.

Be exploratory, contrarian, or forward-looking. Avoid boring, repetitive queries.

Good examples:
- 'Planning Analytics compared to Snowflake for planning workloads 2025'
- 'Why TM1 may be losing to cloud-based planning platforms'
- 'Unexpected use cases of PA in retail beyond finance'
- 'Will Planning Analytics support Copilot in 2026?'
- 'TM1 performance benchmarks vs Oracle Hyperion on Azure'

Constraints:
- Must be relevant to PA/TM1 (can be indirect)
- Prefer sources: ibm.com, developer.ibm.com, gartner.com, forrester.com, tech blogs, VC sites (a16z, etc), arXiv, conference talks
- Include year 2025 or 2026 if possible
- Avoid overused phrases like 'roadmap', 'best practices', 'tips' (we know those)

Output ONLY the line starting with 'QUERY: '. No other text."

# Call OpenRouter directly to avoid cron hang
if [ -z "${OPENROUTER_API_KEY:-}" ]; then
  log "ERROR: OPENROUTER_API_KEY not set; cannot generate dynamic query"
  DYNAMIC_QUERY=""
else
  RESPONSE=$(curl -s -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"stepfun/step-3.5-flash:free","messages":[{"role":"system","content":"You output only a search query line starting with QUERY:"},{"role":"user","content":"'"$PROMPT"'"},{"role":"assistant","content":"QUERY:"}],"max_tokens":1024,"temperature":0.7}' \
    "https://openrouter.ai/api/v1/chat/completions")
  DYNAMIC_QUERY=$(echo "$RESPONSE" | jq -r '.choices[0].message.content // empty' 2>/dev/null || echo "")
fi

# Clean up
DYNAMIC_QUERY=$(echo "$DYNAMIC_QUERY" | tr -d '\"' | tr -d '\n' | xargs)

# Validation: allow queries that mention PA/TM1 OR adjacent terms (planning, OLAP, budgeting, forecasting, EPM)
if [ -z "$DYNAMIC_QUERY" ] || [ ${#DYNAMIC_QUERY} -lt 20 ] || [ ${#DYNAMIC_QUERY} -gt 200 ]; then
  log "Dynamic query invalid (length/empty); using static fallback"
  SELECTED_QUERY="${STATIC_QUERIES[$INDEX]}"
else
  QUERY_LOWER=$(echo "$DYNAMIC_QUERY" | tr '[:upper:]' '[:lower:]')
  if echo "$QUERY_LOWER" | grep -qiE 'planning analytics|TM1|PA |enterprise performance|EPM|OLAP|budgeting|forecasting|planning platform|in-memory cube'; then
    SELECTED_QUERY="$DYNAMIC_QUERY"
    log "Dynamic query: $SELECTED_QUERY"
  else
    log "Dynamic query lacks relevance; using static fallback"
    SELECTED_QUERY="${STATIC_QUERIES[$INDEX]}"
  fi
fi

# Additional dedup: avoid similarity to recent topics
if [ -n "$RECENT_QUERIES" ]; then
  QUERY_LOWER=$(echo "$SELECTED_QUERY" | tr '[:upper:]' '[:lower:]')
  for recent in $RECENT_QUERIES; do
    recent_prefix=$(echo "$recent" | cut -d' ' -f1-3)
    if echo "$QUERY_LOWER" | grep -q "$recent_prefix"; then
      log "Query too similar to recent ($recent); using static fallback"
      SELECTED_QUERY="${STATIC_QUERIES[$INDEX]}"
      break
    fi
  done
fi

log "Final query: $SELECTED_QUERY"
log "Content type: $SELECTED_TYPE"
