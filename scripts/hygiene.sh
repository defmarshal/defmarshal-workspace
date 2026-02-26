#!/usr/bin/env bash
# Workspace hygiene maintenance: logs, branches, downloads, builds, temp files, SQLite vacuum
# Default action: dry-run (shows what would be done). Use --execute to apply changes.

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

EXECUTE=false
if [ "${1:-}" = "--execute" ]; then
  EXECUTE=true
fi

log() {
  if [ "$EXECUTE" = true ]; then
    echo "✅ $*"
  else
    echo "🔍 Would: $*"
  fi
}

warn() { echo "⚠️  $*"; }
error() { echo "❌ $*"; }

# 1. Log rotation (memory/*.log older than 7 days)
echo "=== Log Rotation ==="
find memory/ -name '*.log' -type f -mtime +7 2>/dev/null | while read -r log; do
  if [ "$EXECUTE" = true ]; then
    gzip -9 "$log" && echo "Compressed: $log"
  else
    echo "$log (would compress)"
  fi
done

# 2. Stale Git branches (unmerged >30 days)
echo -e "\n=== Stale Branches ==="
CURRENT_BRANCH=$(git branch --show-current)
git for-each-ref --format='%(refname:short) %(committerdate:unix)' refs/heads/ | while read -r branch ts; do
  if [ "$branch" = "$CURRENT_BRANCH" ] || [ "$branch" = "master" ] || [ "$branch" = "main" ]; then
    continue
  fi
  AGE_DAYS=$(( ( $(date +%s) - ts ) / 86400 ))
  if [ $AGE_DAYS -gt 30 ]; then
    if [ "$EXECUTE" = true ]; then
      git branch -D "$branch" && echo "Deleted branch: $branch ($AGE_DAYS days old)"
    else
      echo "$branch (would delete, $AGE_DAYS days old)"
    fi
  fi
done

# 3. Downloads pruning (older than 30 days)
echo -e "\n=== Old Downloads ==="
if [ -d "downloads" ]; then
  find downloads/ -type f -mtime +30 2>/dev/null | while read -r file; do
    if [ "$EXECUTE" = true ]; then
      rm -f "$file" && echo "Removed: $file"
    else
      echo "$file (would remove)"
    fi
  done
else
  echo "No downloads/ directory"
fi

# 4. Build artifacts cleanup (keep latest 10 in builds/, apps/*/dist/)
echo -e "\n=== Build Artifacts ==="
if [ -d "builds" ]; then
  # Keep 10 newest directories
  cd builds
  ALL_DIRS=$(find . -maxdepth 1 -type d -name '*' ! -name '.' | sort -r)
  KEEP=10
  COUNT=0
  echo "$ALL_DIRS" | while read -r dir; do
    COUNT=$((COUNT+1))
    if [ $COUNT -gt $KEEP ]; then
      if [ "$EXECUTE" = true ]; then
        rm -rf "$dir" && echo "Removed build: $dir"
      else
        echo "$dir (would remove)"
      fi
    fi
  done
  cd "$WORKSPACE"
fi

# 5. Temporary files (common cruft)
echo -e "\n=== Temporary Files ==="
TEMP_PATTERNS=( '*.tmp' '*.bak' 'Thumbs.db' '.DS_Store' '.localized' '*-cache' )
for pat in "${TEMP_PATTERNS[@]}"; do
  find . -type f -name "$pat" 2>/dev/null | while read -r f; do
    # Skip within .git and node_modules
    if [[ "$f" == .git/* ]] || [[ "$f" == */node_modules/* ]] || [[ "$f" == */vendor/* ]]; then
      continue
    fi
    if [ "$EXECUTE" = true ]; then
      rm -f "$f" && echo "Removed temp: $f"
    else
      echo "$f (would remove)"
    fi
  done
done

# 6. SQLite vacuum (memory stores)
echo -e "\n=== SQLite Vacuum ==="
for db in ~/.openclaw/memory/*.sqlite; do
  [ -f "$db" ] || continue
  if [ "$EXECUTE" = true ]; then
    sqlite3 "$db" "VACUUM;" && echo "Vacuumed: $db"
  else
    echo "$db (would vacuum)"
  fi
done

echo -e "\nDone. Use --execute to apply changes."
