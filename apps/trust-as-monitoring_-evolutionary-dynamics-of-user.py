```python
#!/usr/bin/env python3
"""
Trust as Monitoring: Evolutionary Dynamics of User Trust and AI Developer Behaviour
Simulates how user trust functions as a monitoring mechanism in AI development ecosystems.
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Developer:
    """Represents an AI developer or team."""
    name: str
    safety_focus: float  # 0.0 to 1.0; higher = prioritizes safety over speed
    transparency: float  # 0.0 to 1.0; how open about failures/methods
    learning_rate: float  # 0.0 to 1.0; how quickly they adapt from feedback
    
    def respond_to_incident(self, severity: float, user_trust_before: float) -> float:
        """Developer responds to an AI safety incident.
        Returns the trust delta (change in user trust) caused by response."""
        
        # Base response quality depends on safety_focus and learning_rate
        response_quality = (self.safety_focus * 0.6 + self.transparency * 0.4) * self.learning_rate
        
        # If trust was already low, users are more forgiving of transparent responses
        trust_floor_effect = max(0, 0.2 - user_trust_before) * 0.5
        
        # Severity determines maximum possible trust loss/gain
        max_impact = 1.0 - severity
        
        # Net trust change: incident already caused loss; response can recover some
        trust_delta = response_quality * max_impact + trust_floor_effect
        
        # Cap recovery so trust never exceeds 1.0
        return min(trust_delta, 1.0 - user_trust_before)

@dataclass
class User:
    """Represents a user or stakeholder monitoring AI safety."""
    name: str
    trust: float = 0.8  # Initial trust level (0-1)
    vigilance: float  # 0.0 to 1.0; how closely they monitor for incidents
    
    def monitor(self, incident_rate: float, developer_response_quality: float) -> float:
        """Update trust based on observed incident rate and developer response."""
        
        # Vigilance affects how much incidents impact trust
        incident_impact = incident_rate * self.vigilance * 0.5
        
        # Developer response can rebuild trust (but not above baseline if vigilance is high)
        response_gain = developer_response_quality * (1.0 - self.vigilance) * 0.3
        
        # Trust decay/regression to mean (0.7) over time if no incidents
        base_decay = (0.7 - self.trust) * 0.1
        
        new_trust = self.trust - incident_impact + response_gain + base_decay
        return max(0.0, min(1.0, new_trust))

class EvolutionaryDynamicsSimulator:
    """Simulates co-evolution of user trust and developer behavior."""
    
    def __init__(self, num_users: int = 100, num_developers: int = 5, rounds: int = 100):
        self.users = [
            User(f"User{i}", vigilance=random.uniform(0.3, 0.9))
            for i in range(num_users)
        ]
        self.developers = [
            Developer(
                f"Dev{i}",
                safety_focus=random.uniform(0.2, 0.8),
                transparency=random.uniform(0.1, 0.9),
                learning_rate=random.uniform(0.1, 0.9)
            )
            for i in range(num_developers)
        ]
        self.rounds = rounds
        self.history: List[Dict] = []
        
        # Global incident rate (can change based on developer safety focus)
        self.base_incident_rate = 0.05
    
    def calculate_global_incident_rate(self) -> float:
        """Incident rate decreases with average developer safety focus."""
        avg_safety = sum(d.safety_focus for d in self.developers) / len(self.developers)
        return self.base_incident_rate * (1.0 - avg_safety * 0.8)
    
    def calculate_avg_response_quality(self) -> float:
        """Average developer response quality."""
        return sum(d.safety_focus * d.transparency * d.learning_rate 
                  for d in self.developers) / len(self.developers)
    
    def evolve_developers(self, avg_user_trust: float):
        """Developers evolve based on user trust signals."""
        for dev in self.developers:
            if avg_user_trust < 0.4:
                # Low trust -> increase safety focus and transparency
                dev.safety_focus = min(1.0, dev.safety_focus + random.uniform(0, 0.05))
                dev.transparency = min(1.0, dev.transparency + random.uniform(0, 0.03))
                dev.learning_rate = min(1.0, dev.learning_rate + random.uniform(0, 0.02))
            elif avg_user_trust > 0.8:
                # High trust -> slight complacency (reduce vigilance)
                dev.safety_focus = max(0.1, dev.safety_focus - random.uniform(0, 0.01))
                dev.learning_rate = max(0.1, dev.learning_rate - random.uniform(0, 0.01))
    
    def run_round(self, round_num: int):
        """Execute one simulation round."""
        incident_rate = self.calculate_global_incident_rate()
        response_quality = self.calculate_avg_response_quality()
        
        # Users monitor and update trust
        total_trust = 0
        for user in self.users:
            user.trust = user.monitor(incident_rate, response_quality)
            total_trust += user.trust
        
        avg_trust = total_trust / len(self.users)
        
        # Developers respond to incidents (each incident triggers response)
        # Simplified: response quality already computed; trust deltas from monitoring
        
        # Evolutionary pressure: developers adapt based on trust levels
        self.evolve_developers(avg_trust)
        
        # Record history
        self.history.append({
            'round': round_num,
            'avg_trust': avg_trust,
            'incident_rate': incident_rate,
            'response_quality': response_quality,
            'avg_safety_focus': sum(d.safety_focus for d in self.developers) / len(self.developers)
        })
        
        return avg_trust
    
    def simulate(self):
        """Run full simulation and print results."""
        print("=" * 70)
        print("TRUST AS MONITORING: EVOLUTIONARY DYNAMICS")
        print("=" * 70)
        print("\nInitial state:")
        print(f"  Users: {len(self.users)} (vigilance: {self.users[0].vigilance:.2f})")
        print(f"  Developers: {len(self.developers)}")
        print(f"  Avg safety focus: {self.history[0]['avg_safety_focus']:.3f}" if self.history else "")
        
        print("\nSimulating evolutionary dynamics...")
        print("-" * 70)
        print(f"{'Round':<6} {'Avg Trust':<10} {'Incident Rate':<15} {'Response Qual':<15} {'Avg Safety':<10}")
        print("-" * 70)
        
        for round_num in range(1, self.rounds + 1):
            avg_trust = self.run_round(round_num)
            state = self.history[-1]
            
            if round_num % 10 == 0 or round_num == 1:
                print(f"{round_num:<6} {avg_trust:<10.3f} {state['incident_rate']:<15.3f} "
                      f"{state['response_quality']:<15.3f} {state['avg_safety_focus']:<10.3f}")
        
        print("\n" + "=" * 70)
        print("SIMULATION COMPLETE")
        print("=" * 70)
        
        # Final summary
        final = self.history[-1]
        print(f"\nFinal state (round {self.rounds}):")
        print(f"  Average user trust: {final['avg_trust']:.3f}")
        print(f"  Incident rate: {final['incident_rate']:.3f}")
        print(f"  Developer safety focus: {final['avg_safety_focus']:.3f}")
        
        if final['avg_trust'] > 0.7:
            print("\n✅ Positive outcome: Trust remains high, likely stable equilibrium.")
        elif final['avg_trust'] < 0.4:
            print("\n⚠️  Negative outcome: Trust collapse, possible regulatory intervention needed.")
        else:
            print("\n➡️  Mixed outcome: Moderate trust, volatilty persists.")
        
        print("\nInterpretation:")
        print("  This model shows how user trust acts as a monitoring signal that")
        print("  shapes developer behavior evolution. High trust allows complacency;")
        print("  low trust forces safety improvements. The feedback loop determines")
        print("  whether the ecosystem stabilizes in a safe or risky state.")

def main():
    random.seed(42)  # Reproducible runs
    simulator = EvolutionaryDynamicsSimulator(
        num_users=100,
        num_developers=5,
        rounds=100
    )
    simulator.simulate()

if __name__ == "__main__":
    main()
```