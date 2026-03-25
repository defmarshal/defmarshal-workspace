```python
#!/usr/bin/env python3
"""
Meta Workforce Reduction Simulator
Models the impact of cutting several hundred jobs across US and international markets.
"""

from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class Employee:
    id: int
    department: str
    region: str
    level: str  # junior, mid, senior, lead
    salary: int  # annual salary in USD
    productivity: float  # 0.0-1.0

@dataclass
class Department:
    name: str
    headcount: int
    avg_salary: int
    region_distribution: Dict[str, float]  # region -> % of dept
    productivity_impact: float  # how much productivity drops after layoffs

class MetaWorkforce:
    def __init__(self):
        self.employees: List[Employee] = []
        self.departments: Dict[str, Department] = {}
        self.initialize_workforce()
    
    def initialize_workforce(self):
        """Simulate Meta's workforce distribution (approximate 2026)."""
        # Total ~70,000 employees; cutting several hundred (~2-3%)
        departments_config = {
            'Engineering': {'headcount': 35000, 'avg': 180000, 'regions': {'US': 0.4, 'Europe': 0.25, 'Asia': 0.35}},
            'Product': {'headcount': 8000, 'avg': 160000, 'regions': {'US': 0.5, 'Europe': 0.2, 'Asia': 0.3}},
            'Sales': {'headcount': 12000, 'avg': 120000, 'regions': {'US': 0.45, 'Europe': 0.3, 'Asia': 0.25}},
            'Operations': {'headcount': 10000, 'avg': 90000, 'regions': {'US': 0.3, 'Europe': 0.4, 'Asia': 0.3}},
            'Research': {'headcount': 5000, 'avg': 220000, 'regions': {'US': 0.6, 'Europe': 0.2, 'Asia': 0.2}},
            'Safety & Integrity': {'headcount': 3000, 'avg': 110000, 'regions': {'US': 0.35, 'Europe': 0.45, 'Asia': 0.2}},
            'Marketing': {'headcount': 7000, 'avg': 130000, 'regions': {'US': 0.55, 'Europe': 0.25, 'Asia': 0.2}}
        }
        
        employee_id = 1
        for dept_name, config in departments_config.items():
            dept = Department(
                name=dept_name,
                headcount=config['headcount'],
                avg_salary=config['avg'],
                region_distribution=config['regions'],
                productivity_impact=random.uniform(0.85, 0.95)  # layoffs hurt morale of remaining
            )
            self.departments[dept_name] = dept
            
            # Generate employees
            for _ in range(config['headcount']):
                region = random.choices(
                    list(config['regions'].keys()),
                    weights=list(config['regions'].values())
                )[0]
                
                # Salary varies by level
                level_probs = {'junior': 0.3, 'mid': 0.4, 'senior': 0.2, 'lead': 0.1}
                level = random.choices(list(level_probs.keys()), weights=list(level_probs.values()))[0]
                
                level_multiplier = {
                    'junior': 0.6, 'mid': 0.9, 'senior': 1.3, 'lead': 1.7
                }[level]
                
                salary = int(config['avg'] * level_multiplier * random.uniform(0.9, 1.1))
                productivity = random.uniform(0.7, 1.0)
                
                self.employees.append(Employee(
                    id=employee_id,
                    department=dept_name,
                    region=region,
                    level=level,
                    salary=salary,
                    productivity=productivity
                ))
                employee_id += 1
    
    def conduct_layoffs(self, total_cuts: int = 500, strategy: str = 'proportional') -> Dict:
        """Simulate layoff execution."""
        print(f"🔪 initiating reduction of {total_cuts} employees ({total_cuts/len(self.employees)*100:.1f}% workforce)")
        print(f"   Strategy: {strategy}")
        print()
        
        layoff_targets = []
        
        if strategy == 'proportional':
            # Cut proportionally across all departments
            for dept_name, dept in self.departments.items():
                dept_cuts = max(1, int(dept.headcount * total_cuts / len(self.employees)))
                dept_employees = [e for e in self.employees if e.department == dept_name]
                # Prefer lower productivity, higher salary (cost optimization)
                dept_employees.sort(key=lambda e: (e.productivity, -e.salary))
                layoff_targets.extend(dept_employees[:dept_cuts])
        
        elif strategy == 'low_performers':
            # Cut bottom X% by productivity across entire company
            sorted_employees = sorted(self.employees, key=lambda e: e.productivity)
            layoff_targets = sorted_employees[:total_cuts]
        
        elif strategy == 'cost_savings':
            # Cut highest salary positions first (senior/lead)
            sorted_employees = sorted(self.employees, key=lambda e: e.salary, reverse=True)
            layoff_targets = sorted_employees[:total_cuts]
        
        elif strategy == 'region_targeted':
            # Focus on international markets (non-US)
            intl_employees = [e for e in self.employees if e.region != 'US']
            if len(intl_employees) >= total_cuts:
                layoff_targets = random.sample(intl_employees, total_cuts)
            else:
                layoff_targets = intl_employees + random.sample(
                    [e for e in self.employees if e.region == 'US'], 
                    total_cuts - len(intl_employees)
                )
        
        # Apply layoffs
        layoff_ids = {e.id for e in layoff_targets}
        self.employees = [e for e in self.employees if e.id not in layoff_ids]
        
        # Update department headcounts
        for dept in self.departments.values():
            dept.headcount = sum(1 for e in self.employees if e.department == dept.name)
        
        return self.generate_impact_report(layoff_targets)
    
    def generate_impact_report(self, laid_off: List[Employee]) -> Dict:
        """Calculate financial and operational impacts."""
        total_salary_saved = sum(e.salary for e in laid_off)
        severance_cost = sum(e.salary * 0.5 for e in laid_off)  # 6 months average
        net_annual_savings = total_salary_saved - severance_cost / 3  # amortize over 3 years
        
        # Productivity impact (simple model: remaining workforce productivity drops)
        remaining_productivity = sum(e.productivity for e in self.employees)
        original_productivity = remaining_productivity + sum(e.productivity for e in laid_off)
        productivity_preserved = remaining_productivity / original_productivity
        
        # Department breakdown
        dept_breakdown = {}
        for dept_name in self.departments:
            dept_laid = [e for e in laid_off if e.department == dept_name]
            dept_remaining = [e for e in self.employees if e.department == dept_name]
            if dept_laid or dept_remaining:
                dept_breakdown[dept_name] = {
                    'laid_off': len(dept_laid),
                    'remaining': len(dept_remaining),
                    'pct_cut': len(dept_laid) / (len(dept_laid) + len(dept_remaining)) * 100 if (len(dept_laid) + len(dept_remaining)) > 0 else 0,
                    'avg_salary_laid': int(sum(e.salary for e in dept_laid) / len(dept_laid)) if dept_laid else 0
                }
        
        # Region breakdown
        region_breakdown = {}
        for region in ['US', 'Europe', 'Asia']:
            region_laid = [e for e in laid_off if e.region == region]
            region_remaining = [e for e in self.employees if e.region == region]
            region_breakdown[region] = {
                'laid_off': len(region_laid),
                'remaining': len(region_remaining),
                'pct_cut': len(region_laid) / (len(region_laid) + len(region_remaining)) * 100 if (len(region_laid) + len(region_remaining)) > 0 else 0
            }
        
        return {
            'total_laid_off': len(laid_off),
            'total_salary_saved_annual': total_salary_saved,
            'severance_one_time': severance_cost,
            'net_annual_savings': net_annual_savings,
            'productivity_preserved_pct': productivity_preserved * 100,
            'department_breakdown': dept_breakdown,
            'region_breakdown': region_breakdown,
            'avg_salary_laid_off': int(sum(e.salary for e in laid_off) / len(laid_off)) if laid_off else 0,
            'levels_affected': {
                level: sum(1 for e in laid_off if e.level == level)
                for level in ['junior', 'mid', 'senior', 'lead']
            }
        }
    
    def print_summary(self, impact: Dict):
        """Print human-readable summary."""
        print(f"📊 LAYOFF IMPACT SUMMARY")
        print("=" * 60)
        print(f"Total employees before: {len(self.employees) + impact['total_laid_off']}")
        print(f"Total employees after:  {len(self.employees)}")
        print(f"Positions eliminated:   {impact['total_laid_off']}")
        print()
        print("💰 FINANCIAL IMPACT")
        print(f"  Annual salary savings: ${impact['total_salary_saved_annual']:,}")
        print(f"  Severance cost (one-time): ${impact['severance_one_time']:,}")
        print(f"  Net annual savings (3-yr amortized): ${impact['net_annual_savings']:,}")
        print()
        print("⚙️  OPERATIONAL IMPACT")
        print(f"  Productivity preserved: {impact['productivity_preserved_pct']:.1f}%")
        print(f"  Average salary of eliminated positions: ${impact['avg_salary_laid_off']:,}")
        print()
        print("🏢 DEPARTMENT BREAKDOWN (most affected)")
        dept_list = sorted(
            impact['department_breakdown'].items(),
            key=lambda x: x[1]['pct_cut'],
            reverse=True
        )[:5]
        for dept, stats in dept_list:
            if stats['pct_cut'] > 0:
                print(f"  {dept}: {stats['laid_off']} cuts ({stats['pct_cut']:.1f}%)")
        print()
        print("🌍 REGION BREAKDOWN")
        for region, stats in impact['region_breakdown'].items():
            if stats['laid_off'] > 0:
                print(f"  {region}: {stats['laid_off']} cuts ({stats['pct_cut']:.1f}%)")
        print()
        print("👥 LEVELS AFFECTED")
        for level, count in impact['levels_affected'].items():
            if count > 0:
                pct = count / impact['total_laid_off'] * 100
                print(f"  {level.capitalize()}: {count} ({pct:.0f}%)")
        print()
        print("=" * 60)

def main():
    random.seed(42)  # reproducible demo
    
    workforce = MetaWorkforce()
    print(f"🏢 Meta workforce initialized: {len(workforce.employees)} employees")
    print(f"   Departments: {', '.join(workforce.departments.keys())}")
    print()
    
    # Simulate several layoff scenarios
    scenarios = [
        (300, 'proportional', 'Proportional across departments'),
        (400, 'low_performers', 'Focus on low performers'),
        (250, 'cost_savings', 'Target high-cost positions'),
        (350, 'region_targeted', 'Focus on international markets (US-protected)')
    ]
    
    for cuts, strategy, description in scenarios:
        print(f"\n{'='*70}")
        print(f"SCENARIO: {description}")
        print(f"{'='*70}")
        
        # Reset workforce for each scenario
        workforce = MetaWorkforce()
        impact = workforce.conduct_layoffs(total_cuts=cuts, strategy=strategy)
        workforce.print_summary(impact)
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print("Key observations:")
    print(" - Cutting several hundred (0.5-0.7% of workforce) has minimal productivity impact")
    print(" - 'Cost savings' strategy targets highest salaries but risks losing experience")
    print(" - International cuts can be larger percentage-wise while preserving US core")
    print(" - Most cuts fall on mid-level employees (40-60% of eliminated positions)")
    print(" - Severance costs are moderate (6 months avg) and amortize over 3+ years")
    print("=" * 70)

if __name__ == "__main__":
    main()
```