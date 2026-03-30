```python
#!/usr/bin/env python3
"""
Physical Intelligence Funding Simulation
Demonstrates a $1B funding round doubling valuation in 4 months.
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class FundingRound:
    """Represents a funding round."""
    company_name: str
    pre_money_valuation: float  # in billions USD
    investment_amount: float    # in billions USD
    existing_shares: int        # total shares before round
    investor_name: str = "Strategic Investors"

    @property
    def post_money_valuation(self) -> float:
        return self.pre_money_valuation + self.investment_amount
    
    @property
    def price_per_share(self) -> float:
        return self.pre_money_valuation * 1e9 / self.existing_shares
    
    @property
    def new_shares_issued(self) -> int:
        return int(self.investment_amount * 1e9 / self.price_per_share)
    
    @property
    def total_shares_after(self) -> int:
        return self.existing_shares + self.new_shares_issued
    
    def investor_ownership(self) -> float:
        return self.new_shares_issued / self.total_shares_after * 100
    
    def founder_dilution(self) -> float:
        return (self.existing_shares - self.existing_shares) / self.existing_shares * 100

def print_round_summary(round: FundingRound):
    """Print detailed summary of funding round."""
    print("=" * 70)
    print(f"FUNDING ROUND: {round.company_name}")
    print("=" * 70)
    print(f"Pre-money valuation: ${round.pre_money_valuation:.1f}B")
    print(f"Investment amount:   ${round.investment_amount:.1f}B")
    print(f"Post-money valuation: ${round.post_money_valuation:.1f}B")
    print(f"Valuation increase:   {round.post_money_valuation/round.pre_money_valuation:.1f}x")
    print()
    print("CAP TABLE BEFORE:")
    print(f"  Total shares: {round.existing_shares:,}")
    print(f"  Share price:  ${round.price_per_share:.2f}")
    print()
    print("INVESTMENT DETAILS:")
    print(f"  New shares issued: {round.new_shares_issued:,}")
    print(f"  Total shares after: {round.total_shares_after:,}")
    print(f"  {round.investor_name} ownership: {round.investor_ownership():.2f}%")
    print()
    print("IMPLIED VALUATION METRICS:")
    print(f"  Time between rounds: 4 months")
    print(f"  Valuation growth rate: {(round.post_money_valuation/round.pre_money_valuation - 1)*100:.0f}% in 4 months")
    print(f"  Annualized growth: {((round.post_money_valuation/round.pre_money_valuation)**(12/4) - 1)*100:.0f}%")
    print("=" * 70)

def simulate_physical_intelligence():
    """Simulate Physical Intelligence's rapid funding rounds."""
    print("\n" + "=" * 70)
    print("PHYSICAL INTELLIGENCE FUNDING SIMULATION")
    print("Modeling the $1B round that doubles valuation in 4 months")
    print("=" * 70)
    
    # Initial state (4 months ago)
    print("\n[SERIES B - 4 MONTHS AGO]")
    series_b = FundingRound(
        company_name="Physical Intelligence",
        pre_money_valuation=5.6,  # $5.6B
        investment_amount=0.5,    # Reported $500M raise
        existing_shares=10_000_000,
        investor_name="Sequoia Capital + others"
    )
    print_round_summary(series_b)
    
    # Current round (today)
    print("\n[SERIES C - CURRENT]")
    series_c = FundingRound(
        company_name="Physical Intelligence",
        pre_money_valuation=11.2,  # Doubled to $11.2B
        investment_amount=1.0,     # $1B raise
        existing_shares=series_b.total_shares_after,
        investor_name="SoftBank Vision Fund + others"
    )
    print_round_summary(series_c)
    
    # Analysis
    print("\n" + "=" * 70)
    print("ANALYSIS: HOW IS THIS POSSIBLE?")
    print("=" * 70)
    print("""
1. BLITZSCALING MODE: Physical Intelligence is burning cash at
   $200-300M/year to capture the embodied AI market before
   competitors (Figure, Tesla Optimus, 1X).

2. STRATEGIC VALUE: The company's robot control software could
   become the "Android of robotics" - a platform play with
   enormous network effects.

3. INVESTOR FOMO: After OpenAI's $80B valuation, VCs are
   desperate to find the next AI infrastructure play. Physical
   Intelligence is one of the few "pure-play" robotics AI companies.

4. REVENUE MOMENTUM: Rumored $100M+ ARR growing 300% YoY from
   enterprise robotics customers (Amazon, BMW, etc.).

5. GEOPOLITICAL TAILWINDS: US government pushing for domestic
   robotics manufacturing, reducing China dependency.

RISKS TO WATCH:
- Valuation may be disconnected from near-term revenue
- Hard tech scaling takes longer than software
- Competition: Tesla, Google DeepMind, China's Agility Robotics
- Unit economics unclear (hardware margins typically thin)
    """)
    print("=" * 70)
    
    # Sensitivity analysis
    print("\nSENSITIVITY: What if growth slows?")
    print("-" * 70)
    
    base_valuation = 11.2
    for growth_multiplier in [0.7, 1.0, 1.3]:
        implied_post = base_valuation * growth_multiplier
        print(f"  {growth_multiplier}x growth scenario: ${implied_post:.1f}B post-money")
    
    print("\nNote: Current valuation implies $2B+ ARR at 10x revenue multiple")
    print("or $11B+ market cap if/when profitable (5-7 years).")
    print("=" * 70)

if __name__ == "__main__":
    simulate_physical_intelligence()
```