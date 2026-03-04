#!/bin/bash
#
# rotate-logs.sh - Log rotation and compression for OpenClaw memory logs
#
# Features:
#   - Compresses logs older than 1 day or larger than 10 MB
#   - Keeps last 1000 lines uncompressed for fast access
#   - Uses flock to avoid conflicts with writing processes
#   - Idempotent and safe to run on live systems
#   - Moves compressed archives to memory/archive/
#
# Usage: ./rotate-logs.sh [--dry-run]
#

set -euo pipefail

# Configuration
MEMORY_DIR="${HOME}/.openclaw/workspace/memory"
ARCHIVE_DIR="${MEMORY_DIR}/archive"
ROTATE_LOG="${MEMORY_DIR}/rotate-logs.log"
MAX_SIZE_MB=10
MAX_AGE_DAYS=1
KEEP_LINES=1000
LOCK_FILE="/tmp/rotate-logs.lock"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Logging function
log() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} $*" | tee -a "${ROTATE_LOG}"
}

log_info() {
    log "${GREEN}[INFO]${NC} $*"
}

log_warn() {
    log "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    log "${RED}[ERROR]${NC} $*"
}

# Check if a file is currently open by any process
is_file_open() {
    local file="$1"
    lsof +f -- "$file" >/dev/null 2>&1
}

# Get file age in days
get_file_age_days() {
    local file="$1"
    local now
    local file_mtime
    now=$(date +%s)
    file_mtime=$(stat -c %Y "$file" 2>/dev/null || echo "$now")
    echo $(( (now - file_mtime) / 86400 ))
}

# Get file size in MB
get_file_size_mb() {
    local file="$1"
    local size_bytes
    size_bytes=$(stat -c %s "$file" 2>/dev/null || echo 0)
    echo $(( size_bytes / 1048576 ))
}

# Rotate a single log file
rotate_file() {
    local file="$1"
    local basename
    local timestamp
    local archive_name
    local temp_file
    
    basename=$(basename "$file")
    timestamp=$(date '+%Y%m%d-%H%M%S')
    archive_name="${basename%.log}-${timestamp}.log.gz"
    
    # Check if file is being written to
    if is_file_open "$file"; then
        log_warn "Skipping $basename - file is currently open by a process"
        return 0
    fi
    
    local age_days
    local size_mb
    age_days=$(get_file_age_days "$file")
    size_mb=$(get_file_size_mb "$file")
    
    # Determine if rotation is needed
    local should_rotate=false
    local reason=""
    
    if [[ $size_mb -ge $MAX_SIZE_MB ]]; then
        should_rotate=true
        reason="size (${size_mb}MB >= ${MAX_SIZE_MB}MB)"
    elif [[ $age_days -ge $MAX_AGE_DAYS ]]; then
        should_rotate=true
        reason="age (${age_days} days >= ${MAX_AGE_DAYS} days)"
    fi
    
    if [[ "$should_rotate" == "false" ]]; then
        return 0
    fi
    
    log_info "Rotating $basename (${size_mb}MB, ${age_days} days old) - reason: $reason"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would compress $basename to archive/$archive_name"
        log_info "[DRY-RUN] Would keep last $KEEP_LINES lines in $basename"
        return 0
    fi
    
    # Create a temporary file for the compressed content
    temp_file=$(mktemp)
    
    # Compress the entire file content to archive
    if gzip -c "$file" > "${ARCHIVE_DIR}/${archive_name}"; then
        log_info "Compressed $basename to archive/${archive_name}"
        
        # Get total lines in file
        local total_lines
        total_lines=$(wc -l < "$file" || echo 0)
        
        # Keep only the last N lines in the original file
        if [[ $total_lines -gt $KEEP_LINES ]]; then
            tail -n "$KEEP_LINES" "$file" > "$temp_file"
            mv "$temp_file" "$file"
            log_info "Truncated $basename to last $KEEP_LINES lines (was $total_lines lines)"
        else
            log_info "Kept $basename as-is ($total_lines lines <= $KEEP_LINES)"
        fi
    else
        log_error "Failed to compress $basename"
        rm -f "$temp_file"
        return 1
    fi
    
    return 0
}

