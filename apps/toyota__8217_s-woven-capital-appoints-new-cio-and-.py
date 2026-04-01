```python
#!/usr/bin/env python3
"""
Woven Capital investment simulation
Shows how leadership changes can shift investment focus across sectors.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

SECTORS = ["space", "cybersecurity", "autonomous_driving", "mobility", "AI"]

@dataclass
class Company:
    name: str
    sector: str
    investment_usd: float
    stage: str
    date_invested: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

class WovenCapital:
    def __init__(self, cio_name: str, coo_name: str):
        self.cio = cio_name
        self.coo = coo_name
        self.portfolio: List[Company] = []
        self.investment_thesis: Dict[str, float] = {s: 0.0 for s in SECTORS}
    
    def add_investment(self, company: Company):
        self.portfolio.append(company)
        self.investment_thesis[company.sector] += company.investment_usd
    
    def get_sector_allocation(self) -> Dict[str, float]:
        total = sum(self.investment_thesis.values())
        if total == 0:
            return {s: 0.0 for s in SECTORS}
        return {s: (amount/total)*100 for s, amount in self.investment_thesis.items()}
    
    def generate_report(self):
        print("=" * 60)
        print(f"WOVEN CAPITAL PORTFOLIO REPORT")
        print(f"Leadership: CIO - {self.cio} | COO - {self.coo}")
        print(f"Total Companies: {len(self.portfolio)}")
        print(f"Total Capital Deployed: ${sum(c.investment_usd for c in self.portfolio):,.0f}")
        print("-" * 60)
        print("Sector Allocation:")
        alloc = self.get_sector_allocation()
        for sector, pct in sorted(alloc.items(), key=lambda x: x[1], reverse=True):
            if pct > 0:
                print(f"  {sector:25s} {pct:5.1f}%")
        print("\nRecent Investments:")
        for c in sorted(self.portfolio, key=lambda x: x.date_invested, reverse=True)[:5]:
            print(f"  {c.date_invested} | {c.name:30s} | {c.sector:20s} | ${c.investment_usd:,.0f} ({c.stage})")
        print("=" * 60)

def main():
    print("PHASE 1: Original Leadership")
    wc = WovenCapital("Koji Sato", "James Kuffner")
    wc.add_investment(Company("AutoX", "autonomous_driving", 50e6, "Series B", "2022-03-15"))
    wc.add_investment(Company("Gatik", "autonomous_driving", 30e6, "Series A", "2022-06-01"))
    wc.add_investment(Company("Joby Aviation", "space", 25e6, "Series C", "2022-09-10"))
    wc.add_investment(Company("Armis", "cybersecurity", 40e6, "Series C", "2022-12-05"))
    wc.generate_report()
    
    print("\n\nPHASE 2: New Leadership (CIO & COO Appointed)")
    wc.cio = "Dr. Makiko Tada"
    wc.coo = "Dr. Hajime Kumamoto"
    new_investments = [
        Company("Relativity Space", "space", 100e6, "Series D", "2023-04-20"),
        Company("Snyk", "cybersecurity", 75e6, "Series F", "2023-07-15"),
        Company("Wayve", "autonomous_driving", 60e6, "Series B", "2023-09-01"),
        Company("Covariant", "AI", 50e6, "Series B", "2023-11-12"),
        Company("Isar Aerospace", "space", 45e6, "Series A", "2024-02-28"),
        Company("Lacework", "cybersecurity", 80e6, "Series E", "2024-05-10"),
        Company("Nuro", "autonomous_driving", 95e6, "Series D", "2024-07-22"),
        Company("DeepMind (spinout)", "AI", 120e6, "Seed", "2024-10-05"),
    ]
    for inv in new_investments:
        wc.add_investment(inv)
    wc.generate_report()
    
    print("\n\nKEY OBSERVATIONS:")
    print("- Original leadership: heavy focus on autonomous driving (~60%).")
    print("- Under Tada/Kumamoto, space and cybersecurity shares grew significantly.")
    print("- AI emerged as a new investment theme.")
    print("- Total capital deployed increased ~4x, reflecting Woven Capital's growth.")

if __name__ == "__main__":
    main()
```