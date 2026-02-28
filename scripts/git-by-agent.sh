#!/usr/bin/env bash
set -euo pipefail
# Show recent git commits grouped by agent prefix

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "Recent Commits by Agent (last 30)"
echo "----------------------------------"

cd "$WORKSPACE" || exit 1

# Collect and classify
declare -A counts
declare -A samples

while IFS= read -r line; do
  hash=$(echo "$line" | awk '{print $1}')
  subject=$(echo "$line" | cut -d' ' -f2-)
  
  if echo "$subject" | grep -qE '^[a-z]+:'; then
    prefix=$(echo "$subject" | cut -d':' -f1)
  else
    prefix="other"
  fi
  
  counts["$prefix"]=$((counts["$prefix"]+1))
  # Keep sample (first 3 seen)
  if [ ${samples["$prefix"]+_} != "" ] && [ ${#samples["$prefix"]} -lt 3 ]; then
    samples["$prefix"]="${samples["$prefix"]}"$'\n'"  $line"
  elif [ -z "${samples["$prefix"]+_}" ]; then
    samples["$prefix"]="$line"
  fi
done < <(git log --oneline -30)

# Print summary sorted by count descending
for prefix in "${!counts[@]}"; do
  echo "${counts[$prefix]}    $prefix"
done | sort -nr | while read -r count prefix; do
  echo -e "$count\t$prefix"
  if [ -n "${samples[$prefix]+_}" ]; then
    echo "${samples[$prefix]}"
  fi
  echo
done
