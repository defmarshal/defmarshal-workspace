#!/usr/bin/env bash
# Check write permissions on critical directories

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "Permission Check for Critical Directories"
echo "-----------------------------------------"

check_dir() {
  dir="$1"
  desc="$2"
  if [ -d "$dir" ]; then
    if [ -w "$dir" ]; then
      echo "✅ $desc: $dir (writable)"
    else
      echo "❌ $desc: $dir (NOT writable)"
    fi
  else
    echo "⚠️  $desc: $dir (missing)"
  fi
}

check_dir "$WORKSPACE" "Workspace"
check_dir "$WORKSPACE/research" "Research output"
check_dir "$WORKSPACE/content" "Content output"
check_dir "$WORKSPACE/apps/research-hub/public/research" "Research Hub public"
check_dir "$WORKSPACE/memory" "Memory/index"

# Check Obsidian vault from OBSIDIAN_VAULT or default
VAULT="${OBSIDIAN_VAULT:-$HOME/obsidian-vault}"
check_dir "$VAULT/Content" "Obsidian Content (if configured)"

echo
echo "If any are not writable, fix with: sudo chown -R ubuntu:ubuntu <path>"
