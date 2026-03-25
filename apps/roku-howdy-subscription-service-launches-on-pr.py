#!/usr/bin/env python3
"""
Auto-generated app for: Roku's $3 Howdy subscription service launches on Prime Video
Context: TechCrunch RSS feed - March 24, 2026
This script demonstrates a simple subscription management simulation for the Howdy service.
"""

import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict

SERVICE_NAME = "Roku Howdy"
SUBSCRIPTION_PRICE = 3.00

@dataclass
class Subscription:
    user_id: str
    plan: str
    start_date: str
    active: bool = True

    def days_remaining(self) -> int:
        start = datetime.fromisoformat(self.start_date)
        # 30-day billing cycle
        cycle_end = start + timedelta(days=30)
        remaining = (cycle_end - datetime.now()).days
        return max(0, remaining)

class HowdyManager:
    def __init__(self):
        self.subscriptions: Dict[str, Subscription] = {}
        self.revenue = 0.0

    def new_subscription(self, user_id: str) -> Subscription:
        plan = "monthly"
        start = datetime.now().isoformat()
        sub = Subscription(user_id, plan, start)
        self.subscriptions[user_id] = sub
        self.revenue += SUBSCRIPTION_PRICE
        print(f"🎉 New subscription: {user_id} → {SERVICE_NAME} (${SUBSCRIPTION_PRICE}/mo)")
        return sub

    def get_user_status(self, user_id: str) -> Dict:
        sub = self.subscriptions.get(user_id)
        if not sub:
            return {"user_id": user_id, "active": False, "message": "No subscription"}
        return {
            "user_id": user_id,
            "active": sub.active,
            "days_remaining": sub.days_remaining(),
            "plan": sub.plan,
            "start_date": sub.start_date
        }

    def simulate_billing_cycle(self):
        print(f"\n💰 Monthly Revenue: ${self.revenue:.2f}")
        active_count = sum(1 for s in self.subscriptions.values() if s.active)
        print(f"Active subscribers: {active_count}")
        print(" Billing cycle simulation complete.")

def main():
    print(f"=== {SERVICE_NAME} Subscription Manager ===")
    manager = HowdyManager()

    # Simulate new signups
    sample_users = [f"user_{i:03d}" for i in range(1, 6)]
    for uid in sample_users:
        manager.new_subscription(uid)

    # Display status
    print("\n📊 Subscriber Status:")
    for uid in sample_users:
        status = manager.get_user_status(uid)
        print(f"  {uid}: active={status['active']}, renews in {status['days_remaining']} days")

    manager.simulate_billing_cycle()

    # Save state example
    state = {
        "service": SERVICE_NAME,
        "generated_at": datetime.now().isoformat(),
        "subscriptions": [asdict(s) for s in manager.subscriptions.values()],
        "total_revenue": manager.revenue
    }
    with open("howdy_state.json", "w") as f:
        json.dump(state, f, indent=2)
    print("\n💾 State saved to howdy_state.json")

if __name__ == "__main__":
    main()
