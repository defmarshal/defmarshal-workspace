#!/usr/bin/env bash
# find-large-files.sh — Find large files in the workspace, optionally older than N days
# Usage: find-large-files.sh [--size SIZE] [--days N] [--dir DIR] [--top N]
# Examples:
#   find-large-files.sh                   # files > 10MB in workspace
#   find-large-files.sh --size 50M        # files > 50MB
#   find-large-files.sh --days 30         # files > 10MB AND older than 30 days
#   find-large-files.sh --size 5M --days 7 --dir downloads/
#   find-large-files.sh --top 20          # show top 20 results

set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/ubuntu/.openclaw/workspace}"
MIN_SIZE="10M"
MIN_DAYS=""
SEARCH_DIR="$WORKSPACE"
TOP_N=15

# Colors
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

log()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Find large files in the workspace.

Options:
  --size SIZE     Minimum file size (default: 10M). Examples: 5M, 100M, 1G
  --days N        Only show files older than N days (optional)
  --dir PATH      Directory to search (default: workspace root)
  --top N         Max number of results to show (default: 15)
  -h, --help      Show this help

Examples:
  $(basename "$0")                    # Files > 10MB anywhere in workspace
  $(basename "$0") --size 5M          # Files > 5MB
  $(basename "$0") --days 30          # Files > 10MB older than 30 days
  $(basename "$0") --size 50M --days 7 --dir downloads/
  $(basename "$0") --top 30           # Show up to 30 results
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --size)   MIN_SIZE="$2"; shift 2 ;;
        --days)   MIN_DAYS="$2"; shift 2 ;;
        --dir)    SEARCH_DIR="$2"; shift 2 ;;
        --top)    TOP_N="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown option: $1"; usage; exit 1 ;;
    esac
done

# Resolve relative path
if [[ "$SEARCH_DIR" != /* ]]; then
    SEARCH_DIR="$WORKSPACE/$SEARCH_DIR"
fi

if [[ ! -d "$SEARCH_DIR" ]]; then
    echo "Error: directory '$SEARCH_DIR' not found." >&2
    exit 1
fi

# Build find command
FIND_ARGS=("$SEARCH_DIR" -type f -size "+${MIN_SIZE}")

# Exclude noisy dirs
FIND_ARGS+=( ! -path "*/node_modules/*" ! -path "*/.git/objects/*" ! -path "*/downloads/*" )

if [[ -n "$MIN_DAYS" ]]; then
    FIND_ARGS+=(-mtime "+${MIN_DAYS}")
fi

echo ""
echo -e "${CYAN}🔍 Large Files Scanner${NC}"
echo -e "   Directory : $SEARCH_DIR"
echo -e "   Min size  : $MIN_SIZE"
[[ -n "$MIN_DAYS" ]] && echo -e "   Older than: ${MIN_DAYS} days"
echo -e "   Top       : $TOP_N results"
echo ""

# Run find, sort by size descending
results=$(find "${FIND_ARGS[@]}" -printf "%s\t%TY-%Tm-%Td\t%p\n" 2>/dev/null | sort -rn | head -"$TOP_N")

if [[ -z "$results" ]]; then
    log "No files matching criteria found."
    exit 0
fi

count=$(echo "$results" | wc -l)
echo -e "${YELLOW}Found $count file(s):${NC}"
echo ""
printf "%-10s  %-12s  %s\n" "SIZE" "MODIFIED" "PATH"
printf "%-10s  %-12s  %s\n" "----------" "------------" "----"

while IFS=$'\t' read -r bytes date path; do
    # Human-readable size
    if   (( bytes >= 1073741824 )); then size=$(echo "scale=1; $bytes/1073741824" | bc)G
    elif (( bytes >= 1048576 )); then    size=$(echo "scale=1; $bytes/1048576" | bc)M
    elif (( bytes >= 1024 )); then       size=$(echo "scale=1; $bytes/1024" | bc)K
    else                                  size="${bytes}B"
    fi

    # Shorten path relative to workspace
    short_path="${path#$WORKSPACE/}"

    # Color code by size
    if   (( bytes >= 524288000 )); then col="$RED"      # ≥ 500MB
    elif (( bytes >= 104857600 )); then col="$YELLOW"   # ≥ 100MB
    else                                 col="$NC"
    fi

    printf "${col}%-10s${NC}  %-12s  %s\n" "$size" "$date" "$short_path"
done <<< "$results"

echo ""
total_bytes=$(echo "$results" | awk '{sum += $1} END {print sum}')
if   (( total_bytes >= 1073741824 )); then total_hr=$(echo "scale=1; $total_bytes/1073741824" | bc)G
elif (( total_bytes >= 1048576 )); then    total_hr=$(echo "scale=1; $total_bytes/1048576" | bc)M
elif (( total_bytes >= 1024 )); then       total_hr=$(echo "scale=1; $total_bytes/1024" | bc)K
else                                        total_hr="${total_bytes}B"
fi

echo -e "${GREEN}Total: ${total_hr} across ${count} file(s)${NC}"
echo ""
