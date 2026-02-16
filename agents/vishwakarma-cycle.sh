#!/usr/bin/env bash
# Vishwakarma — Game Development Planner
# Spawns Kṛṣṇa to build games

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOG="agents/vishwakarma/vishwakarma.log"
mkdir -p agents/vishwakarma
echo "[$(date --iso-8601=seconds)] Vishwakarma cycle starting" >> "$LOG"

# Avoid overlap
if pgrep -f "vishwakarma-cycle.sh" > /dev/null; then
  echo "[$(date --iso-8601=seconds)] Another Vishwakarma running — exiting" >> "$LOG"
  exit 0
fi

# Don't spawn if Kṛṣṇa is already building
if pgrep -f "krishna-builder.sh" > /dev/null; then
  echo "[$(date --iso-8601=seconds)] Kṛṣṇa already working — skipping" >> "$LOG"
  exit 0
fi

# --- Game Planning Phase ---
echo "[$(date --iso-8601=seconds)] Designing next game…" >> "$LOG"

# For v1, we'll build "Anime Studio Tycoon" if not exists
game_dir="games/anime-studio-tycoon"
timestamp=$(date +%Y-%m-%d_%H%M)
plan_file="agents/vishwakarma/plans/gameplan-${timestamp}.md"

# Check if game already exists
if [ -f "${game_dir}/main.py" ]; then
  # Determine next phase: could be "polish", "expand", "fix"
  phase="polish"
  task_desc="Polish and expand Anime Studio Tycoon (add new events, balance)"
else
  phase="create"
  task_desc="Create initial version of Anime Studio Tycoon (CLI management sim)"
fi

cat > "$plan_file" << PLAN
# Vishwakarma Game Plan — $timestamp
**Phase**: $phase
**Task**: $task_desc
**Generated**: $(date --iso-8601=seconds)

## Objective
$task_desc

## Game Concept: Anime Studio Tycoon
You manage a small anime studio. Balance:
- 💰 Money (budget)
- 👥 Staff (animators, writers, voice actors)
- ⭐ Reputation (fan love)
- 📅 Schedule (production timeline)

## Core Mechanics (v0.1)
- Start with ¥100,000, 5 staff, 10 episodes planned
- Each episode takes 2 weeks to produce
- Weekly expenses: staff salaries (¥2000 × staff count)
- Random events: staff burnout, fan backlash, viral hit, budget overrun
- Player choices each week: Hire/Fire, Train, Rush Production, Quality Focus, Marketing
- Win: Complete 10 episodes with >50k fans and positive reputation
- Lose: Bankruptcy or reputation < 0

## Implementation Steps (for Kṛṣṇa)

1. Create directory structure: games/anime-studio-tycoon/
   - main.py (entry point)
   - game.py (core logic)
   - events.py (random events)
   - ui.py (display)
   - requirements.txt (none, pure stdlib)
   - README.md (how to play)

2. Implement core state:
   - money, staff, reputation, fans, week, episodes_completed
   - salary_per_staff = 2000
   - episodes_target = 10

3. Implement weekly loop:
   - deduct salaries
   - check win/lose conditions
   - present choices (menu)
   - process choice outcomes
   - trigger random event (10% chance)
   - advance week

4. Add events:
   - "Viral moment!" → fans +5000
   - "Staff burnout" → lose 2 staff unless you pay overtime
   - "Budget overrun" → lose ¥10,000
   - "Positive review" → reputation +10

5. Display weekly status using simple text UI with colors (optional)

6. Add save/load? (v0.2 maybe)

7. Test: run through a full game to ensure no crashes

8. Package: ensure `python3 games/anime-studio-tycoon/main.py` runs

9. Write README with instructions and sample playthrough

10. Commit with prefix "game:" and push

## Notes
- Keep it simple, pure Python 3, no external dependencies
- Use only standard library (random, sys, os, json for save)
- Aim for ~200-300 lines total
- Focus on gameplay feel, not graphics

PLAN

echo "[$(date --iso-8601=seconds)] Plan created: $plan_file" >> "$LOG"
plan_id=$(basename "$plan_file" .md | cut -d'-' -f2-)

# --- Spawn Kṛṣṇa ---
echo "[$(date --iso-8601=seconds)] Spawning Kṛṣṇa to build the game…" >> "$LOG"

message="You are Kṛṣṇa, the game builder agent. Your task: execute the attached game development plan using the exec tool.

Plan file: $plan_file

Workflow:
1. Read the plan file.
2. Create the game directory and implement each step in the plan's 'Implementation Steps' section.
3. Test the game by running it at least once.
4. Write a completion report to agents/krishna/reports/report-${plan_id}.md
5. Commit changes with prefix 'game:' and push to origin/master.
6. Send a brief message back to Vishwakarma with summary.

Important: Use bash commands to create files and write code. For Python code, ensure proper indentation. Test often."

./openclaw sessions spawn --agent main --label krishna-${plan_id} --task "$message" 2>&1 >> "$LOG"

echo "[$(date --iso-8601=seconds)] Kṛṣṇa spawned (label: krishna-${plan_id})" >> "$LOG"
echo "[$(date --iso-8601=seconds)] Vishwakarma cycle complete" >> "$LOG"
