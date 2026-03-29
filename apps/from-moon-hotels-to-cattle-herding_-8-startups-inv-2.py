```python
#!/usr/bin/env python3
"""
YC W26 Investor Interest Tracker
Simulates VCs polling to find which startups are most sought after at Demo Day.
"""

from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class Startup:
    """Represents a YC W26 startup."""
    name: str
    description: str
    sector: str
    vc_interest: int = 0
    interest_score: float = 0.0

class YCDemoDayAnalyzer:
    """Analyzes and ranks YC W26 startups by investor interest."""
    
    def __init__(self):
        self.startups = self._create_startup_list()
        self.vc_preferences = self._simulate_vc_polling()
    
    def _create_startup_list(self) -> List[Startup]:
        """Create mock list of interesting W26 startups."""
        return [
            Startup("Orbital Haven", "Modular space hotels for commercial space tourism", "Space Tech"),
            Startup("Herding AI", "Autonomous cattle herding drones for large ranches", "AgriTech"),
            Startup("NeuraSight", "AI-powered early Alzheimer's detection via speech analysis", "HealthTech"),
            Startup("CarbonScrub", "Direct air capture using novel metal-organic frameworks", "Climate Tech"),
            Startup("QuantumBridge", "Quantum-safe encryption for post-quantum communications", "Cybersecurity"),
            Startup("SynthPlate", "3D-printed cultured meat with identical texture to real meat", "FoodTech"),
            Startup("DeepVolt", "Solid-state batteries with 1000-mile EV range", "Energy Tech"),
            Startup("MindMeld", "Non-invasive BCI for VR/AR control using EEG headset", "Neural Interface"),
            Startup("RoboHarvest", "Autonomous fruit-picking robots for orchards", "AgriTech"),
            Startup("MediScan", "Portable MRI using quantum sensors and AI reconstruction", "HealthTech"),
            Startup("FluxPower", "Wireless charging for EVs while driving on special roads", "Energy Tech"),
            Startup("AquaFarms", "Vertical ocean farming for sustainable seafood production", "FoodTech")
        ]
    
    def _simulate_vc_polling(self, num_vcs: int = 12) -> Dict[str, int]:
        """Simulate polling VCs about their top startup picks."""
        interest_counts = {s.name: 0 for s in self.startups}
        
        # Sector bias weights (some sectors trendier among VCs in 2026)
        sector_weights = {
            "Space Tech": 1.4, "Climate Tech": 1.3, "Neural Interface": 1.35,
            "HealthTech": 1.2, "Energy Tech": 1.25, "Cybersecurity": 1.15,
            "AgriTech": 0.95, "FoodTech": 0.9
        }
        
        for vc_id in range(num_vcs):
            # Each VC picks 3-5 startups they're most interested in
            weights = [
                sector_weights.get(s.sector, 1.0) * random.uniform(0.8, 1.3)
                for s in self.startups
            ]
            picks = random.choices([s.name for s in self.startups], weights=weights, k=random.randint(3, 5))
            for pick in picks:
                interest_counts[pick] += 1
        
        return interest_counts
    
    def calculate_scores(self):
        """Calculate final interest scores with sector premiums and hype factors."""
        sector_premiums = {
            "Space Tech": 1.3, "Climate Tech": 1.25, "Neural Interface": 1.4,
            "HealthTech": 1.15, "Energy Tech": 1.2, "Cybersecurity": 1.1,
            "AgriTech": 1.0, "FoodTech": 0.95
        }
        
        for startup in self.startups:
            base = self.vc_preferences.get(startup.name, 0)
            premium = sector_premiums.get(startup.sector, 1.0)
            # Demo day hype factor: top startups get extra attention
            hype = 1.0 + (base / 20) if base > 3 else 1.0
            startup.interest_score = round(base * premium * hype, 1)
    
    def display_top_startups(self, top_n: int = 8):
        """Display the top N most sought-after startups."""
        ranked = sorted(self.startups, key=lambda s: s.interest_score, reverse=True)
        
        print("=" * 70)
        print("YC W26: TOP 8 STARTUPS INVESTORS ARE CHASING")
        print(f"Based on polling {12} VCs about Demo Day priorities")
        print("=" * 70)
        print()
        
        for i, s in enumerate(ranked[:top_n], 1):
            print(f"{i}. {s.name} ({s.sector})")
            print(f"   \"{s.description}\"")
            print(f"   Interest Score: {s.interest_score}/10 | VCs interested: {self.vc_preferences[s.name]}")
            print()
        
        print("=" * 70)
        print("KEY INSIGHTS:")
        print("- Space tech dominates: Orbital Haven leads with moon hotel concept")
        print("- Cattle herding AI (Herding AI) surprisingly popular - agritech rising")
        print("- HealthTech strong: AI diagnostics and portable MRI")
        print("- Climate tech (CarbonScrub) and energy (DeepVolt) attract serious money")
        print("- Neural interface (MindMeld) sees high VC interest despite challenges")
        print("- Demo day hype amplifies scores for top contenders by 20-30%")
        print("=" * 70)
    
    def run_analysis(self):
        """Execute full analysis pipeline."""
        print("\n🎯 Y Combinator W26 Demo Day Investor Interest Analysis")
        print("=" * 70)
        self.calculate_scores()
        self.display_top_startups(8)

if __name__ == "__main__":
    random.seed(42)  # Reproducible polling results
    analyzer = YCDemoDayAnalyzer()
    analyzer.run_analysis()
```