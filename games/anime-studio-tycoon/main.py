#!/usr/bin/env python3
"""Anime Studio Tycoon — polish/balance update 2026-03-01"""
import random
import sys

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
}


# ── Helpers ──────────────────────────────────────────────────────────────────
def clamp_rep():
    global reputation
    reputation = max(0, min(100, reputation))


def status():
    upgr = ", ".join(studio_upgrades) if studio_upgrades else "none"
    print(
        f"\nWeek {week} | Money: ¥{money:,} | Staff: {staff} | "
        f"Rep: {reputation} | Fans: {fans:,} | Episodes: {episodes_completed}/{episodes_target}"
    )
    print(f"  Upgrades: {upgr}")


def check_end():
    if money < 0:
        print("\n💸 Bankruptcy! The studio closes. You lose.")
        sys.exit(0)
    if reputation <= 0:
        print("\n💔 Reputation destroyed — sponsors and fans abandoned you. You lose.")
        sys.exit(0)
    if staff <= 0:
        print("\n🚪 No staff left — production halts. You lose.")
        sys.exit(0)
    if episodes_completed >= episodes_target:
        if fans >= 50_000 and reputation >= 0:
            print(
                f"\n🎉 Congratulations! You completed {episodes_target} episodes with "
                f"{fans:,} fans and reputation {reputation}. You win!"
            )
        else:
            print(
                f"\n📺 Show completed, but only {fans:,} fans (need 50 000) "
                f"and rep {reputation}. Better luck next season!"
            )
        sys.exit(0)


def fire_and_gain():
    global staff, money
    if staff > 1:
        staff -= 1
        money += 2_000
        print("  Fired a staff member.")
    else:
        print("  Can't fire the only staff member!")


