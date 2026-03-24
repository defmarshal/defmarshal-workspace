```python
#!/usr/bin/env python3
import random
import re
from difflib import SequenceMatcher

# Target topic for Generative Engine Optimization
TARGET_TOPIC = "sustainable urban gardening"
TARGET_KEYWORDS = ["sustainable", "urban", "gardening", "eco-friendly", "city farming"]

def fitness(content):
    """Score content relevance to target topic."""
    text = content.lower()
    # Keyword density (normalized by word count)
    kw_density = sum(text.count(kw) for kw in TARGET_KEYWORDS) / max(1, len(text.split()))
    # Semantic similarity proxy (string level)
    similarity = SequenceMatcher(None, text, TARGET_TOPIC).ratio()
    return 0.7 * kw_density + 0.3 * similarity

def mutate(content):
    """Apply a random content mutation."""
    words = content.split()
    if not words:
        return content
    ops = ['insert', 'replace', 'delete', 'swap']
    op = random.choice(ops)
    
    if op == 'insert' and random.random() < 0.6:
        kw = random.choice(TARGET_KEYWORDS)
        pos = random.randint(0, len(words))
        words.insert(pos, kw)
    elif op == 'replace':
        pos = random.randint(0, len(words)-1)
        words[pos] = random.choice(TARGET_KEYWORDS)
    elif op == 'delete' and len(words) > 2:
        pos = random.randint(0, len(words)-1)
        words.pop(pos)
    elif op == 'swap' and len(words) > 1:
        i = random.randint(0, len(words)-2)
        words[i], words[i+1] = words[i+1], words[i]
    
    return ' '.join(words)

def evolve(initial, generations=10, pop_size=5):
    """Run evolutionary loop."""
    population = [initial]
    for gen in range(1, generations+1):
        # Select best from current population (elitism)
        parent = max(population, key=fitness)
        # Generate new population via mutations of parent
        population = [parent] + [mutate(parent) for _ in range(pop_size-1)]
        best_score = fitness(parent)
        print(f"Gen {gen}: best fitness={best_score:.4f} | snippet: '{parent[:40]}...'")
    return max(population, key=fitness)

def main():
    # Initial seed content (suboptimal)
    seed = (
        "Urban areas have many problems like pollution and缺少 green spaces. "
        "People want to grow food but often have little room. "
        "This post covers city garden ideas."
    )
    print("Initial seed content:")
    print(seed)
    print(f"Initial fitness: {fitness(seed):.4f}\n")
    
    print("Starting AgenticGEO evolution...")
    best = evolve(seed, generations=8, pop_size=4)
    
    print("\n" + "="*60)
    print("Optimized content for generative engines:")
    print(best)
    print(f"Final fitness: {fitness(best):.4f}")

if __name__ == "__main__":
    main()
```