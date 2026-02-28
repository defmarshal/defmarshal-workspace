#!/usr/bin/env bash
# research-topics-today.sh — List today's research topics (for deduplication checks)
# Used by research-agent to avoid picking already-covered topics.
#
# Usage: scripts/research-topics-today.sh [--date YYYY-MM-DD] [--short]
# Output: one slug per line (--short) or human-readable list (default)

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
RESEARCH_DIR="$WORKSPACE/research"

TARGET_DATE=$(date -u +%Y-%m-%d)
SHORT=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --date) TARGET_DATE="$2"; shift 2 ;;
    --short) SHORT=true; shift ;;
    -h|--help) echo "Usage: $0 [--date YYYY-MM-DD] [--short]"; exit 0 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# Find dated reports for target date
mapfile -t files < <(ls -1t "$RESEARCH_DIR"/${TARGET_DATE}-*.md 2>/dev/null || true)

if [[ "$SHORT" == "true" ]]; then
  for f in "${files[@]}"; do
    basename "$f" .md | sed "s/^${TARGET_DATE}-//"
  done
  exit 0
fi

count="${#files[@]}"
echo "Research Topics — ${TARGET_DATE} (${count} reports)"
echo "$(printf '─%.0s' {1..50})"

if [[ $count -eq 0 ]]; then
  echo "  (none yet)"
  exit 0
fi

i=1
for f in "${files[@]}"; do
  slug=$(basename "$f" .md | sed "s/^${TARGET_DATE}-//")
  size=$(wc -c < "$f" 2>/dev/null || echo 0)
  size_kb=$(( size / 1024 ))
  printf "  %2d. %s (%dKB)\n" "$i" "$slug" "$size_kb"
  i=$(( i + 1 ))
done

echo ""
echo "Suggested next topics (not yet covered):"
# Common topic areas — filter out already-covered keywords
all_topics=(
  "cybersecurity" "satellite-internet" "spacex-starlink" "devops-2026"
  "kubernetes" "rust-programming" "typescript-5" "react-2026"
  "nextjs" "supabase" "postgres-2026" "redis" "vector-databases"
  "rag-retrieval" "langchain" "docker-2026" "github-actions"
  "terraform" "vercel-platform" "cloudflare-2026" "deno" "bun"
  "open-source-databases" "time-series-databases" "clickhouse"
  "manga-2026" "manhwa" "webtoon" "k-drama-2026" "j-drama"
  "fintech-2026" "crypto-2026" "defi" "thai-tech-ecosystem"
  "indonesia-tech" "vietnam-startup" "sea-ecommerce"
  "nvidia-blackwell" "arm-architecture" "risc-v"
)

covered_raw="${files[*]}"
suggestions=0
for topic in "${all_topics[@]}"; do
  if ! echo "$covered_raw" | grep -qi "$topic"; then
    echo "  → $topic"
    suggestions=$(( suggestions + 1 ))
    [[ $suggestions -ge 5 ]] && break
  fi
done
