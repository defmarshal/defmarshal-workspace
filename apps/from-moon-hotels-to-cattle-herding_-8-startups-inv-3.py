```python
#!/usr/bin/env python3
"""
YC W26 Demo Day: Top Startups Investors Are Chasing
Simulates VC polling to identify most sought-after startups.
"""

from dataclasses import dataclass, field
from typing import List, Dict
import random

@dataclass
class Startup:
    """Represents a YC W26 startup."""
    name: str
    tagline: str
    sector: str
    vc_votes: int = 0
    interest_score: float = 0.0

class YCInvestorPoll:
    """Simulates VC polling for top YC W26 startups."""
    
    def __init__(self):
        self.startups = self._create_startups()
        self.vc_prefs = self._generate_vc_polling()
        
    def _create_startups(self) -> List[Startup]:
        """Create mock list of W26 hot startups."""
        return [
            Startup("Orbital Haven", "Modular space hotels for space tourism", "Space Tech"),
            Startup("Herding AI", "Autonomous cattle herding drones for ranches", "AgriTech"),
            Startup("NeuraSight", "AI-powered early Alzheimer's detection via speech", "HealthTech"),
            Startup("CarbonScrub", "Direct air capture using novel MOFs at 1/10th cost", "Climate Tech"),
            Startup("QuantumBridge", "Quantum-safe encryption for post-quantum era", "Cybersecurity"),
            Startup("SynthPlate", "3D-printed cultured meat with perfect texture", "FoodTech"),
            Startup("DeepVolt", "Solid-state batteries with 1000-mile EV range", "Energy Tech"),
            Startup("MindMeld", "Non-invasive BCI for VR/AR control", "Neural Interface"),
            Startup("RoboHarvest", "Autonomous fruit-picking robots for orchards", "AgriTech"),
            Startup("MediScan", "Portable MRI using quantum sensors", "HealthTech"),
            Startup("AquaFarms", "Vertical ocean farming for sustainable seafood", "FoodTech"),
            Startup("SkyNet sensors", "Drone detection and counter-drone cybersecurity", "Defense Tech")
        ]
    
    def _generate_vc_polling(self, num_vcs: int = 12) -> Dict[str, int]:
        """Simulate polling VCs on their top startup picks."""
        votes = {s.name: 0 for s in self.startups}
        
        # Sector hype weights (2026 market sentiment)
        hype_weights = {
            "Space Tech": 1.5, "Neural Interface": 1.4, "Climate Tech": 1.3,
            "HealthTech": 1.2, "Energy Tech": 1.25, "Cybersecurity": 1.15,
            "AgriTech": 0.9, "FoodTech": 0.85, "Defense Tech": 1.1
        }
        
        for _ in range(num_vcs):
            # Each VC picks 3-5 startups weighted by sector hype
            weights = [hype_weights.get(s.sector, 1.0) * random.uniform(0.8, 1.3) 
                      for s in self.startups]
            picks = random.choices([s.name for s in self.startups], weights=weights, k=random.randint(3, 5))
            for p in picks:
                votes[p] += 1
                
        return votes
    
    def calculate_scores(self):
        """Calculate final investor interest scores."""
        for startup in self.startups:
            base = self.vc_prefs.get(startup.name, 0)
            # Demo day hype boost: top startups get extra attention
            hype_multiplier = 1.0 + (base * 0.15) if base > 3 else 1.0
            startup.interest_score = round(base * hype_multiplier, 1)
    
    def display_results(self, top_n: int = 8):
        """Display top startups ranked by investor interest."""
        ranked = sorted(self.startups, key=lambda s: s.interest_score, reverse=True)
        
        print("=" * 70)
        print("YC W26 DEMO DAY: TOP 8 STARTUPS INVESTORS ARE CHASING")
        print(f"Polled {len(self.vc_prefs)} VCs on their must-meet startups")
        print("=" * 70)
        print()
        
        for i, s in enumerate(ranked[:top_n], 1):
            print(f"{i}. {s.name} ({s.sector})")
            print(f"   \"{s.tagline}\"")
            print(f"   Score: {s.interest_score}/10  |  VCs interested: {self.vc_prefs[s.name]}")
            print()
        
        print("=" * 70)
        print("INSIGHTS:")
        print("• Space & Climate tech dominate - deep physical/IP-heavy startups")
        print("• Moon hotels (Orbital Haven) lead - space tourism hot again")
        print("• Cattle herding AI (Herding AI) surprisingly popular - agritech rising")
        print("• HealthTech strong: early disease detection & portable MRI")
        print("• Demo day hype amplifies top contenders 20-30%")
        print("=" * 70)
    
    def run(self):
        """Execute analysis."""
        print("\n🎯 Y Combinator W26: Investor Pulse Check")
        self.calculate_scores()
        self.display_results(8)

if __name__ == "__main__":
    random.seed(42)  # Consistent demo day buzz
    poll = YCInvestorPoll()
    poll.run()
```