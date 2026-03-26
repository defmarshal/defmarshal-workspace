#!/usr/bin/env python3
"""
Intelligence Inertia: Physical Principles Demo
Based on arXiv:2603.22347v1 - Landauer's principle meets Fisher Information
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List

@dataclass
class PhysicalSystem:
    """Represents a simple memory system with thermodynamic constraints"""
    k: float = 1.38e-23  # Boltzmann constant (J/K)
    T: float = 300.0      # Temperature (Kelvin, ~27°C)
    state: int = 0        # Current binary state (0 or 1)
    energy: float = 0.0   # Current energy
    
    @property
    def landauer_cost(self) -> float:
        """Minimum energy to erase one bit (Landauer's principle)"""
        return self.k * self.T * np.log(2)  # ~2.87e-21 J at 300K
    
    def flip(self, target: int) -> float:
        """Flip state to target, return energy cost"""
        if self.state != target:
            # Energy cost at least Landauer limit (plus overhead)
            self.state = target
            self.energy += self.landauer_cost * np.random.uniform(1.0, 2.5)
            return self.energy
        return 0.0
    
    def fisher_information(self, p: float) -> float:
        """Fisher Information for Bernoulli parameter p"""
        if 0 < p < 1:
            return 1.0 / (p * (1 - p))
        return float('inf')

class IntelligentAgent:
    """Agent that adapts based on Fisher Information - lower inertia with higher FI"""
    def __init__(self, system: PhysicalSystem):
        self.system = system
        self.history = []
        self.inertia = 1.0  # Start with high inertia
        
    def observe(self, external_input: float) -> float:
        """Observe and potentially respond to change"""
        # Convert input to probability estimate
        p = 1.0 / (1.0 + np.exp(-external_input))  # sigmoid
        
        # Compute Fisher Information of observation
        fi = self.system.fisher_information(p)
        
        # Inertia inversely proportional to Fisher Information
        # High FI = precise observation = low inertia (easier to change)
        # Low FI = uncertain observation = high inertia (resist change)
        self.inertia = max(0.05, 1.0 / (1.0 + np.log1p(fi)))
        
        # Store observation
        self.history.append({
            'input': external_input,
            'fi': fi,
            'inertia': self.inertia,
            'system_state': self.system.state
        })
        
        return self.inertia
    
    def decide_flip(self, stimulus: float) -> bool:
        """Decide whether to flip system state based on stimulus and inertia"""
        current_inertia = self.history[-1]['inertia'] if self.history else 1.0
        
        # Stronger stimulus can overcome inertia
        threshold = current_inertia * 2.0
        should_flip = abs(stimulus) > threshold
        
        return should_flip

def simulate_intelligence_inertia(
    steps: int = 100,
    initial_temp: float = 300.0,
    noise_scale: float = 0.5
) -> dict:
    """Run simulation showing relationship between Fisher Information and inertia"""
    
    system = PhysicalSystem(T=initial_temp)
    agent = IntelligentAgent(system)
    
    states = []
    inertias = []
    fis = []
    energies = []
    
    for t in range(steps):
        # External stimulus that drifts slowly (Brownian motion)
        if t == 0:
            stimulus = np.random.choice([-2.0, 2.0])  # Initial push
        else:
            stimulus = states[-1]['stimulus'] + np.random.normal(0, noise_scale)
        
        # Agent observes
        inertia = agent.observe(stimulus)
        
        # Decide action
        if agent.decide_flip(stimulus):
            target = 1 if stimulus > 0 else 0
            cost = system.flip(target)
        else:
            cost = 0.0
        
        # Record
        state_data = {
            't': t,
            'stimulus': stimulus,
            'system_state': system.state,
            'inertia': inertia,
            'fi': agent.history[-1]['fi'],
            'energy': system.energy,
            'cost': cost
        }
        states.append(state_data)
        inertias.append(inertia)
        fis.append(agent.history[-1]['fi'])
        energies.append(system.energy)
    
    return {
        'states': states,
        'inertias': inertias,
        'fisher_info': fis,
        'energies': energies,
        'landauer_cost': system.landauer_cost,
        'final_state': system.state
    }

def print_simulation_summary(results: dict):
    """Print human-readable summary of simulation"""
    landauer = results['landauer_cost']
    total_energy = results['energies'][-1]
    states = results['states']
    
    # Count actual flips
    flips = sum(1 for i in range(1, len(states)) 
                if states[i]['system_state'] != states[i-1]['system_state'])
    
    print("="*60)
    print("🧠 INTELLIGENCE INERTIA SIMULATION")
    print("="*60)
    print(f"Landauer limit (kT ln2) at {300}K: {landauer:.3e} J")
    print(f"Total energy expended: {total_energy:.3e} J")
    print(f"Number of state flips: {flips}")
    print(f"Average cost per flip: {total_energy/max(1,flips):.3e} J")
    
    # Inertia-Fisher relationship
    inertias = results['inertias']
    fis = results['fisher_info']
    avg_inertia = np.mean(inertias)
    avg_fi = np.mean(fis)
    
    print(f"\n📊 Average metrics:")
    print(f"  Inertia: {avg_inertia:.3f} (lower = more adaptable)")
    print(f"  Fisher Information: {avg_fi:.1f} (higher = more precise)")
    print(f"  Correlation (FI vs 1/Inertia): {np.corrcoef(fis, [1/i for i in inertias])[0,1]:.3f}")
    
    print("\n💡 Principle demonstrated:")
    print("  Higher Fisher Information → Lower Inertia")
    print("  More precise observations reduce resistance to change")
    print("  Landauer's principle sets the minimum energy cost for any state update")

def plot_results(results: dict, save_path: str = None):
    """Simple visualization (requires matplotlib)"""
    try:
        import matplotlib.pyplot as plt
        
        states = results['states']
        t = [s['t'] for s in states]
        inertias = [s['inertia'] for s in states]
        fis = [s['fi'] for s in states]
        stimulus = [s['stimulus'] for s in states]
        
        fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        
        # Plot 1: Stimulus and system state
        ax1 = axes[0]
        ax1.plot(t, stimulus, 'r-', alpha=0.7, label='Stimulus')
        ax1.set_ylabel('Stimulus')
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        ax1_twin = ax1.twinx()
        ax1_twin.plot(t, [s['system_state'] for s in states], 'b-', label='System State')
        ax1_twin.set_ylabel('State (0/1)')
        ax1_twin.legend(loc='upper right')
        
        # Plot 2: Fisher Information
        ax2 = axes[1]
        ax2.plot(t, fis, 'g-', label='Fisher Information')
        ax2.set_ylabel('FI')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Inertia
        ax3 = axes[2]
        ax3.plot(t, inertias, 'm-', label='Intelligence Inertia')
        ax3.set_xlabel('Time Step')
        ax3.set_ylabel('Inertia')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=100)
        else:
            plt.show()
        plt.close()
    except ImportError:
        print("Matplotlib not available - skipping plots")

def main():
    """Demonstrate Intelligence Inertia principle"""
    print("🧠 Intelligence Inertia: Physical Principles and Applications")
    print("   Demonstrating Landauer's principle + Fisher Information")
    print("-" * 60)
    
    # Run simulation
    results = simulate_intelligence_inertia(
        steps=200,
        initial_temp=300.0,
        noise_scale=0.3
    )
    
    # Print summary
    print_simulation_summary(results)
    
    # Optional: generate plot
    try:
        plot_results(results)
        print("\n📈 Plot generated (if matplotlib available)")
    except:
        pass
    
    print("\n" + "="*60)
    print("✨ Key Insight:")
    print("   Intelligence Inertia = resistance to belief updating")
    print("   High Fisher Information → Precise observations → Lower inertia")
    print("   Landauer's principle: Every update has thermodynamic cost")
    print("   Optimal intelligence balances information gain vs. energy expenditure")

if __name__ == "__main__":
    main()
```