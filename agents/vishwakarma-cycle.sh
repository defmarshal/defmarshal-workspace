#!/usr/bin/env bash
# Vishwakarma — Game Development Planner
# Spawns Kṛṣṇa to build games

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOG="agents/vishwakarma/vishwakarma.log"
mkdir -p agents/vishwakarma
echo "[$(date --iso-8601=seconds)] Vishwakarma cycle starting" >> "$LOG"

# Avoid overlap using lockfile
lockfile="agents/vishwakarma/.lock"
if [ -e "$lockfile" ]; then
  # Check if lock is stale (>1 hour)
  if [ $(($(date +%s) - $(stat -c %Y "$lockfile" 2>/dev/null || echo 0))) -gt 3600 ]; then
    echo "[$(date --iso-8601=seconds)] Stale lock detected, removing" >> "$LOG"
    rm -f "$lockfile"
  else
    echo "[$(date --iso-8601=seconds)] Another Vishwakarma running (lock present) — exiting" >> "$LOG"
    exit 0
  fi
fi
# Create lock
echo $$ > "$lockfile"

# Don't spawn if Kṛṣṇa is already building
if pgrep -f "krishna-builder.sh" > /dev/null; then
  echo "[$(date --iso-8601=seconds)] Kṛṣṇa already working — skipping" >> "$LOG"
  rm -f "$lockfile"
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
  phase="polish"
  task_desc="Polish and expand Anime Studio Tycoon (add new events, balance)"
else
  phase="create"
  task_desc="Create initial version of Anime Studio Tycoon (CLI management sim)"
fi

# If creating, generate a build script that Kṛṣṇa will run
build_script="${game_dir}/build.sh"
if [ "$phase" = "create" ]; then
  mkdir -p "$game_dir"
  cat > "$build_script" << 'BUILDSCRIPT'
#!/usr/bin/env bash
set -e

game_dir="games/anime-studio-tycoon"

# Create main.py
cat > "$game_dir/main.py" << 'PYEOF'
#!/usr/bin/env python3
import random, sys

# Game state
money = 100000
staff = 5
reputation = 50
fans = 1000
week = 0
episodes_target = 10
episodes_completed = 0
salary_per_staff = 2000

events = [
    ("Viral moment!", 0, 0, 0, 5000),
    ("Staff burnout", -2, 0, 0, 0),
    ("Budget overrun", -10000, 0, 0, 0),
    ("Positive review", 0, 0, +10, 0)
]

def status():
    print(f"Week {week} | Money: ¥{money} | Staff: {staff} | Rep: {reputation} | Fans: {fans} | Episodes: {episodes_completed}/{episodes_target}")

def check_end():
    if money < 0:
        print("Bankruptcy! You lose.")
        sys.exit(0)
    if reputation < 0:
        print("Reputation too low! You lose.")
        sys.exit(0)
    if episodes_completed >= episodes_target:
        print(f"Congratulations! You completed {episodes_target} episodes with {fans} fans and rep {reputation}. You win!")
        sys.exit(0)

