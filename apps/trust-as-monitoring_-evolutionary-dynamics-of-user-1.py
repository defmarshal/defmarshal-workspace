```python
#!/usr/bin/env python3
"""
Trust as Monitoring: Evolutionary dynamics simulation
Demonstrates how user trust shapes AI developer behavior over time.
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Developer:
    """Represents an AI developer or team."""
    name: str
    safety_focus: float  # 0.0 to 1.0; higher = prioritizes safety over capability
    capability: float    # 0.0 to 1.0; inherent technical capability
    trust: float = 0.5   # Current user trust (0-1)
    users: int = 10      # Number of users (fitness)
    
    def produce_outcome(self) -> str:
        """Generate an outcome when a user interacts with this developer's AI."""
        # Probability of failure (unsafe outcome) depends on safety focus and capability
        # High safety focus reduces failure probability; high capability increases success probability
        failure_prob = 0.3 * (1 - self.safety_focus) + 0.1 * (1 - self.capability)
        if random.random() < failure_prob:
            return "failure"  # Unsafe or poor outcome
        else:
            return "success"  # Safe and effective outcome
    
    def update_trust(self, outcome: str, learning_rate: float = 0.1):
        """Update trust based on outcome (user feedback)."""
        if outcome == "success":
            self.trust = min(1.0, self.trust + learning_rate)
        else:
            self.trust = max(0.0, self.trust - learning_rate * 2)  # Failures hurt trust more
    
    def reproduce(self) -> 'Developer':
        """Create offspring with small mutations."""
        mutation_strength = 0.1
        new_safety = max(0.0, min(1.0, self.safety_focus + random.uniform(-mutation_strength, mutation_strength)))
        new_capability = max(0.0, min(1.0, self.capability + random.uniform(-mutation_strength, mutation_strength)))
        return Developer(
            name=f"Gen_{self.name}_{random.randint(1,1000)}",
            safety_focus=new_safety,
            capability=new_capability,
            trust=self.trust * 0.9,  # Offspring start with slightly lower trust
            users=self.users // 2 if self.users > 1 else 1
        )

class Ecosystem:
    """Simulates the evolutionary dynamics of developers and user trust."""
    
    def __init__(self, num_developers: int = 20):
        self.developers: List[Developer] = []
        # Initialize with random developers: some safe, some risky
        for i in range(num_developers):
            # Randomly assign type: safe (high safety, medium capability) or risky (low safety, high capability)
            if random.random() < 0.5:
                safety = random.uniform(0.7, 0.9)
                capability = random.uniform(0.5, 0.7)
            else:
                safety = random.uniform(0.1, 0.3)
                capability = random.uniform(0.7, 0.9)
            self.developers.append(Developer(
                name=f"Dev_{i}",
                safety_focus=safety,
                capability=capability,
                trust=random.uniform(0.3, 0.7),
                users=random.randint(5, 20)
            ))
        self.history = []
    
    def step(self):
        """Run one evolutionary timestep."""
        # 1. Users interact with developers proportional to their current user count
        total_interactions = sum(d.users for d in self.developers)
        for dev in self.developers:
            # Number of interactions this developer gets proportional to its user base
            interactions = max(1, int(dev.users / total_interactions * 100))
            for _ in range(interactions):
                outcome = dev.produce_outcome()
                dev.update_trust(outcome)
        
        # 2. Update user counts based on trust (trust acts as fitness/market share)
        # More trust → more users, less trust → users leave
        total_trust = sum(d.trust for d in self.developers)
        if total_trust == 0:
            # If all trust zero, redistribute equally
            for dev in self.developers:
                dev.users = max(1, dev.users // 2)
        else:
            new_users = []
            for dev in self.developers:
                # Market share proportional to trust
                share = dev.trust / total_trust
                target_users = int(share * sum(d.users for d in self.developers))
                # Some smoothing: don't change too drastically
                dev.users = int(0.7 * dev.users + 0.3 * target_users)
                if dev.users <= 0:
                    dev.users = 1
            
        # 3. Reproduction: top half of developers (by trust) reproduce
        self.developers.sort(key=lambda d: d.trust, reverse=True)
        survivors = self.developers[:len(self.developers)//2]
        newborns = []
        for parent in survivors:
            if random.random() < 0.6:  # 60% chance to reproduce
                newborns.append(parent.reproduce())
        self.developers = survivors + newborns
        
        # Record statistics
        avg_safety = sum(d.safety_focus for d in self.developers) / len(self.developers)
        avg_capability = sum(d.capability for d in self.developers) / len(self.developers)
        avg_trust = sum(d.trust for d in self.developers) / len(self.developers)
        self.history.append({
            'generation': len(self.history),
            'developers': len(self.developers),
            'avg_safety': avg_safety,
            'avg_capability': avg_capability,
            'avg_trust': avg_trust
        })
    
    def run(self, generations: int = 100):
        """Run simulation for given generations."""
        for _ in range(generations):
            self.step()
    
    def plot_history(self):
        """Print a simple text-based plot of the evolutionary trajectory."""
        print("\nEvolutionary Dynamics (Trust as Monitoring)")
        print("=" * 50)
        print(f"{'Gen':<6} {'Devs':<6} {'Safety':<8} {'Capab':<8} {'Trust':<8}")
        print("-" * 50)
        for entry in self.history[::10]:  # Every 10th generation
            print(f"{entry['generation']:<6} {entry['developers']:<6} "
                  f"{entry['avg_safety']:<8.3f} {entry['avg_capability']:<8.3f} "
                  f"{entry['avg_trust']:<8.3f}")
        print("\nNote: Trust acts as fitness. Safe developers gain users; risky ones lose them.")

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    eco = Ecosystem(num_developers=30)
    eco.run(generations=100)
    eco.plot_history()
```