def apply_event(ev):
    """Apply a random event, handling the burnout special case interactively."""
    global money, staff, reputation, fans
    label, m, s, r, f, desc = ev
    print(f"\n⚡ EVENT: {label}")
    print(f"   {desc}")

    # PR agency halves negative rep damage
    if "pr_agency" in studio_upgrades and r < 0:
        r = r // 2

    if label == "Staff burnout":
        # offer to pay overtime
        try:
            ans = input("  Pay overtime ¥4 000 to keep morale? (y/n) > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            ans = "y" if money >= 4_000 else "n"
            print(f"  Auto: {ans}")
        if ans == "y":
            if money >= 4_000:
                money -= 4_000
                print("  Overtime paid — staff happy.")
                reputation += 2
            else:
                print("  Can't afford overtime! Staff morale crashes.")
                reputation -= 10
                staff = max(1, staff - 1)
        else:
            reputation -= 8
            staff = max(1, staff - 1)
            print("  Morale dropped, one animator quit.")
    else:
        money += m
        staff = max(0, staff + s)
        reputation += r
        fans = max(0, fans + f)

    clamp_rep()


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
        print(f"  🛍 Merch income: +¥{income:,}")


def episode_gain():
    """Fan + rep gain on episode completion."""
    global fans, reputation, episodes_completed
    episodes_completed += 1
    base = fan_growth_base + (reputation - 50) * 20
    if "social_team" in studio_upgrades:
        base += 1_000
    gained = max(200, base + random.randint(-200, 500))
    fans += gained
    rep_gain = random.randint(1, 5)
    reputation = min(100, reputation + rep_gain)
    print(f"  🎬 Episode {episodes_completed} completed! +{gained:,} fans, +{rep_gain} rep")


def show_choices():
    print("\nChoices:")
    print("  1) Hire animator      (+1 staff, -¥5 000)")
    print("  2) Fire animator      (-1 staff, +¥2 000)")
    print("  3) Train junior       (+1 staff, -¥3 000)")
    print("  4) Rush episode       (fast fans, risk rep)")
    print("  5) Quality focus      (+5 rep, -¥2 000)")
    print("  6) Run fan campaign   (+fans, -¥4 000)")
    print("  7) Upgrade shop       (permanent upgrades)")
    print("  8) Next week")


def upgrade_shop():
    """Interactive upgrade purchase."""
    global money
    print("\n  === Upgrade Shop ===")
    available = [(k, v) for k, v in UPGRADES.items() if k not in studio_upgrades]
    # hide merch_shop_2 unless merch_shop is owned
    if "merch_shop" not in studio_upgrades:
        available = [(k, v) for k, v in available if k != "merch_shop_2"]
    if not available:
        print("  All upgrades purchased!")
        return
    for i, (k, v) in enumerate(available, 1):
        print(f"  {i}) {v['label']} — ¥{v['cost']:,}  ·  {v['desc']}")
    print("  0) Cancel")
    try:
        sel = int(input("  Buy > ").strip())
    except (ValueError, EOFError, KeyboardInterrupt):
        sel = 0
        print("  Auto: cancel")
    if sel == 0 or sel > len(available):
        print("  No purchase.")
        return
    key, upg = available[sel - 1]
    if money >= upg["cost"]:
        money -= upg["cost"]
        studio_upgrades.append(key)
        # render_farm: immediately halve salary cost
        if key == "render_farm":
            global salary_per_staff
            salary_per_staff = 1_000
        print(f"  ✅ Purchased: {upg['label']}")
    else:
        print(f"  ❌ Not enough money (need ¥{upg['cost']:,}, have ¥{money:,})")


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
    global money, staff, reputation, fans, week, salary_per_staff

    # Passive income first
    passive_income()

    # Pay salaries
    salary = staff * salary_per_staff
    money -= salary
    print(f"  💴 Salaries paid: -¥{salary:,}")

    # Random event (15 % chance)
    if random.random() < 0.15:
        apply_event(random.choice(EVENTS))

    # Episode progress: every 2 weeks completes an episode
    if week % 2 == 1:
        episode_gain()

    status()
    check_end()
    show_choices()

    try:
        choice = input("> ").strip()
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
                print(f"  Auto-purchased: {upg['label']}")
            choice = "8"
        else:
            print(f"  Auto-choosing: {choice}")

    if choice == "1":
        if money >= 5_000:
            money -= 5_000
            staff += 1
            print("  Hired a new animator.")
        else:
            print("  Not enough money.")
    elif choice == "2":
        fire_and_gain()
    elif choice == "3":
        if money >= 3_000:
            money -= 3_000
            staff += 1
            print("  Trained a junior — they levelled up!")
        else:
            print("  Not enough money.")
    elif choice == "4":
        # Rush episode
        if random.random() < 0.65:
            gained = random.randint(1_500, 5_000)
            fans += gained
            print(f"  ⚡ Rush succeeded! +{gained:,} fans.")
        else:
            reputation -= random.randint(8, 15)
            fans = max(0, fans - random.randint(500, 1_500))
            clamp_rep()
            print("  ⚡ Rush failed! Reputation and fans dropped.")
    elif choice == "5":
        if money >= 2_000:
            money -= 2_000
            reputation = min(100, reputation + 5)
            print("  Quality focus paid off. +5 rep.")
        else:
            print("  Not enough money.")
    elif choice == "6":
        if money >= 4_000:
            money -= 4_000
            gained = random.randint(3_000, 8_000)
            fans += gained
            print(f"  📣 Fan campaign launched! +{gained:,} fans.")
        else:
            print("  Not enough money for a campaign.")
    elif choice == "7":
        upgrade_shop()
    elif choice == "8":
        pass
    else:
        print("  Invalid choice; advancing week.")

    week += 1
    check_end()


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║       ANIME STUDIO TYCOON  v1.1          ║")
    print("╚══════════════════════════════════════════╝")
    print("Manage your studio: balance money, staff, reputation, and fans.")
    print("Goal: Complete 10 episodes with ≥50 000 fans and positive reputation.\n")
    print("Tips: Hire staff early, invest in upgrades, and watch your budget!")
    print()
    while True:
        weekly_update()
