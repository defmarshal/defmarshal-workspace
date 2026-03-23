```python
#!/usr/bin/env python3
"""AI Energy Investment Calculator

Demystifies the AI-data-center energy bottleneck. Calculates power needs, 
costs, and ROI for energy-efficient upgrades or renewable investments.
Based on: "Power has become one of the biggest bottlenecks in rolling out 
new AI data centers. That's creating an opening for investors."
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class AIDataCenter:
    """Configurable AI data center parameters."""
    gpu_count: int = 1000            # Number of GPUs (e.g., H100)
    gpu_power_watts: float = 700     # Power per GPU (W)
    utilization: float = 0.6         # Average utilization (0-1)
    pue: float = 1.1                # Power Usage Effectiveness
    electricity_cost_kwh: float = 0.12  # $/kWh
    carbon_intensity: float = 400     # g CO2/kWh (grid average)

def calculate_energy(dc: AIDataCenter) -> Dict[str, float]:
    """Compute power and energy metrics."""
    it_power = dc.gpu_count * dc.gpu_power_watts * dc.utilization
    total_power = it_power * dc.pue  # includes cooling, overhead
    annual_energy_mwh = total_power * 24 * 365 / 1000
    annual_cost = annual_energy_mwh * 1000 * dc.electricity_cost_kwh
    annual_carbon = annual_energy_mwh * 1000 * dc.carbon_intensity / 1_000_000  # tons
    
    return {
        "IT Power (kW)": it_power / 1000,
        "Total Facility Power (MW)": total_power / 1_000_000,
        "Annual Energy (MWh)": annual_energy_mwh,
        "Annual Cost ($M)": annual_cost / 1_000_000,
        "Annual Carbon (tons CO2)": annual_carbon,
    }

def investment_roi(dc: AIDataCenter, upgrade_cost: float, improvement_factor: float, years: int = 5) -> Dict[str, float]:
    """Calculate ROI for an energy efficiency upgrade."""
    base_metrics = calculate_energy(dc)
    base_annual_cost = base_metrics["Annual Cost ($M)"]
    
    # After upgrade: power reduces by improvement_factor (e.g., 0.2 = 20% reduction)
    upgraded_dc = AIDataCenter(
        gpu_count=dc.gpu_count,
        gpu_power_watts=dc.gpu_power_watts * improvement_factor,
        utilization=dc.utilization,
        pue=dc.pue * (1 - improvement_factor/2),  # PUE also improves slightly
        electricity_cost_kwh=dc.electricity_cost_kwh,
        carbon_intensity=dc.carbon_intensity
    )
    upgraded_metrics = calculate_energy(upgraded_dc)
    annual_savings = base_annual_cost - upgraded_metrics["Annual Cost ($M)"]
    total_savings = annual_savings * years
    simple_roi = (total_savings - upgrade_cost) / upgrade_cost * 100
    
    return {
        "Upgrade Cost ($M)": upgrade_cost / 1_000_000,
        "Annual Energy Savings (MWh)": base_metrics["Annual Energy (MWh)"] - upgraded_metrics["Annual Energy (MWh)"],
        "Annual Cost Savings ($M)": annual_savings,
        f"5-Year Total Savings ($M)": total_savings,
        "Simple ROI (%)": simple_roi,
        "Payback Period (years)": upgrade_cost / (annual_savings * 1_000_000) if annual_savings > 0 else float('inf')
    }

def renewable_investment_case(dc: AIDataCenter, solar_farm_cost_per_mw: float = 1.5e6) -> Dict[str, float]:
    """Model building a solar farm to power the data center."""
    metrics = calculate_energy(dc)
    required_mw = metrics["Total Facility Power (MW)"]
    # Assume 20% capacity factor for solar
    solar_capacity_mw = required_mw / 0.2
    solar_cost = solar_capacity_mw * solar_farm_cost_per_mw
    
    # Without solar: grid power cost
    grid_annual_cost = metrics["Annual Cost ($M)"]
    
    # With solar: mostly free after capex, minus small O&M
    solar_annual_om = solar_cost * 0.01  # 1% O&M
    solar_annual_savings = grid_annual_cost - solar_annual_om / 1_000_000
    
    roi_10yr = (solar_annual_savings * 10 - solar_cost) / solar_cost * 100
    
    return {
        "Required Solar Capacity (MW)": solar_capacity_mw,
        "Solar Farm Capex ($M)": solar_cost / 1_000_000,
        "Annual O&M ($M)": solar_annual_om / 1_000_000,
        "Annual Grid Cost Avoided ($M)": grid_annual_cost,
        "10-Year ROI (%)": roi_10yr,
        "Break-even (years)": solar_cost / (solar_annual_savings * 1_000_000) if solar_annual_savings > 0 else float('inf')
    }

def print_report(dc: AIDataCenter):
    """Generate investment insight report."""
    print("=== AI DATA CENTER ENERGY INVESTMENT ANALYSIS ===\n")
    
    print("BASE CONFIGURATION:")
    print(f"  GPUs: {dc.gpu_count:,} @ {dc.gpu_power_watts}W each")
    print(f"  PUE: {dc.pue:.2f} | Utilization: {dc.utilization*100:.0f}%")
    print(f"  Electricity: ${dc.electricity_cost_kwh:.3f}/kWh | Grid carbon: {dc.carbon_intensity} g/kWh\n")
    
    base = calculate_energy(dc)
    print("ENERGY PROFILE:")
    for k, v in base.items():
        if isinstance(v, float):
            print(f"  {k}: {v:,.2f}")
        else:
            print(f"  {k}: {v:,}")
    print()
    
    print("INVESTMENT SCENARIOS:\n")
    
    # Scenario 1: Liquid cooling upgrade
    print("1. Liquid Cooling & Efficiency Upgrade ($50M)")
    liquid_roi = investment_roi(dc, upgrade_cost=50e6, improvement_factor=0.15)  # 15% power reduction
    for k, v in liquid_roi.items():
        print(f"   {k}: {v:.2f}" if isinstance(v, float) else f"   {k}: {v}")
    print()
    
    # Scenario 2: On-site solar + storage
    print("2. Solar + Battery Microgrid ($320M)")
    solar_case = renewable_investment_case(dc)
    for k, v in solar_case.items():
        print(f"   {k}: {v:.2f}" if isinstance(v, float) else f"   {k}: {v}")
    print()
    
    # Scenario 3: Co-locate with nuclear
    print("3. Advanced Small Modular Reactor (SMR) Partnership ($800M capex share)")
    # Nuclear: very low cost per MWh after capex
    nuclear_annual_om = (dc.gpu_count * dc.gpu_power_watts * dc.utilization * dc.pue * 24 * 365 / 1000) * 0.02 / 1000  # $/MWh O&M
    nuclear_annual_savings = base["Annual Cost ($M)"] - nuclear_annual_om
    nuclear_roi_15yr = (nuclear_annual_savings * 15 - 800e6) / 800e6 * 100
    print(f"   Capex ($M): 800.00")
    print(f"   Annual O&M ($M): {nuclear_annual_om/1e6:.2f}")
    print(f"   15-Year ROI: {nuclear_roi_15yr:.1f}%")
    print()
    
    print("=== KEY INSIGHTS ===")
    print("• Energy is now the dominant OpEx for AI data centers (often >50% of total).")
    print("• Power availability, not just cost, is the bottleneck for new builds.")
    print("• Investments in energy tech (efficiency, renewables, nuclear) offer")
    print("  compelling returns by reducing or stabilizing long-term power costs.")
    print("• The 'AI energy gap' creates opportunities for energy tech investors.")

def main():
    # Configure a typical large AI training cluster
    cluster = AIDataCenter(
        gpu_count=2048,          # ~2k H100s
        gpu_power_watts=700,
        utilization=0.7,
        pue=1.15,
        electricity_cost_kwh=0.09,
        carbon_intensity=350
    )
    
    print_report(cluster)

if __name__ == "__main__":
    main()
```