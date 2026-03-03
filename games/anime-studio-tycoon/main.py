#!/usr/bin/env python3
import random, sys

# ANSI colors for polish
class C:
    HEAD = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Game state
money = 100000
staff = 5
reputation = 50
fans = 1000
week = 0
episodes_target = 10
episodes_completed = 0
salary_per_staff = 2000

# Production system
production_progress = 0
points_per_episode = 100
weekly_production_per_staff = 5
is_crunching = False

# Genre & Market system
GENRES = ["Shonen", "Isekai", "Slice of Life", "Mecha", "Horror", "Comedy", "Adventure"]
player_genre = "Shonen"
market_trend = random.choice(GENRES)

# Upgrades system
upgrades_purchased = {
    "star_director": False,
    "god_animator": False,
    "merch_shop": False,
    "streaming_deal": False
}
upgrades_info = {
    "merch_shop": {"cost": 15000, "label": "Merchandise Shop", "desc": "Earn ¥5000 per episode from merchandise."},
    "streaming_deal": {"cost": 20000, "label": "Streaming Deal", "desc": "Earn ¥2000 per week from streaming royalties."},
    "god_animator": {"cost": 25000, "label": "God Animator", "desc": "Reduces 'Staff burnout' event chance by 50%."},
    "star_director": {"cost": 30000, "label": "Star Director", "desc": "Reputation gain from episodes is doubled."}
}

events = [
    ("Viral moment!", 0, 0, 0, 5000),
    ("Staff burnout", -2, 0, 0, 0),
    ("Budget overrun", -10000, 0, 0, 0),
    ("Positive review", 0, 0, +10, 0),
    ("Fan meetup", 0, 0, 0, 2000),
    ("Studio renovation", -8000, 0, +5, 0)
]

def status():
    print(f"Week {week} | Money: ¥{money} | Staff: {staff} | Rep: {reputation} | Fans: {fans} | Episodes: {episodes_completed}/{episodes_target}")
    if upgrades_purchased["star_director"]:
        print(f"  {C.YELLOW}★ Star Director active (reputation x2){C.END}")
    if upgrades_purchased["god_animator"]:
        print(f"  {C.CYAN}✦ God Animator active (burnout -50%){C.END}")
    if upgrades_purchased["merch_shop"]:
        print(f"  {C.GREEN}☕ Merch Shop: +¥5000/episode{C.END}")
    if upgrades_purchased["streaming_deal"]:
        print(f"  {C.BLUE}📺 Streaming: +¥2000/week{C.END}")
    print(f"  {C.MAGENTA}Trend: {market_trend} | Your Genre: {player_genre}{C.END}")
    print(f"  Production: {production_progress}/{points_per_episode}")

def check_end():
    if money < 0:
        print("Bankruptcy! You lose.")
        sys.exit(0)
    if reputation < 0:
        print("Reputation too low! You lose.")
        sys.exit(0)
    if episodes_completed >= episodes_target:
        if fans >= 50000:
            print(f"{C.GREEN}{C.BOLD}Congratulations! You completed {episodes_target} episodes with {fans:,} fans and rep {reputation}. You win!{C.END}")
            sys.exit(0)
        else:
            print(f"You completed {episodes_target} episodes but only have {fans:,} fans (need 50k). Keep going...")
            # Allow continuing to build more fans

def episode_gain():
    """Calculate fan gains when an episode is completed, considering genre/trend."""
    global fans, reputation, money
    base_fans = random.randint(2000, 8000)
    # Genre/trend bonus
    trend_mult = 1.5 if player_genre == market_trend else 1.0
    gained = int(base_fans * trend_mult)
    fans += gained
    
    # Reputation gain (base + quality focus heritage)
    rep_gain = random.randint(3, 8)
    if upgrades_purchased["star_director"]:
        rep_gain *= 2
    reputation += rep_gain
    
    print(f"\n{C.GREEN}{C.BOLD}★ Episode {episodes_completed} completed!{C.END}")
    print(f"  Fans: +{gained:,} (Trend bonus: {trend_mult}x)")
    print(f"  Reputation: +{rep_gain}")
    
    # Merchandise income
    if upgrades_purchased["merch_shop"]:
        merch_income = 5000
        money += merch_income
        print(f"  {C.GREEN}☕ Merch sales: +¥{merch_income:,}{C.END}")
    
    # Change market trend every 3 episodes to keep things fresh
    if episodes_completed % 3 == 0:
        change_trend()
    
    # Check win condition
    if fans >= 50000 and episodes_completed >= episodes_target:
        check_end()

