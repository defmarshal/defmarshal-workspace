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
money = 500000  # Heavily increased for winnability
staff = 5
reputation = 50
fans = 1000
week = 0
episodes_target = 6  # Reduced to 6 for quick completion
episodes_completed = 0
salary_per_staff = 1000  # Lowered salary
difficulty = "easy"

# New: Genre & Trend system
GENRES = ["Shonen", "Isekai", "Slice of Life", "Mecha", "Horror", "Sports", "Romance", "Sci-Fi"]
player_genre = random.choice(GENRES)
market_trend = random.choice(GENRES)
trend_announced = False

# New: Production points system
production_progress = 0
points_per_episode = 60  # Reduced for very fast completion
is_crunching = False

# New: Upgrades (add two new ones)
UPGRADES = {
    "star_director": {"cost": 30000, "label": "Star Director", "desc": "Reputation gain from episodes doubled.", "owned": False},
    "god_animator": {"cost": 25000, "label": "God Animator", "desc": "Reduces 'Staff burnout' event chance by 50%.", "owned": False},
    "better_software": {"cost": 15000, "label": "Better Software", "desc": "Weekly salary cost reduced by 20%.", "owned": False},
    "merch_table": {"cost": 20000, "label": "Merch Table", "desc": "Every 4 weeks: +¥3000 fans (actually +3000 fans).", "owned": False},
    # New upgrades
    "marketing_dept": {"cost": 25000, "label": "Marketing Dept", "desc": "Weekly fan gain from advertising (50-200).", "owned": False},
    "advanced_pipeline": {"cost": 35000, "label": "Advanced Pipeline", "desc": "Production per staff +2 weekly.", "owned": False},
    "sponsorship": {"cost": 40000, "label": "Sponsorship Deal", "desc": "Weekly sponsorship income ¥5000.", "owned": False}
}
salary_multiplier = 1.0

