```python
#!/usr/bin/env python3
"""
YC Demo Day Startup Hype Simulator
Based on "From Moon hotels to cattle herding: 8 startups investors chased at YC Demo Day"
Simulates investor interest polling across 12 VCs for W26 batch.
"""

import random
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Startup:
    """Represents a YC startup."""
    name: str
    description: str
    sector: str
    base_interest: float  # 0.0-1.0, inherent investor appeal
    ask: float  # in millions USD
    vc_interest: List[bool] = None
    
    def __post_init__(self):
        self.vc_interest = []

@dataclass
class VC:
    """Represents a venture capital firm."""
    name: str
    check_size: float  # typical investment amount in millions
    focus_areas: List[str]  # sectors they invest in

    def is_interested(self, startup: Startup) -> bool:
        """VC decides to chase startup based on interest and sector alignment."""
        # Base probability from startup's inherent appeal
        prob = startup.base_interest
        
        # Boost if VC's focus includes startup's sector
        if startup.sector in self.focus_areas:
            prob += 0.3
        
        # Random factor (some VCs more aggressive, some conservative)
        prob = min(0.95, prob)
        return random.random() < prob

def generate_w26_startups() -> List[Startup]:
    """Create the 8 notable startups from W26 batch."""
    return [
        Startup(
            name="MoonHotels",
            description="Modular habitats for lunar tourism and research",
            sector="space",
            base_interest=0.7,
            ask=3.5
        ),
        Startup(
            name="HerdTech",
            description="AI-powered drone herding for large cattle ranches",
            sector="agritech",
            base_interest=0.5,
            ask=2.0
        ),
        Startup(
            name="OceanFarm",
            description="Deep-sea automated kelp and mussel cultivation",
            sector="climate",
            base_interest=0.6,
            ask=2.8
        ),
        Startup(
            name="QuantumLeap",
            description="Quantum-accelerated supply chain optimization SaaS",
            sector="enterprise",
            base_interest=0.8,
            ask=4.0
        ),
        Startup(
            name="BioBrew",
            description="Fermentation-based alternative protein at $2/lb",
            sector="foodtech",
            base_interest=0.9,
            ask=3.0
        ),
        Startup(
            name="SolarSkynet",
            description="High-altitude balloons for 24/7 solar energy collection",
            sector="energy",
            base_interest=0.75,
            ask=5.0
        ),
        Startup(
            name="NeuroLink",
            description="Non-invasive BCI for gaming and productivity",
            sector="neurotech",
            base_interest=0.85,
            ask=4.5
        ),
        Startup(
            name="CryoHarvest",
            description="Cryopreservation of endangered plant genetic material",
            sector="biotech",
            base_interest=0.4,
            ask=1.5
        )
    ]

def generate_vcs() -> List[VC]:
    """Create a diverse set of VCs that attend YC Demo Day."""
    return [
        VC("Andreessen Horowitz", 5.0, ["enterprise", "ai", "fintech"]),
        VC("Sequoia Capital", 4.0, ["consumer", "enterprise", "health"]),
        VC("Y Combinator Continuity", 2.0, ["everything"]),
        VC("Founders Fund", 3.0, ["space", "deep tech", "biotech"]),
        VC("Lightspeed Venture Partners", 2.5, ["consumer", "fintech"]),
        VC("General Catalyst", 3.0, ["health", "climate", "enterprise"]),
        VC("Tiger Global", 4.0, ["consumer", "fintech"]),
        VC("Accel", 3.5, ["enterprise", "ai"]),
        VC("Index Ventures", 2.0, ["saaS", "consumer"]),
        VC("First Round Capital", 1.0, ["consumer", "d2c"]),
        VC("Bessemer Venture Partners", 2.5, ["enterprise", "health"]),
        VC("Khosla Ventures", 3.0, ["climate", "deep tech", "health"])
    ]

def run_poll(startups: List[Startup], vcs: List[VC]) -> List[Tuple]:
    """Simulate polling VCs about which startups they're chasing."""
    results = []
    
    for startup in startups:
        interest_count = 0
        interested_vcs = []
        
        for vc in vcs:
            if vc.is_interested(startup):
                interest_count += 1
                interested_vcs.append(vc.name)
        
        results.append({
            'startup': startup.name,
            'description': startup.description,
            'sector': startup.sector,
            'ask': startup.ask,
            'interest_count': interest_count,
            'interested_vcs': interested_vcs,
            'expected_commitment': interest_count * vc.check_size * 0.3  # 30% chance they invest average check
        })
    
    return sorted(results, key=lambda x: x['interest_count'], reverse=True)

def print_results(results: List[dict]):
    """Display the polling results in a readable format."""
    print("=" * 70)
    print("YC W26 DEMO DAY: MOST SOUGHT-AFTER STARTUPS (POLL OF 12 VCs)")
    print("=" * 70)
    
    print("\n🏆 TOP 5 CHASED STARTUPS:")
    print("-" * 70)
    for i, r in enumerate(results[:5], 1):
        print(f"\n{i}. {r['startup']} ({r['sector']})")
        print(f"   {r['description']}")
        print(f"   Ask: ${r['ask']}M | VCs interested: {r['interest_count']}/12")
        print(f"   Top backers: {', '.join(r['interested_vcs'][:3])}")
        if r['interest_count'] >= 8:
            print(f"   ⚡ VERY HOT: Multiple term sheets expected")
        elif r['interest_count'] >= 6:
            print(f"   🔥 HOT: Strong competition")
        else:
            print(f"   🤔 Moderate interest")
    
    print("\n" + "-" * 70)
    print("\n📊 FULL RANKING:")
    print("-" * 70)
    for i, r in enumerate(results, 1):
        print(f"{i:2}. {r['startup'][:20]:20} | {r['sector'][:12]:12} | {r['interest_count']:2}/12 VCs | Ask: ${r['ask']}M")

def simulate_tournament():
    """
    Simulate a 'tournament' where investors gradually focus on fewer startups
    as they commit, showing how interest concentrates.
    """
    print("\n" + "=" * 70)
    print("SIMULATED INVESTMENT ROUND PROGRESSION")
    print("=" * 70)
    
    startups = generate_w26_startups()
    vcs = generate_vcs()
    results = run_poll(startups, vcs)
    
    # Print initial poll
    print_results(results)
    
    # Simulate first round commitments (some VCs commit to their top choice)
    print("\n" + "=" * 70)
    print("AFTER FIRST ROUND COMMITMENTS (simulated)")
    print("=" * 70)
    
    committed = set()
    commitments = []
    
    # Each VC picks one startup to commit to (their top interest)
    for vc in vcs:
        # Find the startup this VC is interested in with highest overall interest
        candidates = [r for r in results if vc.name in r['interested_vcs'] and r['startup'] not in committed]
        if candidates:
            chosen = max(candidates, key=lambda x: x['interest_count'])
            committed.add(chosen['startup'])
            commitments.append((vc.name, chosen['startup'], chosen['ask'] * 0.5))  # 50% of ask
    
    print("\nInitial commitments (first checks):")
    for vc, startup, amount in commitments[:6]:
        print(f"  {vc} commits ${amount:.1f}M to {startup}")
    
    print(f"\n... and {len(commitments)-6} more")
    
    # Show which startups got multiple commitments
    startup_commits = {}
    for _, startup, _ in commitments:
        startup_commits[startup] = startup_commits.get(startup, 0) + 1
    
    print("\nStartup commitment counts:")
    for startup, count in sorted(startup_commits.items(), key=lambda x: x[1], reverse=True):
        print(f"  {startup}: {count} commitment(s)")

def main():
    """Run the YC Demo Day analysis."""
    random.seed(42)  # reproducible poll
    
    print("="*70)
    print("YC W26 DEMO DAY: INVESTOR CHASE ANALYSIS")
    print("Based on polling 12 top VCs about 8 standout startups")
    print("="*70)
    
    startups = generate_w26_startups()
    vcs = generate_vcs()
    
    print(f"\n[BATCH STATS]")
    print(f"  Total startups analyzed: 8 (most sought after)")
    print(f"  VCs polled: {len(vcs)}")
    print(f"  Sectors represented: {sorted(set(s.sector for s in startups))}")
    
    print("\n[STARTUPS IN THE BATCH]")
    for s in startups:
        print(f"  {s.name}: {s.sector} | Ask: ${s.ask}M")
    
    results = run_poll(startups, vcs)
    print_results(results)
    
    # Additional analysis
    print("\n" + "="*70)
    print("KEY INSIGHTS:")
    print("="*70)
    
    # Sector concentration
    sector_hotness = {}
    for r in results:
        sector = r['sector']
        sector_hotness[sector] = sector_hotness.get(sector, 0) + r['interest_count']
    
    print("\nHot sectors by total VC interest:")
    for sector, score in sorted(sector_hotness.items(), key=lambda x: x[1], reverse=True):
        print(f"  {sector}: {score} interest points")
    
    # Most mentioned VCs
    vc_mentions = {}
    for r in results:
        for vc in r['interested_vcs']:
            vc_mentions[vc] = vc_mentions.get(vc, 0) + 1
    
    print("\nMost active VCs in this batch:")
    for vc, count in sorted(vc_mentions.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {vc}: interested in {count} startups")
    
    print("\n💡 OBSERVATIONS:")
    print("- NeuroLink and BioBrew lead due to high-impact, high-margin sectors")
    print("- CryoHarvest is niche but appeals to specialized biotech investors")
    print("- Space (MoonHotels) remains polarizing: some VCs love it, others avoid")
    print("- Multiple VCs chase same few startups → competitive rounds expected")
    print("- Agritech (HerdTech) and climate (OceanFarm) have moderate but steady interest")
    
    print("\n" + "="*70)
    print("Simulation complete. In reality, YC Demo Day results vary!")
    print("="*70)

if __name__ == "__main__":
    simulate_tournament()
```