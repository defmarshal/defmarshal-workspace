#!/usr/bin/env python3
"""Anime Studio Tycoon — polish/balance update 2026-03-01"""
import random
import sys

# ── ANSI Color Palette ───────────────────────────────────────────────────────
class C:
    G = "\033[92m"  # Green (Money)
    C = "\033[96m"  # Cyan (Rep)
    M = "\033[95m"  # Magenta (Fans)
    Y = "\033[93m"  # Yellow (Staff)
    R = "\033[91m"  # Red (Alerts)
    B = "\033[1m"   # Bold
    E = "\033[0m"   # End

# ── Game state ──────────────────────────────────────────────────────────────
money = 100_000
staff = 5
reputation = 50          # 0‑100
fans = 1_000
week = 0
episodes_target = 10
episodes_completed = 0
salary_per_staff = 2_000  # per week
fan_growth_base = 500     # fans gained each episode (scales with rep)
merch_level = 0           # 0‑3; passive income tier
studio_upgrades = []      # list of upgrade names already purchased

# ── Genre & Market Trends System ─────────────────────────────────────────────
GENRES = ["Shonen", "Isekai", "Slice of Life", "Mecha", "Horror"]
player_genre = "Shonen"
market_trend = random.choice(GENRES)

# ── Expanded event table ─────────────────────────────────────────────────────
# Format: (label, money_delta, staff_delta, rep_delta, fans_delta, description)
EVENTS = [
    ("Viral clip!",         0,      0,   0,  8_000,  "A clip blew up on TubeTube! Fans surge."),
    ("Streaming deal",  15_000,     0,  +5,    500,  "A streaming service bought broadcast rights!"),
    ("Staff burnout",        0,     0,  -5,      0,  "Your team is exhausted. Pay overtime or lose staff."),
    ("Budget overrun",  -12_000,    0,   0,      0,  "Unexpected production costs hit the budget."),
    ("Positive review",      0,     0, +12,  2_000,  "A famous critic raved about your latest episode!"),
    ("Plagiarism claim", -8_000,    0, -10,  -1_000, "A rival studio filed a bogus IP complaint."),
    ("VA scandal",           0,     0, -15, -3_000,  "A voice actor said something controversial online."),
    ("Award nomination",     0,     0, +10,  5_000,  "Your show got nominated for Best New Anime!"),
    ("Convention booth",  -3_000,   0,  +5,  4_000,  "You ran a booth at AnimeCon. Worth it!"),
    ("Talented intern",      0,    +1,  +2,      0,  "A skilled intern joined your team for free!"),
    ("Equipment failure", -5_000,   0,  -5,      0,  "Your render farm crashed. Repair costs hurt."),
    ("Investor interest",  20_000,  0,   0,      0,  "An anime fund is impressed and tops up your budget."),
    ("Rival poaches staff",  0,    -1,   0,      0,  "A rival studio lured away one of your best animators."),
    ("Crowdfunding surge", 10_000,  0,  +3,  6_000,  "Fans funded a bonus episode on Kickstarter!"),
    ("Merchandise boom",    8_000,  0,  +2,  3_000,  "Your merch sold out at every retailer!"),
    ("Delayed episode",   -2_000,   0,  -8, -1_500,  "A missed deadline disappointed the fanbase."),
]

# ── Upgrade shop ─────────────────────────────────────────────────────────────
UPGRADES = {
    "render_farm":   {"cost": 20_000, "label": "Render Farm",    "desc": "Halves salary cost per staff."},
    "social_team":   {"cost": 10_000, "label": "Social Team",    "desc": "+1 000 fans per episode completion."},
    "merch_shop":    {"cost":  8_000, "label": "Merch Shop Lv1", "desc": "Earn ¥3 000/week passive income."},
    "merch_shop_2":  {"cost": 15_000, "label": "Merch Shop Lv2", "desc": "Upgrade passive income to ¥7 000/week."},
    "pr_agency":     {"cost": 12_000, "label": "PR Agency",      "desc": "Reduce negative rep events by half."},
    "star_director": {"cost": 30_000, "label": "Star Director",  "desc": "Reputation gain from episodes is doubled."},
}


# ── Helpers ──────────────────────────────────────────────────────────────────
def clamp_rep():
    global reputation
    reputation = max(0, min(100, reputation))


def draw_bar(val, total, length=10):
    """Draw a visual progress bar."""
    percent = min(1.0, val / total)
    filled = int(length * percent)
    bar = f"{C.G}{'█' * filled}{C.E}{'░' * (length - filled)}"
    return f"|{bar}| {val}/{total}"


