```python
#!/usr/bin/env python3
"""
Whoop Growth Challenges Simulator
Demonstrates the tension between scaling a fitness wearable and maintaining quality/regulatory compliance.
"""

from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class WhoopMetrics:
    """Key metrics for Whoop's business."""
    year: int
    users: int
    quality_score: float  # 0-10, elite athlete satisfaction
    fda_compliance: float  # 0-10, regulatory standing
    market_share: float  # vs Oura
    revenue_millions: float

class WhoopGrowthSimulator:
    """Simulates Whoop's growth challenges."""
    
    def __init__(self):
        self.metrics = []
        self.initialize_starting_position()
    
    def initialize_starting_position(self):
        """Whoop's position in 2024 (Year 0)."""
        self.metrics.append(WhoopMetrics(
            year=2024,
            users=500_000,
            quality_score=9.2,  # Elite athletes love it
            fda_compliance=8.5,  # Good but not perfect
            market_share=0.35,  # vs Oura's ~0.40
            revenue_millions=250.0
        ))
    
    def simulate_year(self, strategy: str) -> WhoopMetrics:
        """
        Simulate one year of growth.
        Strategies: 'quality_first', 'growth_aggressive', 'balanced'
        """
        prev = self.metrics[-1]
        
        # Growth rates depend on strategy
        if strategy == 'quality_first':
            user_growth = random.uniform(0.15, 0.25)  # Slower but steady
            quality_change = random.uniform(-0.1, 0.3)  # Maintain/improve
            fda_effort = random.uniform(0.1, 0.3)  # Heavy compliance investment
        elif strategy == 'growth_aggressive':
            user_growth = random.uniform(0.40, 0.70)  # Rapid scaling
            quality_change = random.uniform(-0.5, 0.1)  # Quality suffers
            fda_effort = random.uniform(-0.1, 0.2)  # Compliance neglected
        else:  # balanced
            user_growth = random.uniform(0.25, 0.40)
            quality_change = random.uniform(-0.2, 0.2)
            fda_effort = random.uniform(0.0, 0.3)
        
        # Market share dynamics (Oura as benchmark)
        oura_growth = random.uniform(0.10, 0.25)
        market_share_change = (user_growth - oura_growth) * 0.5
        
        # Revenue scaling (simplified)
        revenue_multiplier = 1.0 + user_growth * 0.8  # Some economies of scale
        
        new_users = int(prev.users * (1 + user_growth))
        new_quality = max(1.0, min(10.0, prev.quality_score + quality_change))
        new_fda = max(1.0, min(10.0, prev.fda_compliance + fda_effort))
        new_market_share = max(0.0, min(0.6, prev.market_share + market_share_change))
        new_revenue = prev.revenue_millions * revenue_multiplier
        
        return WhoopMetrics(
            year=prev.year + 1,
            users=new_users,
            quality_score=new_quality,
            fda_compliance=new_fda,
            market_share=new_market_share,
            revenue_millions=new_revenue
        )
    
    def run_simulation(self, strategy: str, years: int = 5):
        """Run multi-year simulation."""
        print(f"\n{'='*70}")
        print(f"WHOOP GROWTH SIMULATION: {strategy.upper()} STRATEGY")
        print(f"{'='*70}\n")
        
        print(f"{'Year':<6} {'Users':>12} {'Quality':>8} {'FDA':>6} {'Mkt Share':>10} {'Revenue $M':>12}")
        print("-"*70)
        
        for _ in range(years):
            next_year = self.simulate_year(strategy)
            self.metrics.append(next_year)
            print(f"{next_year.year:<6} {next_year.users:>12,} {next_year.quality_score:>8.1f} "
                  f"{next_year.fda_compliance:>6.1f} {next_year.market_share:>10.2%} "
                  f"{next_year.revenue_millions:>12.1f}")
    
    def analyze_tradeoffs(self):
        """Show trade-offs between strategies."""
        print(f"\n{'='*70}")
        print("COMPARATIVE ANALYSIS (5-YEAR OUTCOME)")
        print(f"{'='*70}\n")
        
        # Extract final metrics for each strategy
        strategies = {}
        for strategy in ['quality_first', 'balanced', 'growth_aggressive']:
            # Re-run simulation for each strategy
            self.metrics = [self.metrics[0]]  # Reset
            self.run_simulation(strategy, years=5)
            final = self.metrics[-1]
            strategies[strategy] = final
        
        print(f"{'Strategy':<18} {'Ending Users':>12} {'Quality':>8} {'FDA':>6} {'Revenue $M':>12}")
        print("-"*70)
        for name, m in strategies.items():
            print(f"{name:<18} {m.users:>12,} {m.quality_score:>8.1f} "
                  f"{m.fda_compliance:>6.1f} {m.revenue_millions:>12.1f}")
        
        print(f"\n{'KEY INSIGHTS':<70}")
        print("-"*70)
        print("1. Quality First: Maintains elite athlete reputation but loses market share")
        print("2. Aggressive Growth: gains users quickly but quality and compliance suffer")
        print("3. Balanced: Attempts to manage trade-offs but may excel at nothing")
        print("\nCHALLENGES WHOOP FACES:")
        print("• Elite athletes demand precision; scaling dilutes that precision")
        print("• FDA medical device classification limits marketing claims")
        print("• Oura has first-mover advantage in the ring form factor")
        print("• Hardware margins pressure as volume scales")
        print("• Consumer expectations vs. medical-grade claims is a tightrope")
        print("="*70)

def main():
    """Run the Whoop growth simulation."""
    random.seed(42)  # Reproducible scenarios
    
    print("\n" + "="*70)
    print("WHOOP: SCABILING THE ELITE FITNESS TRACKER")
    print("Simulating the challenges of growing a health wearable brand")
    print("="*70)
    
    print("\n[INITIAL POSITION - 2024]")
    print("Users: 500,000 (mostly elite athletes & enthusiasts)")
    print("Quality Score: 9.2/10 (beloved by pros)")
    print("FDA Compliance: 8.5/10 (some medical claims under scrutiny)")
    print("Market Share: 35% vs Oura (40%) and others")
    print("Revenue: $250M")
    
    simulator = WhoopGrowthSimulator()
    
    # Run three strategy simulations
    simulator.run_simulation('quality_first', years=5)
    simulator.run_simulation('balanced', years=5)
    simulator.run_simulation('growth_aggressive', years=5)
    
    simulator.analyze_tradeoffs()
    
    print("\n[CONCLUSION]")
    print("Whoop's challenge: scaling from elite cult brand to mass market")
    print("while maintaining the precision that made it famous. The FDA,")
    print("Oura's ring form factor, and hardware margins make this path")
    print("treacherous. Can Ahmed thread the needle? Simulation suggests")
    print("balance is possible but requires constant trade-off management.")
    print("="*70)

if __name__ == "__main__":
    main()
```