def weekly_update():
    global money, staff, reputation, fans, week, episodes_completed
    # Salaries
    money -= staff * salary_per_staff
    # Random event
    if random.random() < 0.1:
        ev = random.choice(events)
        print(f"Event: {ev[0]}")
        money += ev[1]
        staff += ev[2]
        reputation += ev[3]
        fans += ev[4]
        if ev[0] == "Staff burnout":
            print("Do you pay overtime (¥5000) to keep staff? (y/n)")
            choice = input("> ").strip().lower()
            if choice == 'y':
                if money >= 5000:
                    money -= 5000
                    print("Paid overtime. Staff stay.")
                else:
                    print("Can't afford overtime. Staff leave.")
                    staff -= 2
            else:
                staff -= 2
                print("Staff quit due to burnout.")
    # Propose choices
    print("\nChoices:")
    print("1) Hire (+1 staff, -¥5000)")
    print("2) Fire (+¥2000, -1 staff)")
    print("3) Train (staff +1, -¥3000)")
    print("4) Rush (faster production but risk quality) - not implemented")
    print("5) Quality focus (reputation +5, costs ¥2000)")
    print("6) Next week")
    choice = input("> ").strip()
    if choice == "1":
        if money >= 5000:
            money -= 5000; staff += 1; print("Hired a new animator.")
        else:
            print("Not enough money.")
    elif choice == "2":
        if staff > 1:
            staff -= 1; money += 2000; print("Fired a staff member.")
        else:
            print("Can't fire the only staff!")
    elif choice == "3":
        if money >= 3000 and staff > 0:
            money -= 3000; staff += 1; print("Trained a junior; they became a full animator.")
        else:
            print("Not enough money or no staff.")
    elif choice == "4":
        if random.random() < 0.7:
            fans += random.randint(500, 2000)
            print("Rush succeeded! Fans increased.")
        else:
            reputation -= 10
            print("Rush failed! Quality dropped, reputation lost.")
    elif choice == "5":
        if money >= 2000:
            money -= 2000; reputation += 5; print("Quality focus paid off.")
        else:
            print("Not enough money.")
    elif choice == "6":
        pass
    else:
        print("Invalid choice; skipping.")
    # Episode production: every 2 weeks completes an episode
    if week % 2 == 0 and episodes_completed < episodes_target:
        episodes_completed += 1
        print(f"Episode {episodes_completed} completed!")
    week += 1
    check_end()

if __name__ == "__main__":
    print("=== Anime Studio Tycoon ===")
    print("Manage your studio: balance money, staff, reputation, fans.")
    print("Goal: Complete 10 episodes with >50k fans and non-negative reputation.")
    print()
    while True:
        status()
        weekly_update()
PYEOF

# Create README
cat > "$game_dir/README.md" << 'EOF'
# Anime Studio Tycoon

A CLI management simulation where you run an anime studio.

## Run
python3 games/anime-studio-tycoon/main.py

## Goal
Complete 10 episodes while maintaining positive reputation and at least 50,000 fans. Avoid bankruptcy!

## Controls
Each week you choose an action:
1. Hire — cost ¥5000, +1 staff
2. Fire — gain ¥2000, -1 staff (minimum 1)
3. Train — cost ¥3000, converts a junior to full animator (+1 staff)
4. Rush production — gamble for fans, risk reputation
5. Quality focus — cost ¥2000, +5 reputation
6. Next week — advance time

Good luck!
EOF

chmod +x "$game_dir/main.py" || true
echo "Build script created"
BUILDSCRIPT

  echo "[$(date --iso-8601=seconds)] Build script created at $build_script" >> "$LOG"
else
  echo "[$(date --iso-8601=seconds)] Phase $phase: using existing build script (if any)" >> "$LOG"
fi

cat > "$plan_file" << PLAN
# Vishwakarma Game Plan — $timestamp
**Phase**: $phase
**Task**: $task_desc
**Generated**: $(date --iso-8601=seconds)
**Game Dir**: $game_dir

## Objective
$task_desc

## Steps for Kṛṣṇa
1. If build script exists at $build_script, run: `bash $build_script`
   Else, skip build (already built or no script)
2. Test the game (non‑interactive, ignore exit code): `timeout 30 python3 ${game_dir}/main.py < /dev/null || true`
3. Commit changes with prefix "game:" and push to origin/master
4. Write completion report to agents/krishna/reports/report-${plan_id}.md

## Notes
- Keep changes small
- If build fails, log and exit non‑zero

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

openclaw sessions spawn --agent main --label krishna-${plan_id} --task "$message" 2>&1 >> "$LOG"

echo "[$(date --iso-8601=seconds)] Kṛṣṇa spawned (label: krishna-${plan_id})" >> "$LOG"
echo "[$(date --iso-8601=seconds)] Vishwakarma cycle complete" >> "$LOG"

# Remove lock
rm -f "$lockfile"
