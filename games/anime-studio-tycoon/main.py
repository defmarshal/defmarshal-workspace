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

# Game state - polished balance (2026-03-05)
money = 75000  # Reduced from 200000 for early-game tension
staff = 5
reputation = 50
fans = 1000
week = 0
episodes_target = 10
episodes_completed = 0
salary_per_staff = 2000  # Keep original salary, upgrades will reduce
studio_rent = 5000  # Fixed weekly rent

# Genre & Trend system
GENRES = ["Shonen", "Isekai", "Slice of Life", "Mecha", "Horror", "Sports", "Romance", "Sci-Fi"]
player_genre = random.choice(GENRES)
market_trend = random.choice(GENRES)
trend_announced = False

# Production points system
production_progress = 0
points_per_episode = 100
is_crunching = False

# Upgrades - added Marketing Team
UPGRADES = {
    "star_director": {"cost": 30000, "label": "Star Director", "desc": "Reputation gain from episodes doubled.", "owned": False},
    "god_animator": {"cost": 25000, "label": "God Animator", "desc": "Reduces 'Staff burnout' event chance by 50%.", "owned": False},
    "better_software": {"cost": 15000, "label": "Better Software", "desc": "Weekly salary cost reduced by 30%.", "owned": False},
    "merch_table": {"cost": 20000, "label": "Merch Table", "desc": "Every 4 weeks: +¥3000 fans (actually +3000 fans).", "owned": False},
    "marketing_team": {"cost": 25000, "label": "Marketing Team", "desc": "Increases fan gain from episodes by 30%.", "owned": False}
}
salary_multiplier = 1.0

# Expanded event pool for more variety and better balance
events = [
    ("Viral moment!", 0, 0, 0, 6000),
    ("Staff burnout", 0, 0, 0, 0),
    ("Budget overrun", -8000, 0, 0, 0),
    ("Positive review", 0, 0, 10, 0),
    ("Critic praise", 0, 0, 15, 1500),
    ("Streaming deal", 25000, 0, 0, 0),
    ("Fan convention", 0, 0, 0, 2500),
    ("Licensing opportunity", 18000, 0, 5, 800),
    ("Merchandise boom", 10000, 0, 0, 3500),
    ("Award nomination", 0, 0, 10, 2500),
    ("Investor injection", 20000, 0, 0, 0),
    ("Fan convention success", 0, 0, 6, 5000),
    ("Voice actor strike", -2000, -1, 0, 0),
    ("Copyright lawsuit", -10000, 0, -5, -1500),
    ("Studio expansion", -12000, 2, 8, 3000),
    ("International licensing", 25000, 0, 5, 6000),
    ("Training seminar", -1500, 1, 5, 0),
    ("Negative press", 0, 0, -10, -2500),
    ("Streaming hit", 15000, 0, 8, 10000),
    ("Collaboration", 6000, 0, 6, 4000),
    ("Studio renovation", -10000, 0, 12, 3000),
    ("Contract dispute", -6000, -1, -6, -1500),
    ("Merchandise counterfeit", -4000, 0, -4, -2500),
    ("Fan art contest", 0, 0, 4, 6000),
    ("Streaming platform partnership", 25000, 0, 6, 4000),
    ("Key animator quits", 0, -1, -4, -800),
    ("Crowdfunding campaign", 20000, 0, 6, 12000),
    ("Licensing deal rejected", -12000, 0, 0, 0),
    ("Talent scout", 0, 1, 0, 0),
    ("Season finale hype", 0, 0, 10, 18000),
    ("Server outage", -6000, 0, -3, -1500),
    ("Fan donation", 3000, 0, 0, 800),
    ("Award win", 0, 0, 8, 4000),
    # New polish events
    ("Social media backlash", -5000, 0, -6, -2000),
    ("Merchandise collaboration", 8000, 0, 4, 6000),
    ("Studio anniversary", 0, 0, 5, 5000),
    ("Publishing deal", 22000, 0, 7, 3000),
    ("Voice actor popularity surge", 0, 0, 6, 2000)
]

def clear_screen():
    print("\033[2J\033[H", end="")

def status():
    trend_str = f" [Trend: {market_trend}]" if market_trend else ""
    genre_str = f" [Genre: {player_genre}]"
    
    # Improved progress bar with clamp to prevent negative dots
    progress_pct = min(production_progress / points_per_episode, 1.0)
    filled = int(progress_pct * 10)
    progress_bar = "[" + "#" * filled + "." * (10 - filled) + "]"
    
    # Add visual indicator when episode is nearly complete
    near_complete = ""
    if progress_pct >= 0.8 and progress_pct < 1.0:
        near_complete = f" {C.WARNING}⚡ NEARLY DONE!{C.E}"
    elif progress_pct >= 1.0:
        near_complete = f" {C.OKGREEN}✓ READY!{C.E}"
    
    print(f"Week {week} | Money: ¥{money} | Staff: {staff} | Rep: {reputation} | Fans: {fans} | Episodes: {episodes_completed}/{episodes_target} | Progress: {progress_bar}{near_complete}{genre_str}{trend_str}")

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
        salary_multiplier = 0.7  # 30% salary reduction