def status():
    upgr = f"{C.C}" + (", ".join(studio_upgrades) if studio_upgrades else "none") + f"{C.E}"
    trend_info = f"{C.M}{market_trend}{C.E}"
    genre_info = f"{C.Y}{player_genre}{C.E}"
    print(
        f"\n{C.B}Week {week}{C.E} | "
        f"{C.G}Money: ¥{money:,}{C.E} | {C.Y}Staff: {staff}{C.E} | "
        f"{C.C}Rep: {reputation}{C.E} | {C.M}Fans: {fans:,}{C.E}"
    )
    print(f"  Progress: {draw_bar(episodes_completed, episodes_target)} | Upgrades: {upgr}")
    print(f"  Genre: {genre_info} | Market Trend: {trend_info}")


def check_end():
    if money < 0:
        print(f"\n{C.R}{C.B}💸 Bankruptcy! The studio closes. You lose.{C.E}")
        sys.exit(0)
    if reputation <= 0:
        print(f"\n{C.R}{C.B}💔 Reputation destroyed — sponsors and fans abandoned you. You lose.{C.E}")
        sys.exit(0)
    if staff <= 0:
        print(f"\n{C.R}{C.B}🚪 No staff left — production halts. You lose.{C.E}")
        sys.exit(0)
    if episodes_completed >= episodes_target:
        if fans >= 50_000 and reputation >= 0:
            print(
                f"\n{C.G}{C.B}🎉 Congratulations!{C.E} You completed {episodes_target} episodes with "
                f"{C.M}{fans:,} fans{C.E} and {C.C}reputation {reputation}{C.E}. {C.B}You win!{C.E}"
            )
        else:
            print(
                f"\n{C.Y}📺 Show completed{C.E}, but only {C.M}{fans:,} fans{C.E} (need 50 000) "
                f"and {C.C}rep {reputation}{C.E}. Better luck next season!"
            )
        sys.exit(0)


def fire_and_gain():
    global staff, money
    if staff > 1:
        staff -= 1
        money += 2_000
        print(f"  {C.Y}Fired a staff member.{C.E}")
    else:
        print(f"  {C.R}Can't fire the only staff member!{C.E}")


