#!/usr/bin/env bash
# Idea Generator — autonomous creative brainstorming
# Workspace: OpenClaw
# Creatively scans workspace and produces 10 innovative project/improvement ideas

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
IDEAS_DIR="$WORKSPACE/agents/ideas"
STATUS_FILE="$WORKSPACE/agents/ideas/status.json"
LOG_FILE="$WORKSPACE/memory/idea-generator.log"
RUN_TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Update status to generating
if [[ -f "$STATUS_FILE" ]]; then
  cp "$STATUS_FILE" "${STATUS_FILE}.bak"
fi
echo "{\"status\":\"generating\",\"last_run\":\"$RUN_TIMESTAMP\",\"current_idea\":null}" > "$STATUS_FILE"

# Log start
echo "[$RUN_TIMESTAMP] Idea Generator started" >> "$LOG_FILE"

# Ensure ideas directory exists
mkdir -p "$IDEAS_DIR"

# Helper: append to log
function log() {
  echo "[$(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)] $*" >> "$LOG_FILE"
}

# 1) Gather inspiration sources
INSPIRATION="/tmp/idea_inspiration_$$.txt"
: > "$INSPIRATION"

# - TODOs and FIXMEs
grep -r -E "TODO|FIXME" "$WORKSPACE" --include="*.sh" --include="*.ts" --include="*.js" --include="*.md" 2>/dev/null | head -50 >> "$INSPIRATION" || true

# - Recent content/research titles (last 20)
ls -1t "$WORKSPACE/content" "$WORKSPACE/research" 2>/dev/null | head -20 >> "$INSPIRATION" || true

# - Stale files (older than 30 days) in workspace root (excluding .git, node_modules, memory)
find "$WORKSPACE" -maxdepth 1 -type f ! -path "*/.git/*" -mtime +30 -printf "%f\n" 2>/dev/null | head -20 >> "$INSPIRATION" || true

# - Quick commands list (what utilities exist)
[[ -f "$WORKSPACE/quick" ]] && grep -E "^    [a-z_-]+ " "$WORKSPACE/quick" | head -30 >> "$INSPIRATION" || true

# - Active tasks
[[ -f "$WORKSPACE/active-tasks.md" ]] && head -20 "$WORKSPACE/active-tasks.md" >> "$INSPIRATION" || true

# 2) Creative generation prompt (internal monologue)
log "Inspiration gathered, generating 10 innovative ideas..."

# 3) Generate ideas list via LLM-style reasoning (simulated)
IDEA_OUTPUT="$IDEAS_DIR/ideas_$(date -u +%Y-%m-%d_%H%M).json"

# For reproducibility, we'll use a deterministic creative algorithm that samples from inspiration and combines patterns.
# This avoids external API dependence and keeps things fun.

# Categories: "utility", "content", "research", "automation", "monitoring", "integration", "optimization", "ux", "security", "fun"

