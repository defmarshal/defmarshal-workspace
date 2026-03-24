```python
#!/usr/bin/env python3
"""
Demo: Transition from Human Interfaces to Agent Interfaces.
Shows a travel planner reimagined for AI-native consumption.
"""

import json
from datetime import datetime

class HumanTravelPlanner:
    """Traditional human-oriented interface: step-by-step prompts."""
    def run(self):
        print("=== Human Travel Planner ===")
        city = input("Enter destination city: ")
        days = int(input("Number of days (1-30): "))
        budget = float(input("Total budget (USD): "))
        interests = input("Interests (comma-separated): ").split(',')
        plan = self._generate(city, days, budget, interests)
        print("\nYour itinerary:")
        for day in plan['itinerary']:
            print(f" - {day}")
        return plan

    def _generate(self, city, days, budget, interests):
        daily_budget = budget / days if days else 0
        base = [f"Day {i+1}: Explore {city}" for i in range(days)]
        if interests:
            for i, interest in enumerate(interests[:days]):
                base[i] += f" | Focus: {interest.strip()}"
        return {
            'city': city,
            'days': days,
            'daily_budget': round(daily_budget, 2),
            'interests': [i.strip() for i in interests],
            'itinerary': base
        }

class AgentTravelPlanner:
    """Agent-oriented interface: structured I/O with machine-readable schema."""
    def __init__(self):
        self.schema = {
            "name": "TravelPlanner",
            "description": "Generates a travel itinerary based on user preferences",
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Destination city name"},
                    "days": {"type": "integer", "minimum": 1, "maximum": 30},
                    "budget": {"type": "number", "minimum": 0, "description": "Total budget in USD"},
                    "interests": {"type": "array", "items": {"type": "string"}, "description": "List of interests/activities"}
                },
                "required": ["city", "days", "budget"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "itinerary": {"type": "array", "items": {"type": "string"}},
                    "daily_budget": {"type": "number"},
                    "metadata": {"type": "object"}
                }
            }
        }

    def plan(self, request):
        """Accept structured dict, return structured dict."""
        city = request['city']
        days = request['days']
        budget = request.get('budget', 0)
        interests = request.get('interests', [])
        daily_budget = budget / days if days else 0
        base = [f"Day {i+1}: Highlights of {city}" for i in range(days)]
        if interests:
            for i, interest in enumerate(interests[:days]):
                base[i] += f" | Activity: {interest.strip()}"
        return {
            "itinerary": base,
            "daily_budget": round(daily_budget, 2),
            "metadata": {
                "source": "AgentTravelPlanner",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "total_days": days
            }
        }

def main():
    print("="*60)
    print("From Human Interfaces to Agent Interfaces")
    print("="*60)

    print("\n1. Human-facing (interactive CLI)")
    print("-"*40)
    human = HumanTravelPlanner()
    # Simulate non-interactive for demo: use defaults if running unattended
    try:
        human.run()
    except EOFError:
        # Fallback for non-interactive environments
        demo_input = {'city': 'Paris', 'days': 3, 'budget': 1500, 'interests': 'art, cuisine, history'.split(',')}
        print("(simulated input)")
        result = human._generate(**demo_input)
        print("\nYour itinerary:")
        for day in result['itinerary']:
            print(f" - {day}")

    print("\n" + "="*60)
    print("\n2. Agent-facing (structured API with schema)")
    print("-"*40)
    agent = AgentTravelPlanner()
    print("Interface schema (exposed for agent discovery):")
    print(json.dumps(agent.schema, indent=2)[:500] + "...\n")

    agent_request = {
        "city": "Tokyo",
        "days": 5,
        "budget": 2500,
        "interests": ["temples", "sushi", "technology", "parks", "nightlife"]
    }
    print("Agent request payload:")
    print(json.dumps(agent_request, indent=2))
    response = agent.plan(agent_request)
    print("\nAgent response payload:")
    print(json.dumps(response, indent=2))

    print("\n" + "="*60)
    print("Key differences:")
    print("- Human: interactive prompts, free-form input, immediate printing.")
    print("- Agent: machine-readable schema, structured dict I/O, embeddable.")
    print("="*60)

if __name__ == "__main__":
    main()
```