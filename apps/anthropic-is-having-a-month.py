#!/usr/bin/env python3
import random
import datetime
import os

# Anthropic incident simulation: a human keeps borking things
borks = [
    "Pushed to production without testing",
    "Deleted the main database backup",
    "Committed AWS secret key to GitHub",
    "Misconfigured firewall exposing internal services",
    "Introduced memory leak in core service",
    "Disabled monitoring during maintenance and forgot to re-enable",
    "Ran rm -rf on wrong server",
    "Changed clock synchronization causing cascade failures",
    "Deployed untested AI model weights causing toxic outputs",
    "Broke the CI/CD pipeline by merging untested PR",
    "Lost encryption keys for customer data",
    "Overloaded database by running unindexed query in production",
    "Misrouted traffic to test environment",
    "Forced restart of all nodes causing downtime",
    "Accidentally scaled down critical service to zero",
    "Introduced race condition causing data corruption",
    "Misconfigured autoscaling causing infinite loop",
    "Deployed code with infinite loop to all instances",
    "Forgot to renew SSL certificates",
    "Broke OAuth integration by changing client secret",
]

def simulate_month(year=2026, month=4, incident_prob=0.25):
    """Simulate a month of incidents at Anthropic."""
    start_date = datetime.date(year, month, 1)
    # Determine days in month
    if month == 12:
        next_month = datetime.date(year+1, 1, 1)
    else:
        next_month = datetime.date(year, month+1, 1)
    days_in_month = (next_month - start_date).days
    
    log_lines = []
    total_incidents = 0
    
    print(f"=== Anthropic Incident Simulator ===")
    print(f"Simulating {start_date.strftime('%B %Y')}...")
    print("-" * 50)
    
    for day in range(1, days_in_month+1):
        current_date = start_date.replace(day=day)
        if random.random() < incident_prob:
            bork = random.choice(borks)
            log_entry = f"{current_date.isoformat()} - INCIDENT: {bork}"
            log_lines.append(log_entry)
            print(log_entry)
            total_incidents += 1
    
    print("-" * 50)
    print(f"Total incidents: {total_incidents} ({total_incidents/days_in_month*100:.1f}% of days)")
    
    # Weekly breakdown
    weeks = {}
    for line in log_lines:
        date_str = line.split(" - ")[0]
        date_obj = datetime.date.fromisoformat(date_str)
        week_num = date_obj.isocalendar()[1]
        weeks[week_num] = weeks.get(week_num, 0) + 1
    
    print("\nWeekly breakdown:")
    for week, count in sorted(weeks.items()):
        marker = " <-- multiple incidents!" if count > 1 else ""
        print(f"  Week {week}: {count} incident(s){marker}")
    
    # Determine if it's a "brutal month"
    brutal = any(count >= 2 for count in weeks.values())
    if brutal:
        print("\n🔥 Anthropic is having a brutal month! 🔥")
    else:
        print("\n✅ Month went relatively smoothly.")
    
    # Write to log file
    logfile = "anthropic_incidents.log"
    with open(logfile, "a") as f:
        f.write(f"=== Log for {start_date.strftime('%B %Y')} ===\n")
        for line in log_lines:
            f.write(line + "\n")
        f.write(f"Total: {total_incidents}\n")
        f.write(f"Weekly: {weeks}\n\n")
    print(f"\nLog saved to {logfile}")

if __name__ == "__main__":
    simulate_month(2026, 4)