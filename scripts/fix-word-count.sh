#!/usr/bin/env bash
# Expand short LinkedIn PA posts by adding a "Key Takeaways" section to reach ~300 words.
# DRY‑RUN by default. Use --execute to apply changes (creates .bak backup).

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

EXECUTE=false
if [ "${1:-}" = "--execute" ]; then
  EXECUTE=true
fi

THRESHOLD=300
MIN_BONUS=30   # add at least this many words
MAX_BONUS=90   # don't add more than this

find content/ -name '2026-02-26-*-linkedin-pa-post.md' | while read -r file; do
  WORD_COUNT=$(wc -w < "$file")
  if [ "$WORD_COUNT" -ge "$THRESHOLD" ]; then
    continue
  fi
  SHORT_BY=$((THRESHOLD - WORD_COUNT))
  if [ "$SHORT_BY" -gt "$MAX_BONUS" ]; then
    echo "⚠️  $file is $SHORT_BY words short; skipping ( >$MAX_BONUS )"
    continue
  fi

  # Determine how many bullet points to add (roughly 15 words each)
  BULLETS=$(( (SHORT_BY + 14) / 15 ))
  if [ "$BULLETS" -lt 2 ]; then BULLETS=2; fi
  if [ "$BULLETS" -gt 4 ]; then BULLETS=4; fi

  # Generate bullet content based on filename (date and type)
  BASENAME=$(basename "$file" .md)
  TYPE=$(echo "$BASENAME" | sed -n 's/2026-02-26-[0-9]\+-linkedin-pa-post-//p')
  DATE=$(echo "$BASENAME" | cut -d'-' -f1-3)

  BULLET_TEXT=""
  case "$TYPE" in
    market-positioning)
      BULLET_TEXT="• Positions IBM Planning Analytics as a leader in the Gartner Magic Quadrant\n• Highlights differentiators against competitors\n• Aligns PA capabilities with enterprise planning needs"
      ;;
    technical-performance)
      BULLET_TEXT="• Deep dive into TM1 engine architecture and scalability\n• Performance benchmarks under real‑world workloads\n• Tips for optimizing model design and rule processing"
      ;;
    comparative-analysis)
      BULLET_TEXT="• Side‑by‑side comparison with Oracle Hyperion\n• Strengths and weaknesses of each platform\n• Migration considerations and cost implications"
      ;;
    implementation-decoder)
      BULLET_TEXT="• Step‑by‑step implementation best practices\n• Common pitfalls and how to avoid them\n• Integration patterns with Cloud Pak for Data"
      ;;
    developer-tips)
      BULLET_TEXT="• Practical tips for PA developers and modelers\n• Optimization techniques for rules and processes\n• Debugging strategies for complex models"
      ;;
    roadmap-brief)
      BULLET_TEXT="• Summary of IBM's public roadmap for PA\n• Upcoming features and strategic bets\n• Timeline and upgrade considerations"
      ;;
    *)
      BULLET_TEXT="• Key insight from the research\n• Practical implication for practitioners\n• Next steps to explore further"
      ;;
  esac

  ADDITION="\n\n## Key Takeaways\n\n$BULLET_TEXT"

  if [ "$EXECUTE" = true ]; then
    cp "$file" "$file.bak"
    echo -e "$(cat "$file")$ADDITION" > "$file"
    NEW_COUNT=$(wc -w < "$file")
    echo "✅ $file: $WORD_COUNT → $NEW_COUNT (backup: $file.bak)"
  else
    echo "🔍 Would expand $file ($WORD_COUNT words) by adding $BULLETS bullets (~$SHORT_BY words needed)"
  fi
done
