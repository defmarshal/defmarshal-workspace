```python
#!/usr/bin/env python3
"""
Physical Intelligence Fundraising Simulator
Demonstrates venture capital round mechanics and valuation growth.
"""

import sys
from dataclasses import dataclass

@dataclass
class FundingRound:
    """Represents a single funding round."""
    name: str
    raise_amount: float  # in millions USD
    pre_money: float     # pre-money valuation in millions USD
    investor_ownership: float = 0.0  # will be calculated
    post_money: float = 0.0         # will be calculated
    
    def calculate(self):
        """Calculate round economics."""
        self.post_money = self.pre_money + self.raise_amount
        self.investor_ownership = (self.raise_amount / self.post_money) * 100
        return self

@dataclass
class Company:
    """Tracks company ownership and valuation over rounds."""
    name: str
    founders_pct: float = 100.0
    employees_pool: float = 0.0  # option pool percentage
    rounds: list = None
    
    def __post_init__(self):
        if self.rounds is None:
            self.rounds = []
    
    def add_round(self, round: FundingRound):
        """Add a funding round, diluting existing shareholders."""
        # Investors get their percentage
        investor_pct = round.investor_ownership
        
        # Dilute everyone proportionally (including option pool if it exists)
        total_dilution = investor_pct
        founders_new = self.founders_pct * (1 - total_dilution/100)
        employees_new = self.employees_pool * (1 - total_dilution/100) if self.employees_pool > 0 else 0
        
        self.founders_pct = founders_new
        self.employees_pool = employees_new
        self.rounds.append(round)
        
        return {
            'round': round.name,
            'pre_money': round.pre_money,
            'raise': round.raise_amount,
            'post_money': round.post_money,
            'investor_ownership': round.investor_ownership,
            'founders_remaining': round(founders_pct, 2),
            'option_pool_remaining': round(employees_new, 2)
        }
    
    def summary(self):
        """Print current cap table."""
        total_others = 100 - self.founders_pct - self.employees_pool
        return {
            'company': self.name,
            'valuation': self.rounds[-1].post_money if self.rounds else 0,
            'founders': round(self.founders_pct, 2),
            'employees': round(self.employees_pool, 2),
            'investors': round(total_others, 2)
        }

def simulate_physical_intelligence():
    """
    Simulate Physical Intelligence's reported $1B raise on $5.6B pre-money.
    This would effectively double their valuation to ~$11.2B post-money.
    """
    print("=" * 60)
    print("PHYSICAL INTELLIGENCE FUNDRAISING SIMULATOR")
    print("=" * 60)
    print()
    
    # Initial state (prior to new raise)
    print("[PREVIOUS ROUNDS]")
    print("Physical Intelligence has raised multiple rounds:")
    print("- Seed: $20M at $80M pre-money")
    print("- Series A: $80M at $400M pre-money")
    print("- Series B: $300M at $1.8B pre-money")
    print("- Series C: $600M at $5.6B pre-money (4 months ago)")
    print()
    
    # Create company with cap table after Series C
    pi = Company("Physical Intelligence")
    pi.founders_pct = 12.5  # Founders heavily diluted
    pi.employees_pool = 10.0  # 10% option pool
    
    # Add previous rounds (for context)
    rounds = [
        FundingRound("Seed", 20, 80).calculate(),
        FundingRound("Series A", 80, 400).calculate(),
        FundingRound("Series B", 300, 1800).calculate(),
        FundingRound("Series C", 600, 5600).calculate(),
    ]
    
    for r in rounds:
        pi.add_round(r)
    
    print("[CURRENT CAP TABLE (before new round)]")
    s = pi.summary()
    print(f"Company: {s['company']}")
    print(f"Latest Valuation: ${s['valuation']:,.0f}M")
    print(f"Founders Ownership: {s['founders']}%")
    print(f"Employee Option Pool: {s['employees']}%")
    print(f"Investors Total: {s['investors']}%")
    print()
    
    # New proposed round
    print("[PROPOSED SERIES D]")
    print("According to reports: Physical Intelligence in talks to raise $1B")
    print(f"This would double $5.6B valuation → ~$11.2B post-money")
    print()
    
    new_round = FundingRound(
        name="Series D (proposed)",
        raise_amount=1000,
        pre_money=5600
    ).calculate()
    
    result = pi.add_round(new_round)
    
    print("[ROUND ECONOMICS]")
    print(f"Round: {result['round']}")
    print(f"Pre-money: ${result['pre_money']:,.0f}M")
    print(f"Amount Raised: ${result['raise']:,.0f}M")
    print(f"Post-money: ${result['post_money']:,.0f}M")
    print(f"Investor Ownership: {result['investor_ownership']:.2f}%")
    print()
    
    print("[DILUTION IMPACT]")
    print(f"Founders before: {pi.founders_pct + result['investor_ownership']/100:.2f}%")
    print(f"Founders after: {result['founders_remaining']}%")
    print(f"Option pool before: {pi.employees_pool + result['investor_ownership']/100:.2f}%")
    print(f"Option pool after: {result['option_pool_remaining']}%")
    print()
    
    print("[POST-ROUND CAP TABLE]")
    s = pi.summary()
    print(f"Company: {s['company']}")
    print(f"Latest Valuation: ${s['valuation']:,.0f}M (~${s['valuation']/1000:.1f}B)")
    print(f"Founders Ownership: {s['founders']}%")
    print(f"Employee Option Pool: {s['employees']}%")
    print(f"Investors Total: {s['investors']}%")
    print()
    
    print("[CONTEXT]")
    print("• $1B raise would be one of the largest AI/robotics rounds ever")
    print("• Physical Intelligence builds AI-powered robotic systems")
    print("• Investors reportedly include OpenAI, Microsoft, and others")
    print("• Valuation doubles in 4 months → extreme growth trajectory")
    print("• Use of funds: aggressive R&D, manufacturing scale-up, acquisitions")
    print()
    
    print("[WHAT THIS DEMONSTRATES]")
    print("• How venture rounds work: pre-money, post-money, dilution")
    print("• Rapid valuation growth ('up-rounds') in hot sectors")
    print("• Cap table evolution across multiple funding events")
    print("• The math behind 'doubling valuation' headlines")
    print()
    
    print("=" * 60)

if __name__ == "__main__":
    simulate_physical_intelligence()
```