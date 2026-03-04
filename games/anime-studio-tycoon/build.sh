#!/usr/bin/env bash
set -e

game_dir="games/anime-studio-tycoon"

# Create main.py
cat > "$game_dir/main.py" << 'PYEOF'
#!/usr/bin/env python3
import random, sys

# ANSI colors for pretty output
class C:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    M = '\033[35m'  # Magenta for special
    R = '\033[31m'  # Red
    E = '\033[0m'   # End

# Game state
money = 100000
staff = 5
reputation = 50
fans = 1000
week = 0
episodes_target = 10
episodes_completed = 0
salary_per_staff = 2000

# New: Genre & Trend system
GENRES = ["Shonen", "Isekai", "Slice of Life", "Mecha", "Horror", "Sports", "Romance", "Sci-Fi"]
player_genre = random.choice(GENRES)
market_trend = random.choice(GENRES)
trend_announced = False

# New: Production points system
production_progress = 0
points_per_episode = 100
is_crunching = False

# New: Upgrades
UPGRADES = {
    "star_director": {"cost": 30000, "label": "Star Director", "desc": "Reputation gain from episodes doubled.", "owned": False},
    "god_animator": {"cost": 25000, "label": "God Animator", "desc": "Reduces 'Staff burnout' event chance by 50%.", "owned": False},
    "better_software": {"cost": 15000, "label": "Better Software", "desc": "Weekly salary cost reduced by 20%.", "owned": False},
    "merch_table": {"cost": 20000, "label": "Merch Table", "desc": "Every 4 weeks: +¥3000 fans (actually +3000 fans).", "owned": False}
}
salary_multiplier = 1.0

events = [
    ("Viral moment!", 0, 0, 0, 5000),
    ("Staff burnout", 0, 0, 0, 0),  # Fixed money delta; staff loss handled separately
    ("Budget overrun", -10000, 0, 0, 0),
    ("Positive review", 0, 0, 10, 0),
    ("Critic praise", 0, 0, 15, 1000),
    ("Streaming deal", 25000, 0, 0, 0),
    ("Fan convention", 0, 0, 0, 2000),
    ("Licensing opportunity", 15000, 0, 5, 500),
    # New events to increase variety and balance
    ("Merchandise boom", 8000, 0, 0, 3000),
    ("Award nomination", 0, 0, 8, 2000),
    ("Investor injection", 15000, 0, 0, 0),
    ("Fan convention success", 0, 0, 5, 4000),
    ("Voice actor strike", -1500, -1, 0, 0),
    ("Copyright lawsuit", -8000, 0, -5, -1000),
    ("Studio expansion", -10000, 2, 5, 2000),
    ("International licensing", 20000, 0, 3, 5000),
    ("Training seminar", -2000, 1, 3, 0),
    ("Negative press", 0, 0, -8, -2000),
    ("Streaming hit", 12000, 0, 5, 8000),
    ("Collaboration", 5000, 0, 5, 3000)
]

def clear_screen():
    print("\033[2J\033[H", end="")

