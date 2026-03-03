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
            # Non-interactive safe: auto-choose based on affordability
            if money >= 5000:
                money -= 5000
                print("Paid overtime (auto). Staff stay.")
            else:
                print("Can't afford overtime. Staff leave.")
                staff -= 2
    # Propose choices
    print("\nChoices:")
    print("1) Hire (+1 staff, -¥5000)")
    print("2) Fire (+¥2000, -1 staff)")
    print("3) Train (staff +1, -¥3000)")
    print("4) Rush (faster production but risk quality)")
    print("5) Quality focus (reputation +5, costs ¥2000)")
    print("6) Next week")
    # Non-interactive: auto-choose based on simple heuristics
    try:
        choice = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        # Auto-mode: choose based on game state
        if money < 5000 and staff > 3:
            choice = "2"  # Fire if low on money and too many staff
        elif money >= 5000 and staff < 5:
            choice = "1"  # Hire if can afford and staff low
        elif money >= 3000 and staff < 5:
            choice = "3"  # Train if can afford
        elif reputation < 60 and money >= 2000:
            choice = "5"  # Quality focus if rep low
        else:
            choice = "6"  # Advance week
        print(f"Auto-choosing: {choice}")
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
