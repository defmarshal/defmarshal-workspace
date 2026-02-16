#!/usr/bin/env bash
# cleanup-downloads.sh - Safely remove old completed torrents from downloads/
# Retention policy: delete files/directories older than N days (default 30)
# Always dry-run by default; use --execute to actually delete.

set -euo pipefail

DOWNLOADS_DIR="/home/ubuntu/.openclaw/workspace/downloads"
RETENTION_DAYS=30
DRY_RUN=true

# Colors for output (optional)
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

warn() {
    echo -e "${RED}[WARN]${NC} $*"
}

usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Safely clean up old downloads from the downloads directory.

Options:
  --days N          Set retention period in days (default: $RETENTION_DAYS)
  --execute         Actually delete files (default: dry-run only)
  --verbose         Show detailed file list
  -h, --help        Show this help message

Examples:
  $0                       # Dry-run: show what would be deleted (30 days)
  $0 --days 60             # Show files older than 60 days
  $0 --execute             # Actually delete files older than 30 days
  $0 --days 45 --execute   # Delete files older than 45 days
EOF
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --days)
            RETENTION_DAYS="$2"
            shift 2
            ;;
        --execute)
            DRY_RUN=false
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            warn "Unknown option: $1"
            usage
            ;;
    esac
done

# If VERBOSE not set, default to false
VERBOSE=${VERBOSE:-false}

if [[ ! -d "$DOWNLOADS_DIR" ]]; then
    warn "Downloads directory not found: $DOWNLOADS_DIR"
    exit 1
fi

log "Scanning $DOWNLOADS_DIR for files older than $RETENTION_DAYS days..."
if [[ "$DRY_RUN" == "true" ]]; then
    log "Running in DRY-RUN mode. No files will be deleted."
    log "Add --execute to perform deletion."
fi

# Verbose: list all files to be scanned
if [[ "$VERBOSE" == "true" ]]; then
    echo "Files in downloads directory (eligible types only):"
    find "$DOWNLOADS_DIR" -mindepth 1 -type f \( -name "*.mkv" -o -name "*.mp4" -o -name "*.avi" -o -name "*.torrent" -o -name "*.nfo" -o -name "*.txt" -o -name "*.jpg" -o -name "*.png" \) -exec ls -lh {} \; 2>/dev/null || true
    echo ""
fi

# Find files older than retention period
# We'll find files and directories (but only delete empty dirs after files removed)
found_count=0
to_delete_size=0

while IFS= read -r -d '' filepath; do
    if [[ -f "$filepath" ]]; then
        age_days=$(( ( $(date +%s) - $(stat -c %Y "$filepath") ) / 86400 ))
        if [[ $age_days -ge $RETENTION_DAYS ]]; then
            ((found_count++))
            size=$(du -h "$filepath" | cut -f1)
            to_delete_size=$(( to_delete_size + $(stat -c %s "$filepath") ))
            if [[ "$DRY_RUN" == "true" ]]; then
                echo "  Would delete: $filepath (age: ${age_days}d, size: ${size})"
            else
                echo "  Deleting: $filepath (age: ${age_days}d, size: ${size})"
                rm -f "$filepath"
            fi
        fi
    fi
done < <(find "$DOWNLOADS_DIR" -mindepth 1 -type f \( -name "*.mkv" -o -name "*.mp4" -o -name "*.avi" -o -name "*.torrent" -o -name "*.nfo" -o -name "*.txt" -o -name "*.jpg" -o -name "*.png" \) -print0)

# After deleting files, remove empty directories
if [[ "$DRY_RUN" == "false" ]]; then
    log "Removing empty directories..."
    find "$DOWNLOADS_DIR" -mindepth 1 -type d -empty -delete
fi

# Summary
log "Scan complete."
if [[ $found_count -eq 0 ]]; then
    log "No files older than $RETENTION_DAYS days found."
else
    human_size=$(numfmt --to=iec-i --suffix=B $to_delete_size 2>/dev/null || echo "${to_delete_size}B")
    if [[ "$DRY_RUN" == "true" ]]; then
        log "Found $found_count old files (total size: $human_size) that would be deleted."
    else
        log "Deleted $found_count files (total size: $human_size)."
    fi
fi

# Warn if downloads dir is still large
current_size=$(du -sh "$DOWNLOADS_DIR" 2>/dev/null | cut -f1 || echo "0")
log "Current downloads directory size: ${current_size}"