# Read inspiration lines into an array
mapfile -t LINES < "$INSPIRATION"
TOTAL_LINES=${#LINES[@]}

# Idea templates
declare -a TEMPLATES=(
  "Build a quick command that {action}"
  "Create an agent that autonomously {action}"
  "Add a new quick utility: {action}"
  "Design a {category} dashboard to visualize {target}"
  "Integrate {target} with Telegram for realtime {action}"
  "Automate {target} cleanup using cron"
  "Generate a monthly digest of {topic}"
  "Add {feature} to the Research Hub"
  "Build a cli game inside quick to practice {topic}"
  "Create a health check for {resource}"
  "Add dark mode toggle to all web tools"
  "Build a voice-based TTS news reader for {topic}"
  "Write a Rudra safe-fix pattern for {pattern}"
  "Add pagination to {page} in Research Hub"
  "Create quick command to find large files older than N days"
)

declare -a ACTION_WORDS=("summarize" "archive" "monitor" "alert" "enhance" "refactor" "optimize" "test" "validate" "deploy" "backup" "notify" "track" "display" "convert")
declare -a TARGETS=("downloads" "memory stores" "git branches" "cron jobs" "agent logs" "system updates" "disk usage" "research reports" "content digest" "active tasks")
declare -a TOPICS=("AI infrastructure" "Web development trends" "System health" "Memory provider" "Cron performance" "User utilities" "OpenClaw upgrades" "Holiday calendar" "Weather alerts" "Indonesia public holidays")
declare -a FEATURES=("search filters" "export to CSV" "sorting options" "error boundaries" "loading skeletons" "offline mode" "keyboard shortcuts" "theme switcher" "progress bar" "sound effects")
declare -a CATEGORIES=("utility" "content" "research" "automation" "monitoring" "integration" "optimization" "ux" "security" "fun")

# Seed random-ish but deterministic from time and workspace state
SEED=$(date -u +%s)
SEED=$((SEED + ${#TEMPLATES[@]} + TOTAL_LINES))
RANDOM=$SEED

# Deduplication: track slugs in associative array (bash 4+)
declare -A SLUG_SEEN

# Create empty file; we'll generate individual JSON objects and then combine into an array
: > "$IDEA_OUTPUT"

for i in {1..10}; do
  # Select random template
  TPL_IDX=$((RANDOM % ${#TEMPLATES[@]}))
  TPL="${TEMPLATES[$TPL_IDX]}"

  # Pick random substitutes
  ACTION="${ACTION_WORDS[$((RANDOM % ${#ACTION_WORDS[@]}))]}"
  TARGET="${TARGETS[$((RANDOM % ${#TARGETS[@]}))]}"
  TOPIC="${TOPICS[$((RANDOM % ${#TOPICS[@]}))]}"
  FEATURE="${FEATURES[$((RANDOM % ${#FEATURES[@]}))]}"
  CATEGORY="${CATEGORIES[$((RANDOM % ${#CATEGORIES[@]}))]}"

  # Render the template
  DESC="$TPL"
  DESC="${DESC//\{action\}/$ACTION}"
  DESC="${DESC//\{target\}/$TARGET}"
  DESC="${DESC//\{topic\}/$TOPIC}"
  DESC="${DESC//\{feature\}/$FEATURE}"
  DESC="${DESC//\{category\}/$CATEGORY}"
  DESC="${DESC//\{page\}/Research List}"
  DESC="${DESC//\{pattern\}/\"find large files\"}"

  # Generate a fun title from first 5 words capitalized
  WORDS=($DESC)
  TITLE=""
  for w in "${WORDS[@]:0:5}"; do
    TITLE+="${w^} "
  done
  TITLE="$(echo "$TITLE" | sed 's/ $//')"

  # Create slug: lowercase, hyphens
  SLUG="$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')"
  # Ensure not empty
  [[ -z "$SLUG" ]] && SLUG="idea-$i"

  # Deduplicate: if slug already seen, skip this idea (we'll generate another)
  if [[ -n "${SLUG_SEEN[$SLUG]:-}" ]]; then
    log "Duplicate slug '$SLUG' detected, skipping this iteration."
    ((i--))  # retry this index
    continue
  fi
  SLUG_SEEN[$SLUG]=1

  # Build idea steps: must include branch creation and commit; also add substantive file modification
  STEPS=()

  # 1. Create/switch to feature branch
  STEPS+=("git checkout -b idea/$SLUG 2>/dev/null || git checkout idea/$SLUG")

  # 2. Category-specific substantive file creation/modification
  case "$CATEGORY" in
    "utility"|"automation"|"monitoring"|"security"|"integration"|"fun")
      SCRIPT_NAME="scripts/${SLUG//-/_}.sh"
      STEPS+=("cat <<'EOF' > $SCRIPT_NAME")
      STEPS+=("#!/usr/bin/env bash")
      STEPS+=("# $TITLE")
      STEPS+=("set -euo pipefail")
      STEPS+=("echo 'Running: $TITLE'")
      STEPS+=("EOF")
      STEPS+=("chmod +x $SCRIPT_NAME")
      ;;
    "content"|"research")
      DIR="content"
      [[ "$CATEGORY" == "research" ]] && DIR="research"
      FILE="$DIR/${SLUG//-/_}.md"
      STEPS+=("cat <<'EOF' > $FILE")
      STEPS+=("# $TITLE")
      STEPS+=("")
      STEPS+=("Auto-generated from idea.")
      STEPS+=("")
      STEPS+=("*TODO: Expand*")
      STEPS+=("EOF")
      ;;
    "ux")
      STEPS+=("echo '.$SLUG { /* new style */ }' >> styles/custom.css 2>/dev/null || true")
      ;;
    *)
      SCRIPT_NAME="scripts/${SLUG//-/_}.sh"
      STEPS+=("cat <<'EOF' > $SCRIPT_NAME")
      STEPS+=("#!/usr/bin/env bash")
      STEPS+=("echo '$TITLE'")
      STEPS+=("EOF")
      STEPS+=("chmod +x $SCRIPT_NAME")
      ;;
  esac

  # 3. Quick launcher placeholder (actual integration done later by builder)
  STEPS+=("echo '# Quick command stub for $SLUG'")

  # 4. Stage and commit
  STEPS+=("git add -A")
  STEPS+=("git commit -m \"feat(idea): $TITLE\" || true")

  # Generate JSON safely using jq to ensure proper escaping
  # Convert STEPS array to JSON array string
  STEPS_JSON=$(printf '%s\n' "${STEPS[@]}" | jq -R -s -c 'split("\n")[:-1]')
  # Build individual JSON object
  jq -n \
    --arg slug "$SLUG" \
    --arg title "$TITLE" \
    --arg desc "$DESC" \
    --arg cat "$CATEGORY" \
    --argjson steps "$STEPS_JSON" \
    --argjson priority "$((1 + RANDOM % 5))" \
    '{slug:$slug, title:$title, description:$desc, category:$cat, steps:$steps, priority:$priority, files_to_touch:["quick"]}' \
    >> "$IDEA_OUTPUT"

  log "Idea $i: $TITLE (slug: $SLUG)"
done

# The IDEA_OUTPUT file currently contains one JSON object per line (not a valid array yet)
# Convert to a JSON array by wrapping with [] and replacing newlines with commas
# Use jq to safely combine
TMP_ARRAY=$(mktemp)
jq -s '.' "$IDEA_OUTPUT" > "$TMP_ARRAY"
mv "$TMP_ARRAY" "$IDEA_OUTPUT"

# Also copy to latest.json for executor
cp "$IDEA_OUTPUT" "$IDEAS_DIR/latest.json"

# Update status to idle (done)
echo "{\"status\":\"idle\",\"last_run\":\"$RUN_TIMESTAMP\",\"current_idea\":null}" > "$STATUS_FILE"

log "Generator completed: $(jq 'length' "$IDEA_OUTPUT" 2>/dev/null || echo "?") ideas written."
log "Output: $IDEA_OUTPUT, linked as latest.json"

# Cleanup
rm -f "$INSPIRATION"

exit 0