# Main function
main() {
    log_info "=========================================="
    log_info "Starting log rotation (dry-run: $DRY_RUN)"
    log_info "=========================================="
    
    # Ensure archive directory exists
    mkdir -p "$ARCHIVE_DIR"
    
    # Acquire lock to prevent concurrent runs
    exec 200>"$LOCK_FILE"
    if ! flock -n 200; then
        log_error "Another instance is already running (lock: $LOCK_FILE)"
        exit 1
    fi
    
    # Find all .log files (excluding already compressed and rotate-logs.log itself)
    local log_files
    local total_files=0
    local rotated_files=0
    local skipped_files=0
    local total_size_before=0
    local total_size_after=0
    
    log_info "Scanning for .log files in $MEMORY_DIR..."
    
    while IFS= read -r -d '' file; do
        # Skip the rotation log itself
        if [[ "$(basename "$file")" == "rotate-logs.log" ]]; then
            continue
        fi
        
        # Skip files in archive directory
        if [[ "$file" == "$ARCHIVE_DIR"* ]]; then
            continue
        fi
        
        ((total_files++)) || true
        
        # Get size before rotation
        local file_size
        file_size=$(stat -c %s "$file" 2>/dev/null || echo 0)
        total_size_before=$((total_size_before + file_size))
        
        # Try to rotate the file
        if rotate_file "$file"; then
            if [[ "$DRY_RUN" != "true" ]]; then
                ((rotated_files++)) || true
                # Get size after rotation
                local new_size
                new_size=$(stat -c %s "$file" 2>/dev/null || echo 0)
                total_size_after=$((total_size_after + new_size))
            fi
        else
            ((skipped_files++)) || true
        fi
    done < <(find "$MEMORY_DIR" -maxdepth 1 -name "*.log" -type f -print0 2>/dev/null)
    
    # Also check subdirectories (like evolution/, knowledge/)
    while IFS= read -r -d '' file; do
        # Skip the rotation log itself
        if [[ "$(basename "$file")" == "rotate-logs.log" ]]; then
            continue
        fi
        
        # Skip files in archive directory
        if [[ "$file" == "$ARCHIVE_DIR"* ]]; then
            continue
        fi
        
        ((total_files++)) || true
        
        # Get size before rotation
        local file_size
        file_size=$(stat -c %s "$file" 2>/dev/null || echo 0)
        total_size_before=$((total_size_before + file_size))
        
        # Try to rotate the file
        if rotate_file "$file"; then
            if [[ "$DRY_RUN" != "true" ]]; then
                ((rotated_files++)) || true
                # Get size after rotation
                local new_size
                new_size=$(stat -c %s "$file" 2>/dev/null || echo 0)
                total_size_after=$((total_size_after + new_size))
            fi
        else
            ((skipped_files++)) || true
        fi
    done < <(find "$MEMORY_DIR" -mindepth 2 -maxdepth 3 -name "*.log" -type f -print0 2>/dev/null)
    
    # Report summary
    log_info "=========================================="
    log_info "Rotation complete!"
    log_info "  Total log files scanned: $total_files"
    log_info "  Files rotated: $rotated_files"
    log_info "  Files skipped (open or small): $skipped_files"
    
    if [[ "$DRY_RUN" != "true" ]]; then
        local saved_bytes=$((total_size_before - total_size_after))
        local saved_mb=$((saved_bytes / 1048576))
        log_info "  Space saved: ~${saved_mb} MB"
        log_info "  Archive directory: $ARCHIVE_DIR"
    fi
    log_info "=========================================="
    
    # Release lock (automatic on script exit)
    flock -u 200
}

# Run main function
main "$@"
