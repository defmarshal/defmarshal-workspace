#!/usr/bin/env bash
# Show top recent commits with agent tags
# Usage: quick top-commits [N]

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
N="${1:-10}"

git -C "$WORKSPACE" log --oneline -"$N" | sed -E 's/^([a-f0-9]+) ([^:]+):?/\2/' | awk '
  {
    agent=$1;
    msg=substr($0, index($0,$2));
    printf "%-12s %s\n", agent, msg
  }
' | head -n "$N"
