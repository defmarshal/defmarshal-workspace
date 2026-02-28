#!/usr/bin/env python3
"""
Anime Studio Tycoon v1.2
Manage your anime studio: hire staff, balance budgets, build reputation.
Goal: Complete 10 episodes with >50k fans and non-negative reputation.
"""
import random
import sys

# ─── Game State ────────────────────────────────────────────────────────────────
money = 100_000
staff = 5
reputation = 50
fans = 1_000
week = 0
episodes_target = 10
episodes_completed = 0
salary_per_staff = 2_000
merch_unlocked = False
sponsor_deal = 0           # weeks remaining on sponsor deal
sponsor_income = 0
staff_morale = 70          # 0-100; affects episode quality
streak_bonus = 0           # consecutive quality-focus weeks

# ─── Expanded Event Pool ───────────────────────────────────────────────────────
# (description, money_delta, staff_delta, reputation_delta, fans_delta, morale_delta)
EVENTS = [
    ("Viral clip posted online!",          0,      0,  +5,  +8_000,  +10),
    ("Staff burnout incident",             0,     -1,   0,       0,  -20),
    ("Budget overrun on key scene",   -8_000,      0,  -5,       0,   -5),
    ("Glowing review from critic",         0,      0, +15,  +3_000,  +15),
    ("Crowdfunding campaign succeeds",+15_000,     0, +10,  +5_000,  +20),
    ("Rival studio poaches animator",      0,     -1,  -5,       0,  -10),
    ("Convention appearance pays off",     0,      0, +10,  +4_000,  +10),
    ("Animation error goes viral (bad)", -5_000,   0, -10,  -2_000,  -15),
    ("Studio fire drill panic",        -3_000,     0,   0,       0,   -5),
    ("Fan art contest boosts buzz",        0,      0,  +5,  +6_000,  +10),
    ("Investor shows interest",       +20_000,     0,   0,       0,    0),
    ("Key animator resigns",               0,     -2, -10,       0,  -20),
    ("Music composer joins (free)",        0,      0, +10,       0,  +15),
    ("Streaming deal offered",        +10_000,     0,  +5,  +2_000,   +5),
    ("Staff wellness day",             -2_000,     0,   0,       0,  +25),
    ("Anime expo spotlight",               0,      0, +20, +10_000,  +10),
    ("Merchandise prototype fails",    -4_000,     0,  -5,       0,  -10),
    ("Voice actor controversy",            0,      0, -15,  -5_000,  -15),
    ("Sequel rumors fuel hype",            0,      0,  +5, +12_000,   +5),
    ("Late-night crunch week",         +5_000,     0,  -5,       0,  -20),
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def sep():
    print("─" * 55)

def status():
    morale_bar = "█" * (staff_morale // 10) + "░" * (10 - staff_morale // 10)
    print(f"\n╔══ Week {week:>3} ═══════════════════════════════════╗")
    print(f"║  💴 Money      : ¥{money:>10,}")
    print(f"║  👥 Staff      : {staff}   Morale: [{morale_bar}] {staff_morale}%")
    print(f"║  ⭐ Reputation : {reputation}")
    print(f"║  👥 Fans       : {fans:,}")
    print(f"║  📺 Episodes   : {episodes_completed}/{episodes_target}")
    if sponsor_deal > 0:
        print(f"║  🤝 Sponsor    : ¥{sponsor_income:,}/wk ({sponsor_deal} wks left)")
    if merch_unlocked:
        print(f"║  🛍️  Merch income: ¥{merch_revenue():,}/wk")
    print(f"╚{'═'*45}╝")


def merch_revenue():
    """Weekly passive merch income based on fans and reputation."""
    if not merch_unlocked:
        return 0
    return int(fans * 0.02 * (reputation / 50))


def fan_growth():
    """Each week fans grow a little passively based on rep and episodes."""
    global fans
    base = int(reputation * 0.5 * (episodes_completed + 1) * 0.1)
    fans += max(0, base + random.randint(-50, 200))


def check_end():
    if money < 0:
        print("\n💸 BANKRUPTCY! You couldn't pay the bills. Studio closed. You LOSE.\n")
        sys.exit(0)
    if reputation <= 0:
        print("\n💔 REPUTATION DESTROYED! No one wants to work with you. You LOSE.\n")
        sys.exit(0)
    if staff <= 0:
        print("\n👤 Everyone quit! You can't make anime alone. You LOSE.\n")
        sys.exit(0)
    if episodes_completed >= episodes_target:
        if fans >= 50_000:
            print(f"\n🎉 VICTORY! You completed all {episodes_target} episodes!")
            print(f"   Final fans: {fans:,} | Reputation: {reputation} | Money: ¥{money:,}")
            print("   Your studio is legendary! ✨\n")
        else:
            print(f"\n🎬 You finished the series, but only had {fans:,} fans (need 50,000).")
            print("   The show was decent but never found its audience. Studio dissolved.\n")
        sys.exit(0)


def trigger_event():
    """10% chance of random event each week."""
    global money, staff, reputation, fans, staff_morale
    if random.random() < 0.12:
        ev = random.choice(EVENTS)
        desc, dm, ds, dr, df, dmorale = ev
        print(f"\n  📰 EVENT: {desc}")
        if dm != 0:
            money += dm
            print(f"     {'+'if dm>0 else ''}{dm:,} ¥")
        if ds != 0:
            staff = max(1, staff + ds)
            print(f"     {'+'if ds>0 else ''}{ds} staff")
        if dr != 0:
            reputation += dr
            print(f"     {'+'if dr>0 else ''}{dr} reputation")
        if df != 0:
            fans = max(0, fans + df)
            print(f"     {'+'if df>0 else ''}{df:,} fans")
        if dmorale != 0:
            staff_morale = max(0, min(100, staff_morale + dmorale))
            print(f"     Morale {'+'if dmorale>0 else ''}{dmorale}% → {staff_morale}%")


def print_choices():
    print("\n  Actions:")
    print("  1) Hire animator       (+1 staff, -¥5,000)")
    print("  2) Fire animator       (+¥2,000,  -1 staff)")
    print("  3) Train junior        (+1 staff, -¥3,000)")
    print("  4) Rush production     (episode faster, -10 rep risk)")
    print("  5) Quality focus       (+5 rep, -¥2,000, +morale)")
    print("  6) Morale event        (+20 morale, -¥1,500)")
    print("  7) Merch campaign      (unlock passive income, -¥10,000, one-time)")
    print("  8) Seek sponsor        (sponsor deal for 5 weeks)")
    print("  9) Next week           (advance without action)")


def auto_choose():
    """Heuristic AI for non-interactive / demo mode."""
    global merch_unlocked, sponsor_deal
    # Unlock merch if we have money and fans
    if not merch_unlocked and money >= 15_000 and fans >= 5_000:
        return "7"
    # Seek sponsor if broke and no deal
    if money < 20_000 and sponsor_deal == 0:
        return "8"
    # Morale boost if very low
    if staff_morale < 30 and money >= 1_500:
        return "6"
    # Hire if staff low and money ok
    if staff < 6 and money >= 10_000:
        return "1"
    # Quality focus if rep low and can afford
    if reputation < 60 and money >= 2_000:
        return "5"
    # Train if staff very low
    if staff < 4 and money >= 3_000:
        return "3"
    # Fire if critically broke
    if money < 5_000 and staff > 3:
        return "2"
    return "9"


# ─── Main Weekly Loop ─────────────────────────────────────────────────────────

def weekly_update():
    global money, staff, reputation, fans, week, episodes_completed
    global merch_unlocked, sponsor_deal, sponsor_income, staff_morale, streak_bonus

    # ── Income phase ──
    # Sponsor income
    if sponsor_deal > 0:
        money += sponsor_income
        sponsor_deal -= 1

    # Passive merch income
    if merch_unlocked:
        rev = merch_revenue()
        money += rev

    # Fan-driven ad revenue (small)
    ad_rev = int(fans * 0.005 * (reputation / 50))
    money += ad_rev

    # Passive fan growth
    fan_growth()

    # ── Expenses ──
    salary = staff * salary_per_staff
    # Morale affects salary efficiency; low morale = hidden productivity loss
    if staff_morale < 40:
        morale_penalty = int(salary * 0.1)
        money -= morale_penalty
        print(f"  ⚠️  Low morale! Extra overtime costs: ¥{morale_penalty:,}")
    money -= salary

    # Natural morale drift
    staff_morale = max(10, min(100, staff_morale - 2 + random.randint(-3, 3)))

    # ── Random event ──
    trigger_event()

    # ── Player choice ──
    print_choices()
    try:
        choice = input("\n  > ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = auto_choose()
        print(f"  [auto] → {choice}")

    if choice == "1":
        if money >= 5_000:
            money -= 5_000
            staff += 1
            staff_morale = max(0, min(100, staff_morale + 5))
            print("  ✅ Hired a new animator!")
        else:
            print("  ❌ Not enough money to hire.")

    elif choice == "2":
        if staff > 2:
            staff -= 1
            money += 2_000
            staff_morale = max(0, staff_morale - 10)
            print("  📤 Fired a staff member. (Morale took a hit)")
        else:
            print("  ❌ Can't fire below 2 staff!")

    elif choice == "3":
        if money >= 3_000 and staff > 0:
            money -= 3_000
            staff += 1
            staff_morale = max(0, min(100, staff_morale + 10))
            print("  🎓 Trained a junior — they're now a full animator!")
        else:
            print("  ❌ Not enough money or no staff to train.")

    elif choice == "4":
        # Rush: free episode but risk reputation
        if random.random() < 0.55 + staff_morale * 0.002:
            bonus_fans = random.randint(1_000, 4_000)
            fans += bonus_fans
            print(f"  ⚡ Rush succeeded! Fans +{bonus_fans:,}")
            streak_bonus = 0
        else:
            reputation -= 10
            staff_morale = max(0, staff_morale - 15)
            print("  💥 Rush failed! Quality tanks. Reputation -10, Morale -15")

    elif choice == "5":
        if money >= 2_000:
            money -= 2_000
            reputation += 5
            staff_morale = max(0, min(100, staff_morale + 8))
            streak_bonus += 1
            bonus_fans = streak_bonus * 200
            fans += bonus_fans
            print(f"  🌟 Quality focus paid off! Rep +5, Morale +8, Fans +{bonus_fans} (streak {streak_bonus})")
        else:
            print("  ❌ Not enough money for quality focus.")

    elif choice == "6":
        if money >= 1_500:
            money -= 1_500
            staff_morale = max(0, min(100, staff_morale + 20))
            reputation += 2
            print("  🎉 Team morale event! Morale +20, Rep +2")
        else:
            print("  ❌ Not enough money for morale event.")

    elif choice == "7":
        if merch_unlocked:
            print("  ℹ️  Merch is already active!")
        elif money >= 10_000:
            money -= 10_000
            merch_unlocked = True
            print(f"  🛍️  Merch campaign launched! Now earning ¥{merch_revenue():,}/wk passively.")
        else:
            print("  ❌ Need ¥10,000 to launch merch campaign.")

    elif choice == "8":
        if sponsor_deal > 0:
            print(f"  ℹ️  Already in a sponsor deal ({sponsor_deal} wks left).")
        elif reputation >= 30:
            sponsor_income = int(reputation * 200 + fans * 0.1)
            sponsor_deal = 5
            print(f"  🤝 Sponsor deal secured! ¥{sponsor_income:,}/wk for 5 weeks.")
        else:
            print("  ❌ Reputation too low for sponsors (need ≥30).")

    elif choice == "9":
        streak_bonus = 0
        print("  ⏭️  Advancing to next week...")

    else:
        print("  ❓ Invalid choice; skipping.")
        streak_bonus = 0

    # ── Episode production: every 2 weeks ──
    if week % 2 == 1 and episodes_completed < episodes_target:
        ep_quality = max(1, int((reputation + staff_morale) / 20))
        fan_boost = ep_quality * random.randint(500, 1_500)
        fans += fan_boost
        money += episodes_completed * 1_000  # growing licensing per ep
        episodes_completed += 1
        print(f"\n  📺 Episode {episodes_completed} aired! Fans +{fan_boost:,} (quality {ep_quality}/10)")

    week += 1
    check_end()


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║        ANIME STUDIO TYCOON  v1.2             ║")
    print("║  Manage your studio — build an anime empire  ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  Goal: 10 episodes + 50,000 fans             ║")
    print("║  Balance: money, staff, reputation, morale   ║")
    print("║  New: merch, sponsors, 20 random events!     ║")
    print("╚══════════════════════════════════════════════╝\n")
    while True:
        status()
        weekly_update()