events = [
    ("Viral moment!", 0, 0, 0, 5000),
    ("Staff burnout", 0, 0, 0, 0),
    ("Budget overrun", -10000, 0, 0, 0),
    ("Positive review", 0, 0, 10, 0),
    ("Critic praise", 0, 0, 15, 1000),
    ("Streaming deal", 25000, 0, 0, 0),
    ("Fan convention", 0, 0, 0, 2000),
    ("Licensing opportunity", 15000, 0, 5, 500),
    # Original events
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
    ("Collaboration", 5000, 0, 5, 3000),
    # Polish events (2026-03-04)
    ("Studio renovation", -8000, 0, 10, 2000),
    ("Contract dispute", -5000, -1, -5, -1000),
    ("Merchandise counterfeit", -3000, 0, -3, -2000),
    ("Fan art contest", 0, 0, 3, 5000),
    ("Streaming platform partnership", 20000, 0, 5, 3000),
    ("Key animator quits", 0, -1, -3, -500),
    ("Crowdfunding campaign", 15000, 0, 5, 10000),
    ("Licensing deal rejected", -10000, 0, 0, 0),
    ("Talent scout", 0, 1, 0, 0),
    ("Season finale hype", 0, 0, 8, 15000),
    # New balance events
    ("Talent discovery", 0, 2, 5, 0),  # free staff + rep
    ("Fan convention mega-success", 0, 0, 0, 12000),
    ("Streaming partnership renewal", 20000, 0, 0, 0),
    ("Equipment failure", -5000, 0, -3, 0),
    ("Positive press tour", 5000, 0, 8, 3000),
    ("Merchandise line launch", 10000, 0, 3, 5000),
    ("Voice actor popular", 0, 0, 5, 4000),
    ("Social media viral", 0, 0, 0, 10000),
    ("Production efficiency breakthrough", 0, 0, 0, 0),  # handled separately
    ("Studio relocation", -15000, 0, 10, 5000),
    ("Crisis averted", 5000, 0, 5, 0),
    ("Holiday bonus", -3000, 0, 10, 2000),
    ("Media coverage", 0, 0, 12, 5000),
    ("New investor", 25000, 0, 0, 0)
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
    global salary_multiplier, weekly_gain_base
    salary_multiplier = 1.0
    weekly_gain_base = 5  # base production per staff
    if UPGRADES["better_software"]["owned"]:
        salary_multiplier = 0.8
    if UPGRADES["advanced_pipeline"]["owned"]:
        weekly_gain_base += 2

def episode_gain():
    global reputation, fans, market_trend, player_genre, trend_announced
    # Base gains
    rep_gain = 10
    fan_gain = random.randint(4000, 12000)  # Increased from 2000-8000
    
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
    
    # Initialize weekly gain base (will be adjusted by upgrades)
    weekly_gain_base = 5
    if UPGRADES["advanced_pipeline"]["owned"]:
        weekly_gain_base += 2
    
    # Salary payment (with upgrade discount)
    actual_salary = staff * salary_per_staff * salary_multiplier
    money -= int(actual_salary)
    
    # Passive income from upgrades
    if UPGRADES["sponsorship"]["owned"]:
        money += 5000
        print(f"{C.OKGREEN}Sponsorship income: ¥5000{C.E}")
    
    # Marketing department weekly fan bonus
    if UPGRADES["marketing_dept"]["owned"]:
        marketing_fans = random.randint(50, 200)
        fans += marketing_fans
        print(f"{C.OKCYAN}Marketing brought in {marketing_fans} new fans!{C.E}")
    
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
        # Improved auto-mode logic
        # Keep minimum cash buffer based on staff salary (relative)
        min_cash_buffer = staff * salary_per_staff * 2
        # Avoid firing below 4 staff at all costs (minimum viable team)
        should_fire = (money < min_cash_buffer and staff > 4) or (money < 0 and staff > 4)
        should_hire = staff < 6 and money > 20000 and not should_fire
        should_train = staff < 6 and money > 10000 and not should_fire
        should_quality = reputation < 60 and money >= 2000 and not is_crunching
        should_crunch = production_progress < points_per_episode * 1.5 and money >= 2000 and episodes_completed < episodes_target and not is_crunching and staff >= 4
        should_buy_upgrade = False
        for key, upg in UPGRADES.items():
            if not upg["owned"] and money >= upg["cost"]:
                should_buy_upgrade = True
                break
        
        if should_buy_upgrade:
            choice = "6"
        elif should_hire:
            choice = "1"
        elif should_train:
            choice = "3"
        elif should_quality:
            choice = "5"
        elif should_crunch:
            choice = "4"
        elif should_fire:
            choice = "2"
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
        affordable = []
        for key, upg in UPGRADES.items():
            status_icon = f"{C.OKGREEN}[OWNED]{C.E}" if upg["owned"] else f"[¥{upg['cost']}]"
            if not upg["owned"] and money >= upg["cost"]:
                status_icon = f"{C.OKCYAN}[BUY]{C.E}"
                affordable.append(key)
            print(f"  {upg['label']} {status_icon}")
            print(f"    {upg['desc']}")
        if not affordable:
            print(f"  {C.WARNING}No affordable upgrades.{C.E}")
        # Auto-mode purchase: buy the first affordable upgrade
        if auto_mode and affordable:
            buy_key = affordable[0]
            for key, upg in UPGRADES.items():
                if key == buy_key and not upg["owned"] and money >= upg["cost"]:
                    money -= upg["cost"]
                    upg["owned"] = True
                    print(f"{C.OKGREEN}Auto-purchased {upg['label']}!{C.E}")
                    if key in ("better_software", "advanced_pipeline"):
                        apply_upgrades()
                    break
        elif not auto_mode:
            try:
                buy = input(f"\nEnter upgrade to buy (or press Enter to cancel): ").strip().lower()
                if buy:
                    for key, upg in UPGRADES.items():
                        if not upg["owned"] and money >= upg["cost"] and buy in key.lower():
                            money -= upg["cost"]
                            upg["owned"] = True
                            print(f"{C.OKGREEN}Purchased {upg['label']}!{C.E}")
                            if key == "better_software":
                                apply_upgrades()
                            elif key == "advanced_pipeline":
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
    
    # Weekly production based on staff (and crunch, upgrades)
    weekly_gain = staff * weekly_gain_base
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