def change_trend():
    """Randomly change the market trend, possibly suggesting a genre shift."""
    global market_trend, episodes_completed
    old_trend = market_trend
    while market_trend == old_trend:
        market_trend = random.choice(GENRES)
    print(f"  {C.MAGENTA}📊 Market shift: {old_trend} → {market_trend}{C.END}")

def apply_upgrade_effects():
    """Apply passive upgrade effects each week."""
    global money
    # Streaming deal: passive income
    if upgrades_purchased["streaming_deal"]:
        money += 2000
        print(f"  {C.BLUE}📺 Streaming royalties: +¥2000{C.END}")

def weekly_update():
    global money, staff, reputation, fans, week, episodes_completed, production_progress, is_crunching
    
    # Apply passive income
    apply_upgrade_effects()
    
    # Salaries
    salary_cost = staff * salary_per_staff
    money -= salary_cost
    print(f"  {C.RED}💰 Salaries: -¥{salary_cost:,}{C.END}")
    
    # Production progress
    weekly_gain = staff * weekly_production_per_staff
    if is_crunching:
        weekly_gain *= 2
        reputation -= 2
        print(f"  {C.RED}⚠️ CRUNCH: Progress doubled, rep -2{C.END}")
    
    production_progress += weekly_gain
    print(f"  {C.CYAN}⚙️ Production: +{weekly_gain} points (total: {production_progress}){C.END}")
    
    # Check if episode completes
    while production_progress >= points_per_episode and episodes_completed < episodes_target:
        production_progress -= points_per_episode
        episodes_completed += 1
        episode_gain()
    
    # Random event
    if random.random() < 0.15:  # Slightly higher event rate
        ev = random.choice(events)
        print(f"\n{C.YELLOW}⚡ Event: {ev[0]}{C.END}")
        money += ev[1]
        staff += ev[2]
        reputation += ev[3]
        fans += ev[4]
        if ev[0] == "Staff burnout":
            # Non-interactive safe: auto-choose based on affordability and god animator
            burnout_severity = 1
            if upgrades_purchased["god_animator"]:
                burnout_severity = 0.5  # 50% reduction
                print(f"  {C.CYAN}✦ God Animator protects: only 1 staff member at risk{C.END}")
            if money >= 5000:
                money -= 5000
                print(f"  {C.GREEN}Paid overtime (auto). Staff stay.{C.END}")
            else:
                lost_staff = int(2 * burnout_severity)
                if lost_staff < 1: lost_staff = 1
                staff = max(1, staff - lost_staff)
                print(f"  {C.RED}Can't afford overtime. {lost_staff} staff member(s) left.{C.END}")
    
    is_crunching = False  # Reset crunch for next week
    
    # Propose choices
    print("\n" + C.BOLD + "Choices:" + C.END)
    print("1) Hire (+1 staff, -¥5000)")
    print("2) Fire (+¥2000, -1 staff)")
    print("3) Train (staff +1, -¥3000)")
    print("4) Rush production (double progress this week, but risk reputation)")
    print("5) Quality focus (reputation +5-10, costs ¥2000)")
    print("6) Change Genre (cost ¥10000, switch to better match trend)")
    print("7) Purchase Upgrade (if affordable)")
    print("8) Next week")
    
    # Non-interactive: auto-choose based on smarter heuristics
    try:
        choice = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = get_auto_choice()
        print(f"Auto-choosing: {choice}")
    
    process_choice(choice)

def get_auto_choice():
    """Return an intelligent auto-choice based on game state."""
    weekly_salary = staff * salary_per_staff
    min_runway = weekly_salary * 3  # Want at least 3 weeks runway
    
    # Emergency: if money is critically low and we have excess staff, fire
    if money < min_runway and staff > 3:
        return "2"
    
    # Upgrade strategy: prioritize income-generating upgrades first
    # Order defined in upgrades_info, we already reordered for income priority
    for upgrade_key, info in upgrades_info.items():
        if not upgrades_purchased[upgrade_key]:
            if money >= info["cost"] + min_runway:
                # Ensure after purchase we still have runway
                return f"upgrade_{upgrade_key}"
    
    # If we're behind on production (progress < 50% of an episode) and have staff
    if production_progress < points_per_episode * 0.5 and staff >= 3 and money > 5000:
        if random.random() < 0.4:  # Slightly higher chance
            return "4"
    
    # Quality focus if reputation needs a boost and we have buffer
    if reputation < 60 and money >= (min_runway + 2000):
        return "5"
    
    # Genre switch if mismatched and we have surplus cash
    if player_genre != market_trend and money >= (10000 + min_runway):
        return "6"
    
    # Growth phase: hire/train if we have healthy cash reserves (> 8 weeks)
    if money > weekly_salary * 8:
        if staff < 5:
            return "1" if money >= 5000 else "3"
        if staff < 6:
            return "1"
    
    # Default: advance to next week
    return "8"

