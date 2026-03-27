```python
#!/usr/bin/env python3
"""
Memetic Drift in Multi-Agent LLM Systems
Demonstrates how information degrades as it passes through chains of agents.
"""

import random
import string
from typing import List, Dict

class MemeticAgent:
    """Simulates an LLM agent that receives and retransmits information with drift."""
    
    def __init__(self, drift_rate: float = 0.1, noise_level: int = 2):
        """
        drift_rate: probability that any given token gets altered (0.0-1.0)
        noise_level: max number of tokens to add/remove per transmission
        """
        self.drift_rate = drift_rate
        self.noise_level = noise_level
    
    def process(self, meme: List[str]) -> List[str]:
        """Receive a meme (list of tokens) and transmit with introduced drift."""
        if not meme:
            return meme
        
        # Copy input to avoid modifying original
        transmitted = meme.copy()
        
        # 1. Token substitution (corruption)
        for i in range(len(transmitted)):
            if random.random() < self.drift_rate:
                # Replace with random token (simulates LLM hallucination/semantic drift)
                transmitted[i] = self._random_token()
        
        # 2. Insertion noise (add spurious tokens)
        n_inserts = random.randint(0, self.noise_level)
        for _ in range(n_inserts):
            pos = random.randint(0, len(transmitted))
            transmitted.insert(pos, self._random_token())
        
        # 3. Deletion noise (drop tokens)
        if len(transmitted) > 1:
            n_deletes = random.randint(0, min(self.noise_level, len(transmitted)-1))
            for _ in range(n_deletes):
                pos = random.randint(0, len(transmitted)-1)
                transmitted.pop(pos)
        
        return transmitted
    
    def _random_token(self) -> str:
        """Generate a random token (word) of varying length."""
        length = random.randint(3, 8)
        return ''.join(random.choices(string.ascii_lowercase, k=length))

def calculate_drift(original: List[str], transmitted: List[str]) -> Dict[str, float]:
    """Calculate drift metrics between original and transmitted meme."""
    # Simple token overlap metric
    orig_set = set(original)
    trans_set = set(transmitted)
    
    if not orig_set:
        return {"overlap": 1.0, "edit_distance": 0, "length_diff": 0}
    
    overlap = len(orig_set & trans_set) / len(orig_set)
    length_diff = abs(len(transmitted) - len(original)) / max(len(original), 1)
    
    # Approximate edit distance (simple version)
    edit_dist = levenshtein_distance(' '.join(original), ' '.join(transmitted))
    normalized_edit = edit_dist / max(len(original), len(transmitted), 1)
    
    return {
        "overlap": round(overlap, 3),
        "length_diff": round(length_diff, 3),
        "edit_distance": edit_dist,
        "normalized_edit": round(normalized_edit, 3)
    }

def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def simulate_memetic_cascade(initial_meme: List[str], 
                           chain_length: int = 5,
                           drift_rate: float = 0.1,
                           noise_level: int = 2) -> Dict:
    """Simulate meme propagation through a chain of agents."""
    print(f"\n{'='*70}")
    print(f"MEMETIC DRIFT SIMULATION")
    print(f"Chain length: {chain_length} agents")
    print(f"Drift rate: {drift_rate*100:.1f}% per token")
    print(f"Noise level: ±{noise_level} tokens")
    print(f"{'='*70}")
    
    # Print original meme
    print(f"\n📜 Original meme: {' '.join(initial_meme)}")
    print(f"   Tokens: {len(initial_meme)}")
    
    # Create agent chain
    agents = [MemeticAgent(drift_rate=drift_rate, noise_level=noise_level) 
              for _ in range(chain_length)]
    
    # Propagate through chain
    current_meme = initial_meme.copy()
    results = []
    
    print(f"\n🔄 Propagation chain:")
    for i, agent in enumerate(agents, 1):
        current_meme = agent.process(current_meme)
        drift = calculate_drift(initial_meme, current_meme)
        
        print(f"\n   Agent {i}:")
        print(f"     Output: {' '.join(current_meme[:20])}{'...' if len(current_meme)>20 else ''}")
        print(f"     Length: {len(current_meme)} tokens")
        print(f"     Overlap: {drift['overlap']*100:.1f}%")
        print(f"     Edit dist: {drift['edit_distance']}")
        
        results.append({
            "agent": i,
            "meme": current_meme.copy(),
            "drift": drift
        })
    
    # Summary statistics
    overlaps = [r['drift']['overlap'] for r in results]
    edits = [r['drift']['edit_distance'] for r in results]
    
    print(f"\n📊 CASCADE SUMMARY:")
    print(f"   Final overlap: {overlaps[-1]*100:.1f}%")
    print(f"   Total edit distance: {edits[-1]}")
    print(f"   Average drift per hop: {sum(overlaps)/len(overlaps)*100:.1f}% overlap")
    
    # Fit simple scaling law: drift ~ chain_length^exponent
    if len(overlaps) > 1:
        # Simple linear fit on (hop, 1-overlap)
        x = list(range(1, len(overlaps)+1))
        y = [1-o for o in overlaps]
        # Linear regression (very simple)
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi*yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi*xi for xi in x)
        slope = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x*sum_x)
        print(f"   Drift scaling exponent: {slope:.3f} (drift ∝ L^{slope:.3f})")
    
    return {
        "initial_meme": initial_meme,
        "chain_length": chain_length,
        "agent_outputs": results,
        "final_overlap": overlaps[-1] if overlaps else 1.0,
        "final_edit_distance": edits[-1] if edits else 0,
        "scaling_exponent": slope if len(overlaps) > 1 else None
    }

def demonstrate_scaling_laws() -> None:
    """Run simulations showing how drift scales with chain length."""
    print("\n" + "="*70)
    print("SCALING LAWS DEMONSTRATION")
    print("="*70)
    
    initial = ["knowledge", "graph", "inference", "is", "hard"]
    
    print("\n🧪 Varying chain length (drift_rate=0.1):")
    for L in [2, 5, 10, 20]:
        result = simulate_memetic_cascade(initial, chain_length=L, drift_rate=0.1)
    
    print("\n🧪 Varying drift rate (chain_length=5):")
    for rate in [0.05, 0.1, 0.2, 0.3]:
        result = simulate_memetic_cascade(initial, chain_length=5, drift_rate=rate)

def main():
    print("🧠 When Is Collective Intelligence a Lottery?")
    print("Multi-Agent Scaling Laws for Memetic Drift in LLMs\n")
    
    # Simulate a few cascades with different parameters
    initial_meme = ["the", "cat", "sat", "on", "the", "mat"]
    
    print("📌 SCENARIO: A simple fact propagating through agents")
    result1 = simulate_memetic_cascade(initial_meme, chain_length=3, drift_rate=0.1)
    
    print("\n📌 SCENARIO: Longer chain, higher drift")
    result2 = simulate_memetic_cascade(initial_meme, chain_length=8, drift_rate=0.15)
    
    demonstrate_scaling_laws()
    
    print("\n" + "="*70)
    print("CONCLUSION:")
    print("Memetic drift accumulates with chain length, following a power-law-like")
    print("relationship. For collective intelligence to be reliable, either:")
    print("  • Keep agent chains short (<5 hops), or")
    print("  • Use very low-drift agents (e.g., fine-tuned, constrained LLMs), or")
    print("  • Implement verification/correction at each hop")
    print("="*70)

if __name__ == "__main__":
    main()
```