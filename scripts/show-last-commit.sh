#!/usr/bin/env bash
# Show detailed information about the last commit

WORKSPACE="/home/ubuntu/.openclaw/workspace"

cd "$WORKSPACE" || exit 1

# Get last commit details
COMMIT_HASH=$(git log -1 --format="%H")
COMMIT_MSG=$(git log -1 --format="%s")
COMMIT_AUTHOR=$(git log -1 --format="%an")
COMMIT_DATE=$(git log -1 --format="%cd" --date="iso-local")
COMMIT_BODY=$(git log -1 --format="%b")

echo "Last Commit Details"
echo "-------------------"
printf "Hash:    %s\n" "$COMMIT_HASH"
printf "Author:  %s\n" "$COMMIT_AUTHOR"
printf "Date:    %s\n" "$COMMIT_DATE"
echo "Message: $COMMIT_MSG"
echo

# Show changed files with stats
echo "Changed files:"
git diff-tree --no-commit-id --name-status -r HEAD | while read -r status file; do
  printf "  %-12s %s\n" "$status" "$file"
done

echo
echo "Statistics:"
git diff-tree --no-commit-id --numstat -r HEAD | awk '{added+=$1; removed+=$2; count++} END {printf "  Files: %d\n  Lines added: %d\n  Lines removed: %d\n  Total change: %d\n", count, added, removed, added+removed}'

# Show commit body if present
if [ -n "$COMMIT_BODY" ]; then
  echo
  echo "Full message:"
  echo "$COMMIT_BODY" | sed 's/^/  /'
fi