def episode_gain():
    global reputation, fans, market_trend, player_genre, trend_announced, points_per_episode, episodes_completed
    rep_gain = 10
    fan_gain = random.randint(2000, 8000)
    
    # Genre-trend multiplier
    trend_mult = 1.5 if player_genre == market_trend else 1.0
    fan_gain = int(fan_gain * trend_mult)
    
    # Upgrade effects
    if UPGRADES["star_director"]["owned"]:
        rep_gain *= 2
    if UPGRADES["marketing_team"]["owned"]:
        fan_gain = int(fan_gain * 1.3)
    
    reputation += rep_gain
    fans += fan_gain
    
    print(f"{C.OKCYAN}Episode {episodes_completed} completed!{C.E}")
    print(f"  Reputation +{rep_gain}, Fans +{fan_gain}")
    if trend_mult > 1.0 and not trend_announced:
        print(f"  {C.M}🔥 TREND BONUS: {player_genre} is hot right now!{C.E}")
        trend_announced = True
    
    # Increase difficulty for next episode (25% growth)
    points_per_episode = int(points_per_episode * 1.25)
    print(f"  Production complexity increased to {points_per_episode} points for next episode.")
    
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
    burnout_base_chance = 0.12  # Slightly reduced for better balance
    if UPGRADES["god_animator"]["owned"]:
        burnout_base_chance *= 0.5
    
    if random.random() < burnout_base_chance:
        ev = random.choice(events)
        print(f"{C.WARNING}Event: {ev[0]}{C.E}")
        money += ev[1]
        staff += ev[2]
        reputation += ev[3]
        fans += ev[4]
        
        if ev[0] == "Staff burnout":
            burnout_penalty = 2
            if is_crunching:
                print(f"  {C.R}Crunch makes burnout worse!{C.E}")
                burnout_penalty = 4
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
    
    # Passive fan revenue: ¥2 per fan, scaled by reputation (higher rep = more revenue per fan)
    weekly_revenue = int(fans * 2 * (reputation / 50))
    money += weekly_revenue
    
    # Fixed studio rent
    money -= studio_rent
    
    # Salary payment (with upgrade discount)
    actual_salary = staff * salary_per_staff * salary_multiplier
    money -= int(actual_salary)
    
    print(f"{C.OKGREEN}Weekly Report:{C.E}")
    print(f"  Revenue from Fans: +¥{weekly_revenue}")
    print(f"  Studio Rent: -¥{studio_rent}")
    print(f"  Staff Salaries: -¥{int(actual_salary)}")
    
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
    
    # Determine auto-mode (non-interactive or forced)
    auto_mode = False
    try:
        choice = input("> ").strip()
        if not choice and not sys.stdin.isatty():
            auto_mode = True
    except (EOFError, KeyboardInterrupt):
        auto_mode = True

    if auto_mode:
        # Smarter AI with financial health checks and optimal staffing
        # Financial tiers
        critical_threshold = 50000   # Below this, be very conservative
        safe_threshold = 100000     # Above this, can spend more freely
        
        # Staff management - optimal range 5-7
        min_staff = 5
        max_staff = 7
        
        # Priority: avoid bankruptcy first, then progress towards goals
        
        if money < critical_threshold:
            # Emergency mode: cut costs but keep minimum viable staff
            if staff > min_staff:
                choice = "2"  # Fire to reduce salary burden
            elif reputation < 60 and money >= 2000 and not is_crunching:
                choice = "5"  # Quality focus to boost rep (prevent rep loss)
            elif production_progress < points_per_episode * 0.8 and money >= 3000 and not is_crunching:
                choice = "4"  # Use crunch to push episode completion for fan boost
            else:
                choice = "7"  # Wait and recover
        elif money < safe_threshold:
            # Cautious mode: build stable foundation
            if not UPGRADES["better_software"]["owned"] and money >= UPGRADES["better_software"]["cost"] + 30000:
                choice = "6"  # Better Software reduces ongoing costs (high priority)
            elif reputation < 70 and money >= 2000 and not is_crunching:
                choice = "5"  # Quality focus
            elif staff < min_staff and money >= 5000:
                choice = "1"  # Hire to minimum
            elif staff > max_staff:
                choice = "2"  # Reduce overstaffing
            elif production_progress < points_per_episode * 0.4 and not is_crunching and money > 60000:
                choice = "4"  # Crunch if behind schedule and stable
            elif money >= 5000 and staff < 6:
                choice = "1"  # Hire to 6 staff baseline (good production)
            else:
                choice = "7"
        else:
            # Comfortable mode: can invest in growth
            if not UPGRADES["better_software"]["owned"] and money >= UPGRADES["better_software"]["cost"] + 30000:
                choice = "6"
            elif not UPGRADES["star_director"]["owned"] and money >= UPGRADES["star_director"]["cost"] + 30000:
                choice = "6"
            elif not UPGRADES["god_animator"]["owned"] and money >= UPGRADES["god_animator"]["cost"] + 30000:
                choice = "6"
            elif not UPGRADES["merch_table"]["owned"] and money >= UPGRADES["merch_table"]["cost"] + 30000:
                choice = "6"
            elif not UPGRADES["marketing_team"]["owned"] and money >= UPGRADES["marketing_team"]["cost"] + 30000:
                choice = "6"
            elif staff < max_staff and money >= 5000:
                choice = "1"  # Hire to increase capacity (aim for 7 staff)
            elif reputation < 80 and money >= 2000 and not is_crunching:
                choice = "5"
            elif production_progress < points_per_episode * 0.5 and not is_crunching and money > 40000:
                choice = "4"
            else:
                choice = "7"
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