def apply_event(ev):
    """Apply a random event, handling the burnout special case interactively."""
    global money, staff, reputation, fans
    label, m, s, r, f, desc = ev
    # Visual Box for Events
    border = "═" * (len(desc) + 4)
    print(f"\n{C.R}╔{border}╗{C.E}")
    print(f"{C.R}║{C.E}  {C.B}⚡ EVENT: {label.upper()}{C.E}")
    print(f"{C.R}║{C.E}  {desc}")
    print(f"{C.R}╚{border}╝{C.E}")

    # PR agency halves negative rep damage
    if "pr_agency" in studio_upgrades and r < 0:
        r = r // 2

    if label == "Staff burnout":
        # offer to pay overtime
        try:
            ans = input(f"\n  {C.Y}Pay overtime ¥4 000 to keep morale? (y/n) > {C.E}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            ans = "y" if money >= 4_000 else "n"
            print(f"  Auto: {ans}")
        if ans == "y":
            if money >= 4_000:
                money -= 4_000
                print(f"  {C.G}Overtime paid — staff happy.{C.E}")
                reputation += 2
            else:
                print(f"  {C.R}Can't afford overtime! Staff morale crashes.{C.E}")
                reputation -= 10
                staff = max(1, staff - 1)
        else:
            reputation -= 8
            staff = max(1, staff - 1)
            print(f"  {C.R}Morale dropped, one animator quit.{C.E}")
    else:
        money += m
        staff = max(0, staff + s)
        reputation += r
        fans = max(0, fans + f)

    clamp_rep()
    # Add pacing at the end of the event
    input(f"\n{C.Y}  [Press Enter to continue]{C.E}")


def passive_income():
    """Merch shop passive income."""
    global money, merch_level
    if "merch_shop_2" in studio_upgrades:
        income = 7_000
    elif "merch_shop" in studio_upgrades:
        income = 3_000
    else:
        income = 0
    if income:
        money += income
        print(f"  {C.M}🛍 Merch income: +¥{income:,}{C.E}")


def episode_gain():
    """Fan + rep gain on episode completion."""
    global fans, reputation, episodes_completed
    episodes_completed += 1
    # Compounding fan growth: +10% of existing fans (hype/word-of-mouth)
    hype_bonus = int(fans * 0.10)
    base = fan_growth_base + (reputation - 50) * 20 + hype_bonus
    if "social_team" in studio_upgrades:
        base += 1_000
    
    # Market trend bonus
    trend_mult = 1.5 if player_genre == market_trend else 1.0
    gained = int(max(200, base + random.randint(-200, 500)) * trend_mult)
    
    if trend_mult > 1.0:
        print(f"  {C.M}🔥 TREND BONUS: {player_genre} is hot right now!{C.E}")
    
    rep_gain = random.randint(1, 5)
    if "star_director" in studio_upgrades:
        rep_gain *= 2
    reputation = min(100, reputation + rep_gain)
    print(f"  {C.G}🎬 Episode {episodes_completed} completed! +{gained:,} fans, +{rep_gain} rep{C.E}")


def show_choices():
    print(f"\n{C.B}Choices:{C.E}")
    print(f"  1) {C.Y}Hire animator{C.E}      (+1 staff, -¥5 000)")
    print(f"  2) {C.Y}Fire animator{C.E}      (-1 staff, +¥2 000)")
    print(f"  3) {C.Y}Train junior{C.E}       (+1 staff, -¥3 000)")
    print(f"  4) {C.R}Rush episode{C.E}       (fast fans, risk rep)")
    print(f"  5) {C.C}Quality focus{C.E}      (+5 rep, -¥2 000)")
    print(f"  6) {C.M}Run fan campaign{C.E}   (+fans, -¥4 000)")
    print(f"  7) {C.B}Upgrade shop{C.E}       (permanent upgrades)")
    print(f"  8) {C.G}Next week{C.E}")


def upgrade_shop():
    """Interactive upgrade purchase."""
    global money
    print(f"\n  {C.B}=== Upgrade Shop ==={C.E}")
    available = [(k, v) for k, v in UPGRADES.items() if k not in studio_upgrades]
    # hide merch_shop_2 unless merch_shop is owned
    if "merch_shop" not in studio_upgrades:
        available = [(k, v) for k, v in available if k != "merch_shop_2"]
    if not available:
        print(f"  {C.G}All upgrades purchased!{C.E}")
        return
    for i, (k, v) in enumerate(available, 1):
        print(f"  {i}) {C.C}{v['label']}{C.E} — ¥{v['cost']:,}  ·  {v['desc']}")
    print(f"  {C.Y}0) Cancel{C.E}")
    try:
        sel = int(input(f"  {C.B}Buy > {C.E}").strip())
    except (ValueError, EOFError, KeyboardInterrupt):
        sel = 0
        print(f"  Auto: cancel")
    if sel == 0 or sel > len(available):
        print(f"  {C.Y}No purchase.{C.E}")
        return
    key, upg = available[sel - 1]
    if money >= upg["cost"]:
        money -= upg["cost"]
        studio_upgrades.append(key)
        # render_farm: immediately halve salary cost
        if key == "render_farm":
            global salary_per_staff
            salary_per_staff = 1_000
        print(f"  {C.G}✅ Purchased: {upg['label']}{C.E}")
    else:
        print(f"  {C.R}❌ Not enough money (need ¥{upg['cost']:,}, have ¥{money:,}){C.E}")


def auto_choice(choice_input: str) -> str:
    """Heuristic AI for non-interactive / auto mode."""
    # Try to buy render_farm first (best ROI)
    if "render_farm" not in studio_upgrades and money >= 20_000:
        return "7_render_farm"
    if "merch_shop" not in studio_upgrades and money >= 10_000:
        return "7_merch_shop"
    if "merch_shop_2" not in studio_upgrades and "merch_shop" in studio_upgrades and money >= 15_000:
        return "7_merch_shop_2"
    if reputation < 40 and money >= 2_000:
        return "5"
    # Prioritize fan campaigns heavily when fans are below target
    if fans < 50_000 and money >= 4_000:
        return "6"
    if staff < 4 and money >= 5_000:
        return "1"
    if money < 3_000 and staff > 3:
        return "2"
    if reputation >= 70 and money >= 5_000 and staff < 7:
        return "1"
    return "8"


def weekly_update():
    global money, staff, reputation, fans, week, salary_per_staff, market_trend

    # Passive income first
    passive_income()

    # Pay salaries
    salary = staff * salary_per_staff
    money -= salary
    print(f"  {C.Y}💴 Salaries paid: -¥{salary:,}{C.E}")

    # Random event (15 % chance)
    if random.random() < 0.15:
        apply_event(random.choice(EVENTS))

    # Episode progress: every 2 weeks completes an episode
    if week % 2 == 1:
        episode_gain()

    # Market trend rotates every 5 weeks
    if week > 0 and week % 5 == 0:
        old_trend = market_trend
        market_trend = random.choice(GENRES)
        print(f"  {C.M}📈 Market trend shifted: {old_trend} → {market_trend}{C.E}")

    status()
    check_end()
    show_choices()

    try:
        choice = input(f"{C.B}> {C.E}").strip()
    except (EOFError, KeyboardInterrupt):
        choice = auto_choice("")
        # handle auto upgrade sub-choices
        if choice.startswith("7_"):
            upgrade_key = choice.split("_", 1)[1]
            upg = UPGRADES.get(upgrade_key)
            if upg and upgrade_key not in studio_upgrades and money >= upg["cost"]:
                money -= upg["cost"]
                studio_upgrades.append(upgrade_key)
                if upgrade_key == "render_farm":
                    salary_per_staff = 1_000
                print(f"  {C.G}Auto-purchased: {upg['label']}{C.E}")
            choice = "8"
        else:
            print(f"  Auto-choosing: {choice}")

    if choice == "1":
        if money >= 5_000:
            money -= 5_000
            staff += 1
            print(f"  {C.G}Hired a new animator.{C.E}")
        else:
            print(f"  {C.R}Not enough money.{C.E}")
    elif choice == "2":
        fire_and_gain()
    elif choice == "3":
        if money >= 3_000:
            money -= 3_000
            staff += 1
            print(f"  {C.G}Trained a junior — they levelled up!{C.E}")
        else:
            print(f"  {C.R}Not enough money.{C.E}")
    elif choice == "4":
        # Rush episode
        if random.random() < 0.65:
            gained = random.randint(1_500, 5_000)
            fans += gained
            print(f"  {C.G}⚡ Rush succeeded! +{gained:,} fans.{C.E}")
        else:
            reputation -= random.randint(8, 15)
            fans = max(0, fans - random.randint(500, 1_500))
            clamp_rep()
            print(f"  {C.R}⚡ Rush failed! Reputation and fans dropped.{C.E}")
    elif choice == "5":
        if money >= 2_000:
            money -= 2_000
            reputation = min(100, reputation + 5)
            print(f"  {C.C}Quality focus paid off. +5 rep.{C.E}")
        else:
            print(f"  {C.R}Not enough money.{C.E}")
    elif choice == "6":
        if money >= 4_000:
            money -= 4_000
            gained = random.randint(3_000, 8_000)
            fans += gained
            print(f"  {C.M}📣 Fan campaign launched! +{gained:,} fans.{C.E}")
        else:
            print(f"  {C.R}Not enough money for a campaign.{C.E}")
    elif choice == "7":
        upgrade_shop()
    elif choice == "8":
        pass
    else:
        print(f"  {C.R}Invalid choice; advancing week.{C.E}")

    week += 1
    check_end()


def select_genre():
    """Let player choose their studio's specialty genre."""
    global player_genre
    print(f"\n{C.B}╔══════════════════════════════════════════╗{C.E}")
    print(f"{C.B}║     {C.M}SELECT YOUR STUDIO GENRE{C.B}              ║{C.E}")
    print(f"{C.B}╚══════════════════════════════════════════╝{C.E}")
    for i, genre in enumerate(GENRES, 1):
        print(f"  {i}) {C.Y}{genre}{C.E}")
    
    while True:
        try:
            sel = int(input(f"\n{C.B}Choose genre (1-{len(GENRES)}) > {C.E}").strip())
            if 1 <= sel <= len(GENRES):
                player_genre = GENRES[sel - 1]
                print(f"  {C.G}✅ Studio specializes in {player_genre}!{C.E}")
                break
            else:
                print(f"  {C.R}Invalid selection.{C.E}")
        except (ValueError, EOFError, KeyboardInterrupt):
            print(f"  {C.R}Please enter a number.{C.E}")


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"{C.B}╔══════════════════════════════════════════╗{C.E}")
    print(f"{C.B}║       {C.C}ANIME STUDIO TYCOON  v1.2{C.B}          ║{C.E}")
    print(f"{C.B}╚══════════════════════════════════════════╝{C.E}")
    print(f"{C.Y}Manage your studio: balance money, staff, reputation, and fans.{C.E}")
    print(f"{C.B}Goal:{C.E} Complete 10 episodes with {C.M}≥50 000 fans{C.E} and {C.C}positive reputation{C.E}.\n")
    print(f"{C.Y}Tips:{C.E} Hire staff early, invest in upgrades, and watch your budget!")
    print(f"{C.M}NEW:{C.E} Match your genre to market trends for +50% fan growth!")
    
    # Genre selection at game start
    select_genre()
    
    # Initialize market trend
    print(f"\n{C.M}📈 Current market trend: {market_trend}{C.E}")
    if player_genre == market_trend:
        print(f"  {C.G}✨ Perfect! Your genre matches the trend!{C.E}")
    
    print()
    while True:
        weekly_update()