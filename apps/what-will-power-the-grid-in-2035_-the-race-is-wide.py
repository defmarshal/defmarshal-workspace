```python
#!/usr/bin/env python3
"""
2035 Grid Power Race Simulator
Demonstrates competition between fusion, fission, and gas+CCS for grid power.
"""

from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class Technology:
    """Represents a power generation technology."""
    name: str
    category: str
    base_cost_per_mwh: float
    base_capacity_factor: float
    deployment_speed: float  # GW per year potential
    current_gw: float = 0.0
    tech_readiness: int = 1  # 1-9 scale
    
    def project_2035(self, years: int, policy_support: float, investment: float) -> float:
        """Project capacity by 2035 given conditions."""
        # Growth constrained by tech readiness and deployment speed
        max_deployable = self.deployment_speed * years * (self.tech_readiness / 9.0)
        invested_capacity = investment / self.base_cost_per_mwh * 1000  # $M to GWh
        
        # Policy multiplier (carbon price, subsidies)
        policy_multiplier = 1.0 + (policy_support - 0.5) * 0.5
        
        new_capacity = min(max_deployable, invested_capacity) * policy_multiplier
        return self.current_gw + new_capacity

class GridPowerSimulator:
    """Simulates 2035 grid power composition."""
    
    def __init__(self):
        self.technologies = self._initialize_techs()
        
    def _initialize_techs(self) -> List[Technology]:
        """Initialize competing technologies with 2024 baseline."""
        return [
            Technology(
                name="Nuclear Fission (SMRs)",
                category="Fission",
                base_cost_per_mwh=65.0,
                base_capacity_factor=0.92,
                deployment_speed=8.0,  # GW/year global potential
                current_gw=395.0,  # Global nuclear today
                tech_readiness=9  # Mature
            ),
            Technology(
                name="Natural Gas + CCS",
                category="Gas CCS",
                base_cost_per_mwh=85.0,
                base_capacity_factor=0.70,
                deployment_speed=15.0,
                current_gw=120.0,  # Existing gas + some CCS pilots
                tech_readiness=7  # Demonstrated but not widespread
            ),
            Technology(
                name="Nuclear Fusion",
                category="Fusion",
                base_cost_per_mwh=120.0,  # High initial cost
                base_capacity_factor=0.90,
                deployment_speed=1.5,  # Limited by pilot projects
                current_gw=0.0,
                tech_readiness=4  # Experimental, first plasma soon
            ),
            Technology(
                name="Wind/Solar + Storage",
                category="Renewables",
                base_cost_per_mwh=45.0,
                base_capacity_factor=0.35,  # With storage
                deployment_speed=50.0,
                current_gw=850.0,
                tech_readiness=9
            )
        ]
    
    def simulate_scenario(self, scenario_name: str, policy: float, investment_billions: float):
        """Run a policy/investment scenario."""
        print(f"\n{'='*70}")
        print(f"SCENARIO: {scenario_name.upper()}")
        print(f"Policy support (carbon price/subsidies): {policy:.2f} (0=none, 1=strong)")
        print(f"Additional investment: ${investment_billions}B")
        print(f"{'='*70}\n")
        
        results = []
        total_investment = investment_billions * 1000  # Convert to $M
        
        # Allocate investment based on policy priorities
        if policy > 0.6:
            # Pro-climate: favor fission and fusion
            allocation = {"Fission": 0.35, "Gas CCS": 0.15, "Fusion": 0.30, "Renewables": 0.20}
        elif policy > 0.3:
            # Balanced
            allocation = {"Fission": 0.25, "Gas CCS": 0.25, "Fusion": 0.15, "Renewables": 0.35}
        else:
            # Pro-gas/business-as-usual
            allocation = {"Fission": 0.15, "Gas CCS": 0.45, "Fusion": 0.05, "Renewables": 0.35}
        
        for tech in self.technologies:
            invested = total_investment * allocation.get(tech.category, 0.25)
            projected = tech.project_2035(
                years=11,  # 2024-2035
                policy_support=policy,
                investment=invested
            )
            results.append({
                'name': tech.name,
                'category': tech.category,
                '2035_gw': round(projected, 1),
                'cost_mwh': tech.base_cost_per_mwh,
                'cap_factor': tech.base_capacity_factor
            })
        
        self._display_results(results)
        return results
    
    def _display_results(self, results: List[Dict]):
        """Display simulation results in a table."""
        print(f"{'Technology':<30} {'2035 Capacity (GW)':>20} {'Cost ($/MWh)':>15}")
        print("-"*70)
        
        total_gw = 0
        for r in sorted(results, key=lambda x: x['2035_gw'], reverse=True):
            print(f"{r['name']:<30} {r['2035_gw']:>20,.1f} {r['cost_mwh']:>15,.0f}")
            total_gw += r['2035_gw']
        
        print("-"*70)
        print(f"{'TOTAL':<30} {total_gw:>20,.1f} GW")
        print(f"{'% of US Grid (~1000 GW demand)':<30} {total_gw/1000*100:>19,.1f}%")
        
        # Calculate approximate emissions
        emissions = self._estimate_emissions(results)
        print(f"\nEstimated CO2: {emissions:,.0f} Mt/year")
        print(f"(vs. 2024 US power sector: ~1,500 Mt/year)")
    
    def _estimate_emissions(self, results: List[Dict]) -> float:
        """Rough CO2 estimate from gas generation."""
        gas_gw = next(r for r in results if 'Gas' in r['category'])['2035_gw']
        # Assume 0.4 tCO2/MWh for gas CCGT, 8760 hours/year
        return gas_gw * 1000 * 8760 * 0.4 / 1_000_000
    
    def race_summary(self):
        """Print summary of the 2035 power race."""
        print("\n" + "="*70)
        print("THE 2035 GRID POWER RACE: KEY INSIGHTS")
        print("="*70)
        print("""
1. RACE TRULY 'WIDE OPEN': No single technology dominates. All three
   (fission, gas+CCS, fusion) have plausible paths to significant
   capacity by 2035 depending on policy and investment.

2. FISSION (SMRs) is the safest bet: mature technology, high capacity
   factor, zero emissions. Main barriers: public acceptance and upfront
   capital cost. Likely 50-150 GW new by 2035 if regulations streamline.

3. GAS+CCS is the dark horse: Cheap, fast to build, flexible. But CCS
   adds cost and complexity, and long-term viability questionable if
   carbon prices rise. May get 30-80 GW by 2035 as transitional bridge.

4. FUSION is the long shot: First demo plants might connect 2035-2040.
   Not a major contributor by 2035, but if ITER/private companies
   achieve breakthrough, could accelerate dramatically post-2035.

5. RENEWABLES+STORAGE are the elephant in the room: They'll dominate
   new capacity additions regardless. The race is about what fills the
   'firm power' gap when sun/wind aren't available.

POLICY DECISIONS in next 2-3 years will determine the winner:
- Carbon pricing ($50-100/ton) favors fission & renewables
- Nuclear subsidies/streamlined permitting favor SMRs
- CCS tax credits ($50/ton) could unlock gas+CCS boom
- Fusion research funding could shave years off timeline

BOTTOM LINE: 2035 grid will be a mix, but the relative shares of
fission vs gas+CCS vs fusion remain genuinely up for grabs.
        """)
        print("="*70)

def main():
    """Run the grid power race simulation."""
    random.seed(42)
    
    print("⚡ 2035 GRID POWER RACE SIMULATOR")
    print("Comparing fusion, fission, and gas+CCS trajectories")
    
    simulator = GridPowerSimulator()
    
    # Run three scenarios
    simulator.simulate_scenario(
        scenario_name="Climate Action Aggressive",
        policy=0.8,
        investment_billions=120.0
    )
    
    simulator.simulate_scenario(
        scenario_name="Status Quo / Balanced",
        policy=0.5,
        investment_billions=80.0
    )
    
    simulator.simulate_scenario(
        scenario_name="Business as Usual",
        policy=0.2,
        investment_billions=50.0
    )
    
    simulator.race_summary()

if __name__ == "__main__":
    main()
```