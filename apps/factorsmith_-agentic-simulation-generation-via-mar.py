```python
#!/usr/bin/env python3
"""
FactorSmith Demo: Agentic Simulation Generation via MDP Decomposition
Shows Planner-Designer-Critic loop generating a simple simulation from NL spec.
"""

import json, re, random
from dataclasses import dataclass
from typing import List, Dict, Tuple

# ==================== Domain: Simple Economic Simulation ====================

@dataclass
class SimulationState:
    time: int
    population: int
    capital: float
    resources: float
    gdp: float

class Simulation:
    def __init__(self, rules: Dict, initial: Dict):
        self.rules = rules
        self.state = SimulationState(**initial)
        self.history = []
        self.time_limit = rules.get('time_limit', 100)
    
    def step(self, action: str = "gather") -> Tuple[bool, str]:
        """Execute one simulation step."""
        if self.state.time >= self.time_limit:
            return False, "Simulation complete"
        
        # Simple economy model
        prod_rate = self.rules['production_rate']
        consume_rate = self.rules['consumption_rate']
        
        if action == "gather":
            gathered = self.state.resources * prod_rate * (self.state.population / 1000)
            self.state.capital += gathered * self.rules['capital_value']
            self.state.resources -= gathered
        elif action == "invest":
            if self.state.capital >= self.rules['investment_cost']:
                self.state.capital -= self.rules['investment_cost']
                self.state.resources += self.rules['investment_return']
        
        # Population growth
        self.state.population += int(self.state.population * self.rules['growth_rate'])
        
        # GDP calculation
        self.state.gdp = self.state.capital * self.state.population / 1000000
        
        self.state.time += 1
        self.history.append({
            'time': self.state.time,
            'action': action,
            'population': self.state.population,
            'capital': round(self.state.capital, 2),
            'resources': round(self.state.resources, 2),
            'gdp': round(self.state.gdp, 2)
        })
        return True, f"t={self.state.time}: GDP=${self.state.gdp:.2f}B, Pop={self.state.population:,}"
    
    def get_summary(self) -> Dict:
        if not self.history:
            return {'error': 'No steps executed'}
        final = self.history[-1]
        peak_gdp = max(h['gdp'] for h in self.history)
        return {
            'total_steps': len(self.history),
            'final_gdp': final['gdp'],
            'final_population': final['population'],
            'final_resources': final['resources'],
            'peak_gdp': peak_gdp,
            'sustainability_score': final['resources'] / self.rules['initial_resources']
        }

# ==================== Planner: Decompose Spec into MDP ====================

class Planner:
    def create_plan(self, spec: str) -> Dict:
        """Parse natural language spec and create simulation configuration."""
        print("🧠 PLANNER: Analyzing specification...")
        
        # Very simple parsing - demo purposes
        if "economic" in spec.lower() or "economy" in spec.lower():
            plan = {
                'type': 'economic_growth',
                'entities': ['population', 'capital', 'resources'],
                'actions': ['gather', 'invest', 'grow'],
                'objective': 'maximize_gdp',
                'constraints': ['resources_finite', 'population_growth'],
                'time_horizon': 50
            }
        elif "ecology" in spec.lower() or "environment" in spec.lower():
            plan = {
                'type': 'ecological',
                'entities': ['biomass', 'water', 'pollution'],
                'actions': ['protect', 'extract', 'clean'],
                'objective': 'balance_growth_sustainability',
                'constraints': ['carrying_capacity'],
                'time_horizon': 100
            }
        else:
            plan = {
                'type': 'generic',
                'entities': ['state'],
                'actions': ['advance'],
                'objective': 'reach_goal',
                'constraints': [],
                'time_horizon': 20
            }
        
        print(f"   ✓ Created plan: {plan['type']} simulation")
        print(f"     Entities: {', '.join(plan['entities'])}")
        print(f"     Actions: {', '.join(plan['actions'])}")
        return plan

# ==================== Designer: Generate Simulation Code ====================

class Designer:
    def design_simulation(self, plan: Dict) -> Simulation:
        """Turn plan into executable simulation."""
        print("\n🎨 DESIGNER: Building simulation components...")
        
        # Design simulation rules based on plan type
        if plan['type'] == 'economic_growth':
            rules = {
                'production_rate': 0.05,
                'consumption_rate': 0.02,
                'growth_rate': 0.01,
                'capital_value': 1.2,
                'investment_cost': 1000,
                'investment_return': 500,
                'initial_population': 10000,
                'initial_capital': 100000,
                'initial_resources': 1000000,
                'time_limit': plan['time_horizon']
            }
            initial = {
                'time': 0,
                'population': rules['initial_population'],
                'capital': rules['initial_capital'],
                'resources': rules['initial_resources'],
                'gdp': 0
            }
        elif plan['type'] == 'ecological':
            rules = {
                'production_rate': 0.02,
                'consumption_rate': 0.01,
                'growth_rate': 0.005,
                'capital_value': 1.0,
                'investment_cost': 500,
                'investment_return': 200,
                'initial_population': 5000,
                'initial_capital': 50000,
                'initial_resources': 500000,
                'time_limit': plan['time_horizon']
            }
            initial = {
                'time': 0,
                'population': rules['initial_population'],
                'capital': rules['initial_capital'],
                'resources': rules['initial_resources'],
                'gdp': 0
            }
        else:
            rules = {
                'time_limit': plan['time_horizon'],
                'initial_state': 0
            }
            initial = {'time': 0, 'state': 0}
        
        sim = Simulation(rules, initial)
        print(f"   ✓ Simulation instantiated with {len(rules)} parameters")
        return sim

# ==================== Critic: Test and Refine ====================

class Critic:
    def evaluate(self, sim: Simulation, plan: Dict) -> Tuple[float, str, Dict]:
        """Run simulation and evaluate against objectives."""
        print("\n🔍 CRITIC: Running simulation and evaluating...")
        
        # Simple policy: alternate gather/invest
        actions = ['gather', 'invest', 'gather', 'gather', 'invest']
        success = True
        steps = 0
        
        while success and steps < plan['time_horizon']:
            action = actions[steps % len(actions)]
            success, msg = sim.step(action)
            steps += 1
        
        summary = sim.get_summary()
        
        # Scoring based on plan objective
        if 'error' in summary:
            score = 0.0
            feedback = "Simulation failed to run"
        else:
            if plan['objective'] == 'maximize_gdp':
                score = summary['final_gdp'] / (summary['peak_gdp'] + 1)
                sustainability = summary['sustainability_score']
                if sustainability < 0.1:
                    score *= 0.5
                    feedback = f"GDP achieved but resources depleted (score={score:.3f})"
                else:
                    feedback = f"Good GDP growth with sustainable resources (score={score:.3f})"
            else:
                score = 0.6  # Default
                feedback = "Generic evaluation passed"
        
        print(f"   ✓ Evaluation complete: score={score:.3f}")
        print(f"     {feedback}")
        return score, feedback, summary

# ==================== FactorSmith: Main Orchestrator ====================

class FactorSmith:
    def __init__(self):
        self.planner = Planner()
        self.designer = Designer()
        self.critic = Critic()
        self.iteration_history = []
    
    def generate_simulation(self, spec: str, max_iterations: int = 3) -> Simulation:
        """Full factor generation loop."""
        print("=" * 70)
        print("FactorSmith: Agentic Simulation Generation via MDP Decomposition")
        print("=" * 70)
        print(f"Specification: '{spec}'")
        print()
        
        best_sim = None
        best_score = -1
        
        for iteration in range(max_iterations):
            print(f"\n{'='*70}")
            print(f"ITERATION {iteration + 1}/{max_iterations}")
            print(f"{'='*70}")
            
            # PLANNER: create plan
            plan = self.planner.create_plan(spec)
            
            # DESIGNER: build simulation from plan
            sim = self.designer.design_simulation(plan)
            
            # CRITIC: evaluate
            score, feedback, summary = self.critic.evaluate(sim, plan)
            
            # Record iteration
            self.iteration_history.append({
                'iteration': iteration + 1,
                'plan_type': plan['type'],
                'score': score,
                'feedback': feedback,
                'summary': summary
            })
            
            # Update best
            if score > best_score:
                best_score = score
                best_sim = sim
                print(f"\n🏆 New best simulation (score: {score:.3f})")
            
            # If score is good enough, stop early
            if score >= 0.8:
                print("\n✅ Target score reached. Stopping iterations.")
                break
        
        # Final report
        print("\n" + "=" * 70)
        print("FACTORSMITH COMPLETE")
        print("=" * 70)
        print(f"Best score: {best_score:.3f}")
        print(f"Simulation steps generated: {len(best_sim.history) if best_sim else 0}")
        print("\nIteration history:")
        for rec in self.iteration_history:
            print(f"  {rec['iteration']}. {rec['plan_type']}: score={rec['score']:.3f} - {rec['feedback']}")
        
        return best_sim

# ==================== Demo ====================

def main():
    # Example natural language specification
    spec = "Create an economic simulation of a growing market with finite resources"
    
    smith = FactorSmith()
    simulation = smith.generate_simulation(spec)
    
    if simulation and simulation.history:
        print("\nSample output (first 5 steps):")
        for i, step in enumerate(simulation.history[:5]):
            print(f"  {step}")
        print(f"  ... ({len(simulation.history)} total steps)")
    
    print("\n" + "=" * 70)
    print("FactorSmith demonstrates MDP decomposition:")
    print("  Planner: breaks NL spec into structured plan")
    print("  Designer: translates plan into executable simulation")
    print("  Critic: evaluates and enables refinement loop")
    print("Result: domain-specialized simulation generation")
    print("=" * 70)

if __name__ == "__main__":
    main()
```