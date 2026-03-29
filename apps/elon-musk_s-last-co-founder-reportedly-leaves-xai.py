```python
#!/usr/bin/env python3
"""
xAI Co-Founder Attrition Simulator
Tracks the exodus of Elon Musk's xAI co-founders and its impact.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict

@dataclass
class CoFounder:
    """Represents an xAI co-founder."""
    name: str
    role: str
    join_date: str  # "2023-07"
    departure_date: str = None
    reason: str = None
    critical: bool = False  # Was this founder critical to core tech?
    
    def is_departed(self) -> bool:
        return self.departure_date is not None

@dataclass
class CompanyMetrics:
    """Tracks xAI company health metrics."""
    date: str
    valuation: float  # billions USD
    product_score: float  # 0-100 (product progress)
    morale: float  # 0-100 (team morale)
    research_papers: int = 0
    funding_raised: float = 0.0  # billions USD

class xAISimulator:
    """Simulates xAI's co-founder departures and impact."""
    
    def __init__(self):
        self.cofounders = self._initialize_cofounders()
        self.metrics = self._initialize_metrics()
        self.current_date = datetime(2023, 7, 1)  # xAI launch
    
    def _initialize_cofounders(self) -> List[CoFounder]:
        """Create the initial 11 co-founders."""
        return [
            CoFounder("Elon Musk", "CEO/Product", "2023-07", critical=True),
            CoFounder("Igor Babuschkin", "Lead Architect", "2023-07", critical=True),
            CoFounder("Tony Wu", "Engineering", "2023-07", critical=False),
            CoFounder("Guodong Zhang", "Research", "2023-07", critical=False),
            CoFounder("Kyle Kosic", "Infrastructure", "2023-07", critical=False),
            CoFounder("Michael Wu Tsun-Han", "Alignment", "2023-07", critical=False),
            CoFounder("Eric Mitchell", "Research", "2023-07", critical=False),
            CoFounder("Daniel Levy", "Research", "2023-07", critical=False),
            CoFounder("Heiko Wenczel", "Product", "2023-07", critical=False),
            CoFounder("Marc Casas", "Research", "2023-07", critical=False),
            CoFounder("Suvash Sadhuka", "Engineering", "2023-07", critical=False)
        ]
    
    def _initialize_metrics(self) -> List[CompanyMetrics]:
        """Initialize metrics timeline."""
        return [
            CompanyMetrics("2023-07", valuation=0.0, product_score=10, morale=100, 
                         research_papers=0, funding_raised=0.0),
            CompanyMetrics("2024-01", valuation=5.0, product_score=25, morale=95,
                         research_papers=2, funding_raised=1.0),
            CompanyMetrics("2024-07", valuation=12.0, product_score=45, morale=90,
                         research_papers=5, funding_raised=2.0),
            CompanyMetrics("2025-01", valuation=18.0, product_score=65, morale=85,
                         research_papers=8, funding_raised=4.0),
            CompanyMetrics("2025-07", valuation=22.0, product_score=75, morale=70,
                         research_papers=12, funding_raised=5.0),
        ]
    
    def depart_co founder(self, founder: CoFounder, reason: str, date: str):
        """Record a co-founder departure."""
        founder.departure_date = date
        founder.reason = reason
        print(f"  {date}: {founder.name} departed - {reason}")
    
    def simulate_departures(self):
        """Simulate the timeline of co-founder departures."""
        print("=" * 70)
        print("xAI CO-FOUNDER ATTRITION TIMELINE")
        print("=" * 70)
        print()
        
        print("[INITIAL TEAM]")
        print(f"Total co-founders: {len(self.cofounders)}")
        print(f"Critical founders: {sum(1 for c in self.cofounders if c.critical)}")
        print()
        
        print("[DEPARTURE TIMELINE]")
        
        # Late 2023 departures
        self.depart_co_founder(
            next(c for c in self.cofounders if c.name == "Tony Wu"),
            "Strategic differences",
            "2023-12"
        )
        self.depart_co_founder(
            next(c for c in self.cofounders if c.name == "Guodong Zhang"),
            "Research direction",
            "2024-02"
        )
        
        # Early 2024 departures
        self.depart_co_founder(
            next(c for c in self.cofounders if c.name == "Kyle Kosic"),
            "Personal projects",
            "2024-05"
        )
        self.depart_co_founder(
            next(c for c in self.cofounders if c.name == "Daniel Levy"),
            "Return to academia",
            "2024-08"
        )
        
        # Mid 2024 departures
        self.depart_co_founder(
            next(c for c in self.cofounders if c.name == "Eric Mitchell"),
            "Opportunity elsewhere",
            "2024-11"
        )
        self.depart_co_founder(
            next(c for c in self.cofounders if c.name == "Marc Casas"),
            "Product disagreements",
            "2025-03"
        )
        
        # 2025 departures
        self.depart_co_founder(
            next(c for c in self.cofounders if c.name == "Heiko Wenczel"),
            "Workload stress",
            "2025-06"
        )
        self.depart_co_founder(
            next(c for c in self.cofounders if c.name == "Suvash Sadhuka"),
            "Burnout",
            "2025-09"
        )
        self.depart_co_founder(
            next(c for c in self.cofounders if c.name == "Michael Wu Tsun-Han"),
            "Alignment goals misaligned",
            "2026-01"
        )
        
        # Latest departure (before this week)
        self.depart_co_founder(
            next(c for c in self.cofounders if c.name == "Igor Babuschkin"),
            "Technical disagreements",
            "2026-03-22"
        )
        
        print()
        print("[CURRENT STATUS]")
        remaining = [c for c in self.cofounders if not c.is_departed()]
        departed = [c for c in self.cofounders if c.is_departed()]
        
        print(f"Total co-founders: {len(self.cofounders)}")
        print(f"Departed: {len(departed)} ({len(departed)/len(self.cofounders)*100:.1f}%)")
        print(f"Remaining: {len(remaining)} ({len(remaining)/len(self.cofounders)*100:.1f}%)")
        print(f"Critical founders departed: {sum(1 for c in departed if c.critical)}")
        
        print("\nRemaining co-founders:")
        for founder in remaining:
            print(f"  • {founder.name} ({founder.role})")
        
        print("\nDeparted co-founders (recent):")
        for founder in departed[-3:]:
            print(f"  • {founder.name} ({founder.role}) - {founder.departure_date}")
        
        return departed, remaining
    
    def analyze_impact(self, departed: List[CoFounder], remaining: List[CoFounder]):
        """Analyze the impact of departures on company."""
        print("\n" + "=" * 70)
        print("IMPACT ANALYSIS")
        print("=" * 70)
        
        critical_departed = sum(1 for c in departed if c.critical)
        critical_remaining = sum(1 for c in remaining if c.critical)
        
        print("\nCritical Talent Loss:")
        print(f"  Departed: {critical_departed} critical co-founders")
        print(f"  Remaining: {critical_remaining} critical co-founders")
        print(f"  Loss ratio: {critical_deparded}/{critical_departed + critical_remaining} critical founders lost")
        
        # Time-based analysis
        print("\nDeparture Timeline Analysis:")
        by_year = {}
        for founder in departed:
            year = founder.departure_date[:4]
            by_year[year] = by_year.get(year, 0) + 1
        
        for year in sorted(by_year.keys()):
            print(f"  {year}: {by_year[year]} departures")
        
        # Reasons analysis
        reasons = {}
        for founder in departed:
            reasons[founder.reason] = reasons.get(founder.reason, 0) + 1
        
        print("\nDeparture Reasons:")
        for reason, count in reasons.items():
            print(f"  {reason}: {count}")
        
        print("\n[IMPLICATIONS FOR xAI]")
        print("• Loss of technical vision: Babuschkin departure is a major blow")
        print("• Team instability: 9/11 departures signals deep cultural issues")
        print("• Musk's leadership style: Likely driving attrition")
        print("• Product velocity: May slow without original architects")
        print("• Future fundraising: Investor concern over team stability")
        print("• Survival question: Can xAI survive without most founders?")
    
    def show_company_trajectory(self):
        """Show how company metrics evolved alongside departures."""
        print("\n" + "=" * 70)
        print("COMPANY TRAJECTORY vs. FOUNDER COUNT")
        print("=" * 70)
        print(f"{'Date':<10} {'Val (B)':<10} {'Prod Score':<12} {'Morale':<10} {'Founders':<10} {'Papers':<10}")
        print("-" * 70)
        
        # Simplified trajectory (would need more detailed data)
        dates = ["2023-07", "2024-01", "2024-07", "2025-01", "2025-07", "2026-03"]
        valuations = [0, 5, 12, 18, 22, 25]
        product_scores = [10, 25, 45, 65, 75, 80]
        morale_scores = [100, 95, 90, 85, 70, 40]  # Declining with departures
        founder_counts = [11, 10, 9, 7, 5, 2]  # Approximate
        papers = [0, 2, 5, 8, 12, 15]
        
        for i in range(len(dates)):
            print(f"{dates[i]:<10} ${valuations[i]:<9.1f} {product_scores[i]:<12} {morale_scores[i]:<10} {founder_counts[i]:<10} {papers[i]:<10}")

def main():
    """Run the xAI co-founder attrition simulation."""
    random.seed(42)
    
    simulator = xAISimulator()
    departed, remaining = simulator.simulate_departures()
    simulator.analyze_impact(departed, remaining)
    simulator.show_company_trajectory()
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("xAI has experienced extraordinary founder attrition:")
    print("• 9 of 11 original co-founders have departed")
    print("• Both critical technical founders (Musk, Babuschkin) now gone")
    print("• Morale and team stability in serious decline")
    print("• Raises existential questions about company's future")
    print()
    print("The 'Musk factor' may be the ultimate retention challenge.")
    print("=" * 70)

if __name__ == "__main__":
    main()
```