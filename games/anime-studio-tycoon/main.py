#!/usr/bin/env python3
"""Anime Studio Tycoon — v1.1 (polished)
Manage your anime studio: balance money, staff, reputation, and fans.
Goal: Complete 10 episodes with >50 000 fans and non-negative reputation.
"""
import random
import sys

# ── Game state ────────────────────────────────────────────────────────────────
money = 100_000
staff = 5
reputation = 50      # 0-100 scale
fans = 1_000
week = 0
episodes_target = 10
episodes_completed = 0

# Tuning knobs
SALARY_PER_STAFF = 1_200   # was 2000 — softer weekly drain
FAN_MERCH_RATE = 0.005     # each fan earns ¥0.005/week from merch sales
FAN_GROWTH_BASE = 0.02     # fans grow 2 % per episode aired (cumulative)
REP_FAN_MULT = 1.5         # reputation amplifies fan growth

# ── Extended event table ──────────────────────────────────────────────────────
# (description, Δmoney, Δstaff, Δrep, Δfans)
EVENTS = [
    # Original events
    ("Viral clip on social media!",         0,      0,   +5,  +8_000),
    ("Staff burnout strikes the team.",      0,      0,   -5,   0),
    ("Budget overrun on key animation.",   -8_000,   0,    0,   0),
    ("Positive critic review!",             0,      0,  +10,  +3_000),
    # New events ↓
    ("A famous voice actor joins on loan!",  0,     +1,  +8,  +5_000),
    ("Equipment failure in the render farm.", -6_000, 0,  -3,   0),
    ("Studio featured in an anime magazine!",  0,    0,  +12, +10_000),
    ("Competitor releases similar show.",    0,      0,   -5,  -2_000),
    ("Crowdfunding campaign goes viral!",  +15_000,  0,  +5,  +6_000),
    ("Key animator quits unexpectedly.",     0,     -1,  -4,   0),
    ("Award nomination announced!",          0,      0,  +15, +12_000),
    ("Streaming platform adds your library.", 0,     0,   +8, +20_000),
    ("A character becomes a meme.",           0,     0,  +3,  +15_000),
    ("Tax audit causes delay.",            -4_000,   0,  -2,   0),
    ("Fan convention sells out your booth!", +5_000, 0,  +6,  +4_000),
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def status():
    print(
        f"Week {week:>2} | Money: ¥{money:>9,} | Staff: {staff:>2} | "
        f"Rep: {reputation:>3} | Fans: {fans:>8,} | Episodes: {episodes_completed}/{episodes_target}"
    )


def check_end():
    if money < 0:
        print("\n💸 Bankruptcy! You've run out of money. GAME OVER.")
        sys.exit(0)
    if reputation < 0:
        print("\n📉 Reputation collapsed! The studio shuts down. GAME OVER.")
        sys.exit(0)
    if staff <= 0:
        print("\n😢 Everyone quit! The studio is empty. GAME OVER.")
        sys.exit(0)
    if episodes_completed >= episodes_target:
        if fans >= 50_000:
            print(
                f"\n🎉 You completed {episodes_target} episodes with {fans:,} fans "
                f"and {reputation} reputation.\n🏆 CONGRATULATIONS — YOU WIN!"
            )
        else:
            print(
                f"\n📺 You finished {episodes_target} episodes but only have {fans:,} fans "
                f"(need 50 000). The series was a flop. TRY AGAIN."
            )
        sys.exit(0)


def weekly_update():
    global money, staff, reputation, fans, week, episodes_completed

    # ── Revenue & costs ──────────────────────────────────────────────────────
    merch_income = int(fans * FAN_MERCH_RATE)
    money += merch_income
    money -= staff * SALARY_PER_STAFF

    if merch_income > 0:
        print(f"  Merch income: +¥{merch_income:,}")

    # ── Fan growth (passive) ─────────────────────────────────────────────────
    # Fans grow each week proportional to reputation & staff quality
    growth = int(fans * FAN_GROWTH_BASE * (reputation / 50) * (staff / 5) * REP_FAN_MULT)
    if growth > 0:
        fans += growth

    # ── Random event (20 % chance) ───────────────────────────────────────────
    if random.random() < 0.20:
        ev = random.choice(EVENTS)
        desc, dm, ds, dr, df = ev
        print(f"\n  📢 Event: {desc}")
        money += dm
        fans = max(0, fans + df)
        reputation = max(-999, reputation + dr)

        if ds != 0:
            # Staff-change event — show special message
            if ds < 0:
                staff = max(1, staff + ds)
                print(f"     → Lost {abs(ds)} staff member(s)!")
            else:
                staff += ds
                print(f"     → Gained {ds} staff member(s)!")

        # Special handling: Staff burnout — pay overtime or lose staff
        if "burnout" in desc:
            if money >= 4_000:
                money -= 4_000
                reputation += 2
                print("     → Paid overtime (¥4 000). Staff morale recovers slightly.")
            else:
                staff = max(1, staff - 2)
                reputation -= 3
                print("     → Couldn't pay overtime. 2 staff quit!")

    # ── Player choices ───────────────────────────────────────────────────────
    print("\nChoices:")
    print("  1) Hire animator     (+1 staff, -¥5 000)")
    print("  2) Fire animator     (+¥2 000, -1 staff)")
    print("  3) Train junior      (+1 staff, -¥3 000)")
    print("  4) Rush episode      (faster, but quality risk)")
    print("  5) Quality focus     (+5 rep, -¥2 000)")
    print("  6) Marketing push    (+fans, -¥4 000)")
    print("  7) Next week →")

    try:
        choice = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        # ── Smart auto-play heuristic ────────────────────────────────────────
        if money > 60_000 and staff < 8 and money >= 5_000:
            choice = "1"   # Grow team when flush
        elif money < 8_000 and staff > 3:
            choice = "2"   # Cut costs when tight
        elif fans < 20_000 and money >= 4_000:
            choice = "6"   # Marketing when fans low
        elif reputation < 55 and money >= 2_000:
            choice = "5"   # Fix rep when it's slipping
        elif money >= 3_000 and staff < 6:
            choice = "3"   # Train if affordable
        else:
            choice = "7"
        print(f"Auto: {choice}")

    # ── Apply choice ─────────────────────────────────────────────────────────
    if choice == "1":
        if money >= 5_000:
            money -= 5_000
            staff += 1
            print("🎨 Hired a new animator.")
        else:
            print("💰 Not enough money to hire.")
    elif choice == "2":
        if staff > 1:
            staff -= 1
            money += 2_000
            print("📋 Fired an animator.")
        else:
            print("❌ Can't fire the last staff member!")
    elif choice == "3":
        if money >= 3_000 and staff >= 1:
            money -= 3_000
            staff += 1
            print("📚 Trained a junior animator — they're now full staff!")
        else:
            print("❌ Not enough money or no staff to train.")
    elif choice == "4":
        if random.random() < 0.65:
            bonus_fans = random.randint(500, 3_000)
            fans += bonus_fans
            print(f"🚀 Rush succeeded! Gained {bonus_fans:,} fans.")
        else:
            rep_loss = random.randint(8, 15)
            reputation -= rep_loss
            print(f"💥 Rush failed! Quality issues — reputation -{rep_loss}.")
    elif choice == "5":
        if money >= 2_000:
            money -= 2_000
            reputation = min(100, reputation + 5)
            print("✨ Quality focus paid off. Reputation +5.")
        else:
            print("💰 Not enough money for quality focus.")
    elif choice == "6":
        if money >= 4_000:
            money -= 4_000
            boost = int(fans * 0.15) + random.randint(500, 2_000)
            fans += boost
            print(f"📣 Marketing push! Fans +{boost:,}.")
        else:
            print("💰 Not enough money for marketing.")
    elif choice == "7":
        pass   # Advance week
    else:
        print("⚠️  Invalid choice; skipping.")

    # ── Episode production (every 2 weeks) ───────────────────────────────────
    if week % 2 == 0 and episodes_completed < episodes_target:
        episodes_completed += 1
        ep_fans = int(fans * 0.08 * (reputation / 50))
        fans += ep_fans
        reputation = min(100, reputation + 2)
        print(f"\n📺 Episode {episodes_completed} aired! +{ep_fans:,} fans from new viewers.")

    week += 1
    check_end()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("╔══════════════════════════════════════╗")
    print("║      ANIME STUDIO TYCOON  v1.1       ║")
    print("╠══════════════════════════════════════╣")
    print("║ Manage your studio across 10 episodes║")
    print("║ Goal: 50 000+ fans, rep ≥ 0, solvent ║")
    print("╚══════════════════════════════════════╝")
    print()
    while True:
        status()
        print()
        weekly_update()
        print()
