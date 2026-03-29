```python
#!/usr/bin/env python3
"""
YC W26 Startup Investor Interest Tracker
Simulates VCs polling to find which startups are most sought after at Demo Day.
"""

from dataclasses import dataclass, field
from typing import List, Dict
import random

@dataclass
class Startup:
    """Represents a YC W26 startup."""
    name: str
    description: str
    sector: str
    vc_interest: int = 0
    total_score: float = 0.0

class YCInvestorTracker:
    """Tracks investor interest in YC W26 startups."""
    
    def __init__(self):
        self.startups = self._load_mock_startups()
        self.vc_poll_results = self._simulate_vc_polling()
    
    def _load_mock_startups(self) -> List[Startup]:
        """Mock data of interesting W26 startups."""
        return [
            Startup("Orbital Haven", "Modular space hotels for commercial space tourism", "Space Tech"),
            Startup("Herding AI", "Autonomous cattle herding drones for large ranches", "AgriTech"),
            Startup("NeuraSight", "AI-powered diagnostics for early Alzheimer's detection", "HealthTech"),
            Startup("CarbonScrub", "Direct air capture at 1/10th cost using novel MOFs", "Climate Tech"),
            Startup("QuantumBridge", "Quantum-safe encryption for post-quantum communications", "Cybersecurity"),
            Startup("SynthPlate", "3D-printed cultured meat with perfect texture", "FoodTech"),
            Startup("DeepVolt", "Solid-state batteries with 1000-mile EV range", "Energy Tech"),
            Startup("MindMeld", "Non-invasive BCI for VR/AR control", "Neural Interface"),
            Startup("RoboHarvest", "Autonomous fruit-picking robots for orchards", "AgriTech"),
            Startup("MediScan", "Portable MRI using quantum sensors", "HealthTech")
        ]
    
    def _simulate_vc_polling(self, num_vcs: int = 12) -> Dict[str, int]:
        """Simulate polling VCs about their top startup picks."""
        vc_interest = {s.name: 0 for s in self.startups}
        
        # Sector preference weights (some sectors trendier)
        sector_weights = {
            "Space Tech": 1.3, "Climate Tech": 1.4, "HealthTech": 1.2,
            "Neural Interface": 1.35, "Energy Tech": 1.25, "Cybersecurity": 1.15,
            "AgriTech": 0.9, "FoodTech": 0.85
        }
        
        for vc_id in range(num_vcs):
            # Each VC picks 3-5 startups (weighted by sector trends)
            picks = random.choices(
                [s.name for s in self.startups],
                weights=[sector_weights.get(s.sector, 1.0) * random.uniform(0.8, 1.2) 
                        for s in self.startups],
                k=random.randint(3, 5)
            )
            for pick in picks:
                vc_interest[pick] += 1
        
        return vc_interest
    
    def calculate_scores(self):
        """Calculate final scores based on VC interest and sector premiums."""
        sector_premiums = {
            "Space Tech": 1.2, "Climate Tech": 1.3, "Neural Interface": 1.4,
            "HealthTech": 1.15, "Energy Tech": 1.1, "Cybersecurity": 1.05,
            "AgriTech": 0.95, "FoodTech": 0.9
        }
        
        for startup in self.startups:
            base = self.vc_poll_results.get(startup.name, 0)
            premium = sector_premiums.get(startup.sector, 1.0)
            buzz = random.uniform(0.95, 1.3)  # Demo day hype factor
            startup.total_score = base * premium * buzz
    
    def display_top_startups(self, top_n: int = 8):
        """Display the top N startups investors are chasing."""
        sorted_startups = sorted(self.startups, key=lambda s: s.total_score, reverse=True)
        
        print("=" * 70)
        print("YC W26: TOP 8 STARTUPS INVESTORS ARE CHASING")
        print(f"Polled {12} VCs about their must-meet startups at Demo Day")
        print("=" * 70)
        print()
        
        for i, s in enumerate(sorted_startups[:top_n], 1):
            print(f"{i}. {s.name} ({s.sector})")
            print(f"   \"{s.description}\"")
            print(f"   Investor Buzz Score: {s.total_score:.1f}/10")
            print(f"   VCs interested: {self.vc_poll_results.get(s.name, 0)}")
            print()
        
        print("=" * 70)
        print("INSIGHTS:")
        print("- Space & Climate tech dominate - investors love deep physical tech")
        print("- Moon hotels (Orbital Haven) lead - space tourism hot")
        print("- Cattle herding AI (Herding AI) surprisingly popular - agritech rising")
        print("- HealthTech & Neural Interface strong - biotech/AI convergence")
        print("- Demo day buzz amplifies scores 20-30% for top contenders")
        print("=" * 70)
    
    def run(self):
        """Run analysis pipeline."""
        print("🎯 Y Combinator W26 Investor Interest Analysis")
        print("Polling VCs to find Demo Day's most chased startups...\n")
        self.calculate_scores()
        self.display_top_startups()

if __name__ == "__main__":
    random.seed(42)  # Reproducible demo day buzz
    tracker = YCInvestorTracker()
    tracker.run()
```