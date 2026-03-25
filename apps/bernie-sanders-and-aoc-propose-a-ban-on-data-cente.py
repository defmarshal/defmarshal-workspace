```python
#!/usr/bin/env python3
"""
Bernie & AOC Data Center Construction Ban Simulator
Models the impact of halting new data center builds until AI regulation passes.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict
import random

@dataclass
class DataCenterProject:
    name: str
    location: str
    capacity_mw: float
    cost_million: float
    start_date: datetime
    planned_completion: datetime
    status: str = "pending"  # pending, under_construction, halted, completed
    employer: str = ""  # AWS, Google, Microsoft, etc.

class ConstructionBanSimulator:
    def __init__(self):
        self.projects: List[DataCenterProject] = []
        self.ban_start_date = datetime(2026, 3, 25)  # Bill introduction date
        self.regulation_eta_months = random.randint(18, 48)  # Uncertain legislation timeline
        self.ban_active = True
        
    def add_project(self, project: DataCenterProject):
        self.projects.append(project)
    
    def apply_ban(self):
        """Apply construction ban to all projects not yet completed."""
        print("=" * 70)
        print("🏗️  DATA CENTER CONSTRUCTION BAN INITIATED")
        print("=" * 70)
        print(f"Bill introduced: {self.ban_start_date.strftime('%Y-%m-%d')}")
        print(f"Status: All new construction HALTED until AI regulation enacted")
        print(f"Estimated regulation timeline: {self.regulation_eta_months} months")
        print()
        
        halted_count = 0
        for p in self.projects:
            if p.status in ["pending", "under_construction"]:
                p.status = "halted"
                halted_count += 1
                print(f"⛔ HALTED: {p.name} ({p.location}, {p.capacity_mw} MW)")
        
        print(f"\nTotal projects halted: {halted_count}/{len(self.projects)}")
        print(f"Construction pause until: {self._estimate_regulation_date().strftime('%Y-%m-%d')}")
        print()
    
    def _estimate_regulation_date(self) -> datetime:
        return self.ban_start_date + timedelta(days=self.regulation_eta_months * 30.44)
    
    def calculate_economic_impact(self) -> Dict:
        """Calculate economic impact of construction ban."""
        halted_projects = [p for p in self.projects if p.status == "halted"]
        
        if not halted_projects:
            return {"message": "No projects affected"}
        
        total_capacity = sum(p.capacity_mw for p in halted_projects)
        total_cost = sum(p.cost_million for p in halted_projects)
        avg_cost_per_mw = total_cost / total_capacity if total_capacity > 0 else 0
        
        # Construction jobs lost (estimate: 15 jobs per MW)
        construction_jobs = int(total_capacity * 15)
        construction_salary_total = construction_jobs * 75000  # avg $75k/year
        
        # Operational jobs lost (estimate: 0.1 jobs per MW, long-term)
        operational_jobs = int(total_capacity * 0.1)
        operational_salary_total = operational_jobs * 100000
        
        # Energy capacity impact (AI demand growth)
        delayed_capacity_mw = total_capacity
        estimated_ai_compute_shortfall = delayed_capacity_mw * 0.6  # 60% allocated to AI workloads
        
        return {
            "projects_halted": len(halted_projects),
            "total_capacity_mw": total_capacity,
            "total_construction_cost_million": total_cost,
            "avg_cost_per_mw": avg_cost_per_mw,
            "construction_jobs_lost": construction_jobs,
            "construction_salary_loss_yearly": construction_salary_total,
            "operational_jobs_lost": operational_jobs,
            "operational_salary_loss_yearly": operational_salary_total,
            "ai_compute_capacity_delayed_mw": estimated_ai_compute_shortfall,
            "regulation_eta_months": self.regulation_eta_months
        }
    
    def simulate_legislative_process(self):
        """Simulate the legislative journey to regulation."""
        print("\n" + "=" * 70)
        print("📜 LEGISLATIVE PROCESS SIMULATION")
        print("=" * 70)
        
        phases = [
            ("Committee Review", random.randint(3, 9), "Senate Commerce & House Energy & Commerce"),
            ("Markup & Amendments", random.randint(2, 6), "Committee members propose changes"),
            ("Floor Debate", random.randint(1, 4), "Full Senate/House debate and vote"),
            ("Conference Committee", random.randint(2, 8), "Resolve differences between chambers"),
            ("Presidential Signing", random.randint(1, 2), "President signs or vetoes")
        ]
        
        current_date = self.ban_start_date
        for phase, months, description in phases:
            phase_end = current_date + timedelta(days=months * 30.44)
            print(f"\n{phase}:")
            print(f"  Duration: ~{months} months")
            print(f"  Expected: {phase_end.strftime('%Y-%m-%d')}")
            print(f"  Activity: {description}")
            current_date = phase_end
        
        print(f"\n🎯 Expected regulation enactment: {self._estimate_regulation_date().strftime('%Y-%m-%d')}")
        print(f"   Total legislative timeline: ~{self.regulation_eta_months} months")
    
    def print_project_summary(self):
        """Print summary of all projects."""
        print("\n" + "=" * 70)
        print("PROJECT PORTFOLIO SUMMARY")
        print("=" * 70)
        
        status_counts = {}
        for status in ["pending", "under_construction", "halted", "completed"]:
            count = sum(1 for p in self.projects if p.status == status)
            if count > 0:
                status_counts[status] = count
        
        for status, count in status_counts.items():
            pct = count / len(self.projects) * 100
            print(f"{status.replace('_', ' ').title()}: {count} projects ({pct:.0f}%)")
        
        print("\nTop 5 largest projects by capacity:")
        sorted_projects = sorted(self.projects, key=lambda p: p.capacity_mw, reverse=True)
        for p in sorted_projects[:5]:
            print(f"  {p.name}: {p.capacity_mw} MW, {p.location}, status={p.status}")

def load_sample_projects() -> List[DataCenterProject]:
    """Generate realistic data center projects affected by the ban."""
    locations = [
        ("Northern Virginia", "USA", "AWS"),
        ("Silicon Valley", "USA", "Google"),
        ("Chicago", "USA", "Microsoft"),
        ("Amsterdam", "Netherlands", "Google"),
        ("Dublin", "Ireland", "AWS"),
        ("Singapore", "Singapore", "AWS"),
        ("Tokyo", "Japan", "Microsoft"),
        ("Frankfurt", "Germany", "Google"),
        ("London", "UK", "AWS"),
        ("Sydney", "Australia", "Microsoft")
    ]
    
    # Create projects with varying sizes and timelines
    projects = []
    base_date = datetime(2025, 1, 1)
    
    for i, (city, country, employer) in enumerate(locations * 3):  # 30 projects total
        # Mix of pending and under_construction
        if i < 15:
            status = "pending"
            start_offset = random.randint(60, 180)  # start in future
        else:
            status = "under_construction"
            start_offset = random.randint(-120, 30)  # already started or starting soon
        
        start_date = base_date + timedelta(days=start_offset)
        duration_months = random.randint(18, 36)
        completion_date = start_date + timedelta(days=duration_months * 30.44)
        
        # Capacity based on employer (hypothetical)
        capacity_ranges = {
            "AWS": (80, 150),
            "Google": (100, 200),
            "Microsoft": (60, 120)
        }
        min_cap, max_cap = capacity_ranges.get(employer, (50, 100))
        capacity = random.randint(min_cap, max_cap)
        
        # Cost ~$10M per MW (typical hyperscale)
        cost = capacity * random.uniform(8, 12)
        
        project = DataCenterProject(
            name=f"{employer} DC {city} {random.randint(1, 5)}",
            location=f"{city}, {country}",
            capacity_mw=capacity,
            cost_million=cost,
            start_date=start_date,
            planned_completion=completion_date,
            status=status,
            employer=employer
        )
        projects.append(project)
    
    return projects

def main():
    random.seed(42)  # Reproducible simulation
    
    print("🏛️  BERNIE SANDERS & AOC DATA CENTER BAN IMPACT ANALYSIS")
    print("Companion Legislation: Halt construction until AI regulation passes")
    print()
    
    # Initialize simulator
    simulator = ConstructionBanSimulator()
    
    # Load sample projects (30 data centers worldwide)
    projects = load_sample_projects()
    for p in projects:
        simulator.add_project(p)
    
    simulator.print_project_summary()
    
    # Apply the ban
    simulator.apply_ban()
    
    # Calculate impact
    impact = simulator.calculate_economic_impact()
    
    print("\n" + "=" * 70)
    print("ECONOMIC IMPACT ASSESSMENT")
    print("=" * 70)
    print(f"Projects halted: {impact['projects_halted']}")
    print(f"Total capacity delayed: {impact['total_capacity_mw']:.0f} MW")
    print(f"Construction investment delayed: ${impact['total_construction_cost_million']:,.0f}M")
    print(f"Average cost per MW: ${impact['avg_cost_per_mw']:,.0f}")
    print()
    print("👷 JOB IMPACT:")
    print(f"  Construction jobs lost: {impact['construction_jobs_lost']:,}")
    print(f"  Annual payroll loss: ${impact['construction_salary_loss_yearly']:,}")
    print(f"  Long-term ops jobs lost: {impact['operational_jobs_lost']:,}")
    print(f"  Annual ops payroll loss: ${impact['operational_salary_loss_yearly']:,}")
    print()
    print("⚡ ENERGY & AI IMPACT:")
    print(f"  AI compute capacity delayed: {impact['ai_compute_capacity_delayed_mw']:.0f} MW")
    print(f"  This equals ~{impact['ai_compute_capacity_delayed_mw'] * 1000:,} GPUs of compute power")
    print()
    
    # Simulate legislative timeline
    simulator.simulate_legislative_process()
    
    print("\n" + "=" * 70)
    print("POLICY IMPLICATIONS")
    print("=" * 70)
    print("💡 PRO-BAN ARGUMENTS:")
    print("  - Forces comprehensive AI regulation before infrastructure scales")
    print("  - Gives Congress time to address energy consumption, monopolies")
    print("  - Environmental pause to assess carbon footprint")
    print("  - Labor leverage for unionization and local hiring requirements")
    print()
    print("⚠️  ANTI-BAN ARGUMENTS:")
    print("  - US loses competitive edge in AI infrastructure")
    print("  - Construction jobs lost, especially in rural areas")
    print("  - Hyperscalers build overseas instead (Ireland, Netherlands)")
    print("  - AI startups can't scale without cloud capacity")
    print("  - Tax revenue lost from construction activity and future operations")
    print()
    print("🎯 KEY QUESTION:")
    print("   Does the regulatory benefit outweigh the economic and strategic cost?")
    print("=" * 70)

if __name__ == "__main__":
    main()
```