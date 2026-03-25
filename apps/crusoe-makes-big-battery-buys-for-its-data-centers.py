```python
#!/usr/bin/env python3
"""
Crusoe Data Centers: Battery Procurement Strategy
Simulating large-scale battery purchases from Form Energy and Redwood Materials
for data center backup power and grid services.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict

@dataclass
class BatteryOrder:
    supplier: str
    technology: str
    capacity_mwh: float
    duration_hours: float
    cost_per_mwh: float
    delivery_date: str
    use_case: str

class CrusoeBatteryPortfolio:
    def __init__(self):
        self.orders: List[BatteryOrder] = []
        self.total_capacity = 0
        self.total_cost = 0
    
    def add_order(self, order: BatteryOrder):
        self.orders.append(order)
        self.total_capacity += order.capacity_mwh
        self.total_cost += order.capacity_mwh * order.cost_per_mwh
    
    def get_portfolio_summary(self) -> Dict:
        by_tech = {}
        for order in self.orders:
            by_tech[order.technology] = by_tech.get(order.technology, 0) + order.capacity_mwh
        
        return {
            'total_capacity_mwh': round(self.total_capacity, 1),
            'total_cost_mm': round(self.total_cost / 1e6, 1),
            'num_suppliers': len(set(o.supplier for o in self.orders)),
            'tech_breakdown': {k: round(v, 1) for k, v in by_tech.items()},
            'backup_hours': self.calculate_backup_hours()
        }
    
    def calculate_backup_hours(self) -> float:
        """Assuming 100MW critical load per data center"""
        critical_load_mw = 100
        total_backup_hours = sum(o.capacity_mwh * o.duration_hours for o in self.orders)
        return total_backup_hours / critical_load_mw if critical_load_mw > 0 else 0

def main():
    print("=" * 70)
    print("Crusoe Energy: Data Center Battery Portfolio")
    print("Strategic procurement from Form Energy & Redwood Materials")
    print("=" * 70)
    print()
    
    portfolio = CrusoeBatteryPortfolio()
    
    # Form Energy: Iron-air batteries (long duration, low cost)
    form_orders = [
        BatteryOrder(
            supplier="Form Energy",
            technology="Iron-Air",
            capacity_mwh=200,
            duration_hours=100,
            cost_per_mwh=120_000,  # $120k/MWh (target price)
            delivery_date="2026-Q3",
            use_case="Multi-day grid backup"
        ),
        BatteryOrder(
            supplier="Form Energy",
            technology="Iron-Air",
            capacity_mwh=300,
            duration_hours=100,
            cost_per_mwh=115_000,  # Volume discount
            delivery_date="2026-Q4",
            use_case="Renewable firming"
        ),
        BatteryOrder(
            supplier="Form Energy",
            technology="Iron-Air",
            capacity_mwh=500,
            duration_hours=100,
            cost_per_mwh=110_000,  # Mass production pricing
            delivery_date="2027-Q2",
            use_case="Base load replacement"
        )
    ]
    
    # Redwood Materials: Lithium-ion (high power, fast response)
    redwood_orders = [
        BatteryOrder(
            supplier="Redwood Materials",
            technology="Lithium-Ion (NMC)",
            capacity_mwh=50,
            duration_hours=4,
            cost_per_mwh=350_000,  # $350k/MWh (market rate)
            delivery_date="2026-Q2",
            use_case="Frequency regulation"
        ),
        BatteryOrder(
            supplier="Redwood Materials",
            technology="Lithium-Ion (NMC)",
            capacity_mwh=80,
            duration_hours=4,
            cost_per_mwh=340_000,
            delivery_date="2026-Q3",
            use_case="Peak shaving"
        ),
        BatteryOrder(
            supplier="Redwood Materials",
            technology="Lithium-Ion (NMC)",
            capacity_mwh=120,
            duration_hours=4,
            cost_per_mwh=330_000,
            delivery_date="2026-Q4",
            use_case="Black start capability"
        )
    ]
    
    # Add orders to portfolio
    for order in form_orders + redwood_orders:
        portfolio.add_order(order)
    
    # Display individual orders
    print("INDIVIDUAL ORDERS:")
    print("-" * 70)
    for i, order in enumerate(portfolio.orders, 1):
        print(f"{i}. {order.supplier} | {order.technology}")
        print(f"   Capacity: {order.capacity_mwh} MWh | Duration: {order.duration_hours} hrs")
        print(f"   Cost: ${order.cost_per_mwh:,}/MWh | Delivery: {order.delivery_date}")
        print(f"   Use case: {order.use_case}")
        print()
    
    # Portfolio summary
    summary = portfolio.get_portfolio_summary()
    
    print("=" * 70)
    print("PORTFOLIO SUMMARY")
    print("=" * 70)
    print(f"Total Battery Capacity: {summary['total_capacity_mwh']} MWh")
    print(f"Total Investment: ${summary['total_cost_mm']} million")
    print(f"Suppliers: {summary['num_suppliers']}")
    print(f"Backup Duration: {summary['backup_hours']:.1f} hours at 100MW load")
    print()
    print("Technology Mix:")
    for tech, cap in summary['tech_breakdown'].items():
        pct = (cap / summary['total_capacity_mwh']) * 100
        print(f"  - {tech}: {cap} MWh ({pct:.1f}%)")
    print()
    
    print("STRATEGIC RATIONALE:")
    print("-" * 70)
    print("1. DIVERSIFICATION: Iron-air (long duration) + Li-ion (fast response)")
    print("   - Form Energy: 1000 MWh for multi-day grid resilience")
    print("   - Redwood: 250 MWh for sub-second frequency regulation")
    print()
    print("2. COST OPTIMIZATION: Iron-air at $110-120k/MWh vs Li-ion $330-350k/MWh")
    print(f"   - Average blended cost: ${summary['total_cost_mm']*1e6/summary['total_capacity_mwh']:,.0f}/MWh")
    print()
    print("3. TIMELINE ALIGNMENT: Phased delivery matches data center build-out")
    print("   - 2026-Q2: Initial 50 MWh for first data center")
    print("   - 2026-Q4: Scale to 400 MWh across fleet")
    print("   - 2027+: 500 MWh iron-air for renewable integration")
    print()
    print("4. ENVIRONMENTAL: Iron-air uses abundant materials (iron, water, air)")
    print("   - No lithium/coobalt/cobalt supply chain concerns")
    print("   - Redwood's recycled lithium closes loop")
    print()
    
    print("RISK FACTORS:")
    print("-" * 70)
    print("⚠️  Form Energy: Technology risk (first commercial scale)")
    print("⚠️  Redwood Materials: Commodity price exposure (lithium)")
    print("⚠️  Integration: Need power conversion systems (PCS) compatible")
    print("⚠️  Timeline: Supply chain delays could affect data center commissioning")
    print()
    
    print("FINANCIAL IMPACT:")
    print("-" * 70)
    annual_energy_savings = portfolio.total_cost * 0.15  # Assume 15% grid cost savings
    payback_years = portfolio.total_cost / annual_energy_savings if annual_energy_savings > 0 else float('inf')
    print(f"Estimated annual energy savings: ${annual_energy_savings/1e6:.1f}M")
    print(f"Simple payback period: {payback_years:.1f} years")
    print(f"Carbon reduction: ~{summary['total_capacity_mwh'] * 500:.0f} tons CO2/year")
    print()
    
    print("=" * 70)
    print("CONCLUSION: Strategic battery portfolio enables")
    print(" - 24/7 uptime for AI workloads")
    print(" - Grid services revenue (demand response)")
    print(" - Renewable energy integration")
    print(" - ESG positioning for investors")
    print("=" * 70)

if __name__ == "__main__":
    main()
```