def process_choice(choice):
    global money, staff, reputation, fans, production_progress, is_crunching, player_genre, upgrades_purchased, week
    
    if choice.startswith("upgrade_"):
        upgrade_key = choice.replace("upgrade_", "")
        if upgrade_key in upgrades_info:
            info = upgrades_info[upgrade_key]
            if not upgrades_purchased[upgrade_key] and money >= info["cost"]:
                money -= info["cost"]
                upgrades_purchased[upgrade_key] = True
                print(f"{C.GREEN}✨ Purchased: {info['label']} - {info['desc']}{C.END}")
            else:
                print("Can't purchase that upgrade (already purchased or insufficient funds).")
        else:
            print("Invalid upgrade.")
        return
    
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
        # Rush: double production this week, 30% chance of reputation loss
        if random.random() < 0.7:
            is_crunching = True
            print(f"{C.GREEN}Rush initiated! Production doubled this week.{C.END}")
        else:
            reputation -= 10
            print(f"{C.RED}Rush failed! Quality dropped, reputation -10.{C.END}")
    elif choice == "5":
        if money >= 2000:
            quality_gain = random.randint(5, 10)
            money -= 2000; reputation += quality_gain
            print(f"Quality focus paid off. Reputation +{quality_gain}.")
        else:
            print("Not enough money.")
    elif choice == "6":
        print("\nAvailable genres:")
        for i, g in enumerate(GENRES, 1):
            marker = "✓" if g == player_genre else ("↑" if g == market_trend else " ")
            trend_note = f" (TREND!)" if g == market_trend else ""
            print(f"  {i}. {g}{marker}{trend_note}")
        try:
            sel = input("Select genre number (auto-cancels if invalid): ").strip()
            idx = int(sel) - 1
            if 0 <= idx < len(GENRES):
                new_genre = GENRES[idx]
                cost = 10000
                if money >= cost:
                    money -= cost
                    player_genre = new_genre
                    print(f"Switched to {new_genre}. Cost ¥{cost:,}.")
                    if new_genre == market_trend:
                        print(f"{C.MAGENTA}🔥 Perfect! Your genre matches the trend!{C.END}")
                else:
                    print(f"Not enough money (need ¥{cost:,}).")
        except:
            print("Invalid selection.")
    elif choice == "7":
        print("\nAvailable Upgrades:")
        for key, info in upgrades_info.items():
            status_icon = "✓" if upgrades_purchased[key] else "?"
            cost_str = f"¥{info['cost']:,}" if not upgrades_purchased[key] else "OWNED"
            print(f"  {status_icon} {info['label']} - {info['desc']} ({cost_str})")
        # Auto-purchase best affordable in auto-mode; interactive just shows list
        if choice == "7":
            print("Select an upgrade to purchase (in interactive mode).")
    elif choice == "8":
        pass  # Next week
    else:
        print("Invalid choice; skipping.")
    
    week += 1
    check_end()

if __name__ == "__main__":
    print(f"{C.HEAD}{C.BOLD}=== Anime Studio Tycoon ==={C.END}")
    print(f"{C.CYAN}Manage your studio: balance money, staff, reputation, fans.{C.END}")
    print(f"{C.YELLOW}Goal: Complete 10 episodes with ≥50,000 fans and non-negative reputation.{C.END}")
    print()
    print(f"{C.MAGENTA}Your genre: {player_genre} | Current trend: {market_trend}{C.END}")
    if market_trend == player_genre:
        print(f"{C.GREEN}🔥 Perfect match! Your genre is trending!{C.END}")
    print()
    
    # Non-interactive: auto-choosing
    try:
        while True:
            status()
            weekly_update()
    except (EOFError, KeyboardInterrupt):
        print(f"\n{C.YELLOW}Auto-mode: game running non-interactive test (press Ctrl+C to stop){C.END}")
        # Actually continue running since it's auto-mode already
        pass