def status():
    trend_str = f" [Trend: {market_trend}]" if market_trend else ""
    genre_str = f" [Genre: {player_genre}]"
    progress_bar = "[" + "#" * (production_progress * 10 // points_per_episode) + "." * (10 - production_progress * 10 // points_per_episode) + "]"
    print(f"Week {week} | Money: ¥{money} | Staff: {staff} | Rep: {reputation} | Fans: {fans} | Episodes: {episodes_completed}/{episodes_target} | Progress: {progress_bar}{genre_str}{trend_str}")

def check_end():
    if money < 0:
        print(f"{C.FAIL}Bankruptcy! You lose.{C.E}")
        sys.exit(0)
    if reputation < 0:
        print(f"{C.FAIL}Reputation too low! You lose.{C.E}")
        sys.exit(0)
    if episodes_completed >= episodes_target:
        print(f"{C.OKGREEN}Congratulations! You completed {episodes_target} episodes with {fans} fans and rep {reputation}. You win!{C.E}")
        sys.exit(0)

def apply_upgrades():
    global salary_multiplier
    if UPGRADES["better_software"]["owned"]:
        salary_multiplier = 0.8

def episode_gain():
    global reputation, fans, market_trend, player_genre, trend_announced
    # Base gains
    rep_gain = 10
    fan_gain = random.randint(2000, 8000)
    
    # Genre-trend multiplier
    trend_mult = 1.5 if player_genre == market_trend else 1.0
    fan_gain = int(fan_gain * trend_mult)
    
    # Upgrades effect
    if UPGRADES["star_director"]["owned"]:
        rep_gain *= 2
    
    reputation += rep_gain
    fans += fan_gain
    
    print(f"{C.OKCYAN}Episode {episodes_completed} completed!{C.E}")
    print(f"  Reputation +{rep_gain}, Fans +{fan_gain}")
    if trend_mult > 1.0 and not trend_announced:
        print(f"  {C.M}🔥 TREND BONUS: {player_genre} is hot right now!{C.E}")
        trend_announced = True
    
    # Every 3 episodes, player can change genre
    if episodes_completed % 3 == 0 and episodes_completed > 0:
        print(f"\n{C.OKBLUE}New Season! You can change your studio's genre.{C.E}")
        for i, g in enumerate(GENRES, 1):
            current = " (current)" if g == player_genre else ""
            print(f"  {i}) {g}{current}")
        print(f"  0) Keep current genre")
        try:
            choice = input("> ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(GENRES):
                    player_genre = GENRES[idx]
                    print(f"{C.OKGREEN}Studio genre changed to {player_genre}.{C.E}")
                elif int(choice) == 0:
                    print(f"Keeping {player_genre}.")
        except (EOFError, KeyboardInterrupt):
            print(f"Auto-keeping {player_genre}.")

def weekly_event():
    global money, staff, reputation, fans, is_crunching
    if random.random() < 0.15:  # 15% chance per week
        ev = random.choice(events)
        print(f"{C.WARNING}Event: {ev[0]}{C.E}")
        money += ev[1]
        staff += ev[2]
        reputation += ev[3]
        fans += ev[4]
        
        if ev[0] == "Staff burnout":
            # Crunch increases burnout chance; if in crunch, event is more likely
            burnout_penalty = 2
            if is_crunching:
                print(f"  {C.R}Crunch makes burnout worse!{C.E}")
                burnout_penalty = 4
            # Non-interactive auto-response
            if money >= 5000:
                money -= 5000
                print(f"  Paid overtime (auto). Staff stay.")
            else:
                print(f"  Can't afford overtime. Staff leave.")
                staff -= burnout_penalty
                if staff < 1:
                    staff = 1

def weekly_update():
    global money, staff, reputation, week, episodes_completed, production_progress, is_crunching, market_trend, trend_announced, fans
    
    # Salary payment (with upgrade discount)
    actual_salary = staff * salary_per_staff * salary_multiplier
    money -= int(actual_salary)
    
    # Random event
    weekly_event()
    
    # Show choices with auto-mode
    print(f"\n{C.BOLD}Choices:{C.E}")
    print(f"1) Hire (+1 staff, -¥5000)")
    print(f"2) Fire (+¥2000, -1 staff)")
    print(f"3) Train (staff +1, -¥3000)")
    print(f"4) Rush production (crunch mode: 2x progress, -2 rep/week, higher burnout)")
    print(f"5) Quality focus (reputation +5, costs ¥2000)")
    print(f"6) View upgrades")
    print(f"7) Next week")
    
    # Non-interactive auto-choose based on simple heuristics
    try:
        choice = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        # Auto-mode: choose based on game state (do NOT modify game state here!)
        if money < 8000 and staff > 4:
            choice = "2"  # Fire if low on money and too many staff
        elif money >= 5000 and staff < 6:
            choice = "1"  # Hire if can afford and staff low
        elif money >= 3000 and staff < 6:
            choice = "3"  # Train if can afford
        elif reputation < 70 and money >= 2000 and not is_crunching:
            choice = "5"  # Quality focus if rep low
        elif not UPGRADES["star_director"]["owned"] and money >= UPGRADES["star_director"]["cost"]:
            choice = "6"  # Buy upgrade if affordable
        elif production_progress < points_per_episode * 1.5 and money >= 2000 and episodes_completed < episodes_target and not is_crunching:
            # If behind schedule and can afford crunch (and not already active)
            choice = "4"
        else:
            choice = "7"  # Advance week
        print(f"Auto-choosing: {choice}")
    
    if choice == "1":
        if money >= 5000:
            money -= 5000; staff += 1; print(f"{C.OKGREEN}Hired a new animator.{C.E}")
        else:
            print(f"{C.FAIL}Not enough money.{C.E}")
    elif choice == "2":
        if staff > 1:
            staff -= 1; money += 2000; print(f"{C.WARNING}Fired a staff member.{C.E}")
        else:
            print(f"{C.FAIL}Can't fire the only staff!{C.E}")
    elif choice == "3":
        if money >= 3000 and staff > 0:
            money -= 3000; staff += 1; print(f"{C.OKCYAN}Trained a junior; they became a full animator.{C.E}")
        else:
            print(f"{C.FAIL}Not enough money or no staff.{C.E}")
    elif choice == "4":
        if is_crunching:
            is_crunching = False
            print(f"{C.OKGREEN}Crunch deactivated. Studio returns to normal pace.{C.E}")
        else:
            is_crunching = True
            print(f"{C.R}⚠️ CRUNCH ACTIVATED: Progress doubled, but reputation suffers and burnout risk increases!{C.E}")
    elif choice == "5":
        if money >= 2000:
            money -= 2000; reputation += 5; print(f"{C.OKGREEN}Quality focus paid off. Reputation +5.{C.E}")
        else:
            print(f"{C.FAIL}Not enough money.{C.E}")
    elif choice == "6":
        print(f"\n{C.HEADER}Available Upgrades:{C.E}")
        affordable = False
        for key, upg in UPGRADES.items():
            status_icon = f"{C.OKGREEN}[OWNED]{C.E}" if upg["owned"] else f"[¥{upg['cost']}]"
            if not upg["owned"] and money >= upg["cost"]:
                status_icon = f"{C.OKCYAN}[BUY]{C.E}"
                affordable = True
            print(f"  {upg['label']} {status_icon}")
            print(f"    {upg['desc']}")
        if not affordable:
            print(f"  {C.WARNING}No affordable upgrades.{C.E}")
        # Allow purchase
        if affordable:
            try:
                buy = input(f"\nEnter upgrade to buy (or press Enter to cancel): ").strip().lower()
                for key, upg in UPGRADES.items():
                    if not upg["owned"] and money >= upg["cost"] and buy in key.lower():
                        money -= upg["cost"]
                        upg["owned"] = True
                        print(f"{C.OKGREEN}Purchased {upg['label']}!{C.E}")
                        if key == "better_software":
                            apply_upgrades()
                        break
            except (EOFError, KeyboardInterrupt):
                pass
    elif choice == "7":
        is_crunching = False
        # Change trend occasionally
        if random.random() < 0.2:  # 20% chance per week when advancing
            old_trend = market_trend
            while market_trend == old_trend:
                market_trend = random.choice(GENRES)
            trend_announced = False
            print(f"{C.OKCYAN}Market trend shifted to: {market_trend}{C.E}")
        # Bonus from merch table
        if UPGRADES["merch_table"]["owned"] and week % 4 == 0:
            fans += 3000
            print(f"{C.M}Merch sales added 3000 fans!{C.E}")
    else:
        print(f"{C.FAIL}Invalid choice; skipping.{C.E}")
    
    # Weekly progress based on staff (and crunch)
    weekly_gain = staff * 5
    if is_crunching:
        weekly_gain *= 2
        reputation -= 2  # Crunch penalty
        print(f"  {C.R}⚠️ CRUNCH: Progress doubled but reputation -2, staff morale dropping...{C.E}")
    
    production_progress += weekly_gain
    
    # Check episode completion
    while production_progress >= points_per_episode and episodes_completed < episodes_target:
        production_progress -= points_per_episode
        episodes_completed += 1
        episode_gain()
    
    week += 1
    check_end()

if __name__ == "__main__":
    clear_screen()
    print(f"{C.HEADER}=== Anime Studio Tycoon ==={C.E}")
    print("Manage your studio: balance money, staff, reputation, fans.")
    print("Goal: Complete 10 episodes while maintaining positive reputation and at least 50,000 fans. Avoid bankruptcy!")
    print()
    print(f"{C.OKCYAN}Your studio's genre: {player_genre}{C.E}")
    print(f"Current market trend: {market_trend} (bonus fan growth if matched!)")
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

## New Features (Enhanced)

- **Genre & Trend System**: Choose your studio's genre and watch market trends. Matching the trend gives +50% fan growth!
- **Production Points**: Staff generate progress points each week; complete episodes by reaching 100 points.
- **Crunch Mode**: Activate crunch for 2x progress at the cost of -2 reputation/week and higher burnout risk.
- **Upgrades System**: Purchase special upgrades like Star Director (double rep gain), God Animator (reduce burnout), Better Software (20% salary discount), and Merch Table (every 4 weeks +3000 fans).
- **Dynamic Events**: More events including viral moments, streaming deals, licensing opportunities.
- **Weekly Progress Bar**: Visual indicator of episode completion progress.

## Controls
Each week you choose an action:
1. Hire — cost ¥5000, +1 staff
2. Fire — gain ¥2000, -1 staff (minimum 1)
3. Train — cost ¥3000, converts a junior to full animator (+1 staff)
4. Rush production — toggle crunch mode (2x progress, -2 rep/week, higher burnout)
5. Quality focus — cost ¥2000, +5 reputation
6. View upgrades — see available purchases; buy if affordable
7. Next week — advance time

Good luck!
EOF

chmod +x "$game_dir/main.py" || true
echo "Build script created"