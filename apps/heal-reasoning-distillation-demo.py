#!/usr/bin/env python3
"""
HEAL Concept Demo: Hindsight Entropy-Assisted Learning for Reasoning Distillation

This script demonstrates the key idea behind HEAL: using entropy of reasoning chains
to identify the most informative examples for distilling a large teacher model into a
smaller student model.

Core concept:
- Teacher model generates multiple reasoning chains for a problem
- Each chain has a correctness label (correct/incorrect)
- Entropy measures uncertainty across chains for a given problem
- High-entropy problems are more informative for training the student
- HEAL selects these high-entropy examples to maximize distillation efficiency

Author: dev-agent
Date: 2026-03-13
"""

import random
import math
from typing import List, Tuple
import matplotlib.pyplot as plt

# Simulated data: for each problem, we have multiple reasoning chains with correctness
def generate_synthetic_data(num_problems: int = 50, chains_per_problem: int = 5) -> List[dict]:
    """Generate synthetic reasoning chains with varying difficulty."""
    data = []
    for pid in range(num_problems):
        # Randomly assign problem difficulty (easy, medium, hard)
        difficulty = random.choice(['easy', 'medium', 'hard'])
        if difficulty == 'easy':
            correct_prob = 0.9  # Teacher gets it right most of the time
        elif difficulty == 'medium':
            correct_prob = 0.6
        else:
            correct_prob = 0.3  # Hard problems: teacher is often wrong
        
        chains = []
        for cid in range(chains_per_problem):
            is_correct = random.random() < correct_prob
            chains.append({
                'problem_id': pid,
                'chain_id': cid,
                'correct': is_correct,
                # Simulate confidence: correct chains tend to have higher confidence
                'confidence': random.betavariate(2, 1) if is_correct else random.betavariate(1, 2)
            })
        data.append({'problem_id': pid, 'difficulty': difficulty, 'chains': chains})
    return data

def calculate_entropy(chains: List[dict]) -> float:
    """Compute binary entropy based on proportion of correct chains."""
    n = len(chains)
    if n == 0:
        return 0.0
    correct_count = sum(1 for c in chains if c['correct'])
    p = correct_count / n
    # Avoid log(0)
    p = max(min(p, 0.9999), 0.0001)
    entropy = -p * math.log2(p) - (1-p) * math.log2(1-p)
    return entropy

def select_heal_examples(data: List[dict], top_k: float = 0.3) -> List[dict]:
    """Select top-k highest entropy problems for distillation (HEAL selection)."""
    entropies = []
    for problem in data:
        entropy = calculate_entropy(problem['chains'])
        entropies.append((problem['problem_id'], entropy, problem))
    # Sort by entropy descending
    entropies.sort(key=lambda x: x[1], reverse=True)
    # Take top_k fraction
    n_select = max(1, int(len(data) * top_k))
    selected = [item[2] for item in entropies[:n_select]]
    return selected, [item[1] for item in entropies[:n_select]]

def baseline_random_selection(data: List[dict], seed: int = 42) -> List[dict]:
    """Select random subset of problems (baseline)."""
    random.seed(seed)
    selected = random.sample(data, k=max(1, int(len(data) * 0.3)))
    return selected

def simulate_distillation_gain(selected_problems: List[dict]) -> float:
    """Simulate student model performance gain based on selected examples.
    In this simplified simulation, we assume the student learns from the *distribution* 
    of correctness. High-entropy examples (mixed correct/incorrect) force the student
    to learn more nuanced representations, potentially leading to better generalization.
    
    Here we simply return the base accuracy of the selected set; in reality HEAL would
    show improved downstream task accuracy beyond this baseline."""
    total_correct = 0
    total_examples = 0
    for problem in selected_problems:
        chains = problem['chains']
        for chain in chains:
            if chain['correct']:
                total_correct += 1
            total_examples += 1
    accuracy = total_correct / total_examples if total_examples > 0 else 0
    return accuracy

def main():
    random.seed(42)
    
    print("=== HEAL: Hindsight Entropy-Assisted Learning Demo ===\n")
    
    # Generate synthetic data
    data = generate_synthetic_data(num_problems=100, chains_per_problem=5)
    print(f"Generated {len(data)} problems with 5 reasoning chains each.")
    
    # Count difficulties
    difficulties = {'easy': 0, 'medium': 0, 'hard': 0}
    for p in data:
        difficulties[p['difficulty']] += 1
    print(f"Difficulty distribution: {difficulties}\n")
    
    # HEAL selection
    heal_selected, heal_entropies = select_heal_examples(data, top_k=0.3)
    heal_gain = simulate_distillation_gain(heal_selected)
    print(f"HEAL selected {len(heal_selected)} problems (top 30% entropy).")
    print(f"  Average entropy of selected: {sum(heal_entropies)/len(heal_entropies):.3f}")
    print(f"  Simulated student accuracy: {heal_gain:.2%}\n")
    
    # Baseline random selection
    random_selected = baseline_random_selection(data)
    random_gain = simulate_distillation_gain(random_selected)
    print(f"Random baseline selected {len(random_selected)} problems.")
    print(f"  Simulated student accuracy: {random_gain:.2%}\n")
    
    # Compare
    improvement = (heal_gain - random_gain) / random_gain if random_gain > 0 else 0
    print(f"HEAL improvement over random: {improvement:.2%}")
    
    # Visualize entropy distribution
    all_entropies = [calculate_entropy(p['chains']) for p in data]
    selected_entropies = [calculate_entropy(p['chains']) for p in heal_selected]
    
    plt.figure(figsize=(10, 5))
    plt.hist(all_entropies, bins=20, alpha=0.5, label='All problems', color='gray')
    plt.hist(selected_entropies, bins=15, alpha=0.7, label='HEAL selected (high entropy)', color='orange')
    plt.xlabel('Hindsight Entropy (bits)')
    plt.ylabel('Number of Problems')
    plt.title('HEAL: Selects High-Entropy Reasoning Chains for Distillation')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Print a sample of selected problems
    print("\n--- Sample HEAL-selected problems ---")
    for i, prob in enumerate(heal_selected[:3]):
        chains = prob['chains']
        correct_count = sum(1 for c in chains if c['correct'])
        print(f"Problem {prob['problem_id']} ({prob['difficulty']}): {correct_count}/{len(chains)} correct chains, entropy={calculate_entropy(chains):.3f}")

if __name__ == "__main__":
    main()
