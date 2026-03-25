```python
#!/usr/bin/env python3
"""
AgenticGEO: Self-Evolving System for Generative Engine Optimization
Demo: Agents compete to optimize content for AI-driven search results.
"""

import random, string, hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Callable
from datetime import datetime

# Simulated generative search engine (black box)
class GenerativeSearchEngine:
    def __init__(self):
        self.query_log = []
    
    def rank(self, query: str, documents: List[str]) -> List[str]:
        """Simulate LLM-based ranking - prefers clarity, authority, structure."""
        scores = []
        for doc in documents:
            score = 0
            # Prefer authoritative language
            if any(word in doc.lower() for word in ['research', 'study', 'analysis', 'comprehensive']):
                score += 2
            # Prefer structured content (headings, lists)
            if doc.count('\n') > 5:
                score += 1
            # Prefer recent dates
            if '2025' in doc or '2026' in doc:
                score += 1
            # Penalize keyword stuffing
            words = doc.lower().split()
            if max(words.count(w) for w in set(words)) > 5:
                score -= 2
            scores.append(score + random.random() * 0.5)  # Add noise
        ranked = [doc for _, doc in sorted(zip(scores, documents), reverse=True)]
        return ranked[:3]

# Agent strategies for GEO optimization
@dataclass
class Agent:
    name: str
    generation: int
    fitness: float = 0.0
    strategies: Dict[str, float] = field(default_factory=dict)
    
    def optimize(self, content: str, query: str) -> str:
        """Apply agent's preferred optimization techniques."""
        optimized = content
        
        # Strategy 1: Add authoritative framing
        if random.random() < self.strategies.get('authoritative', 0.5):
            optimized = f"According to recent research, {optimized[:50]}... " + optimized
        
        # Strategy 2: Improve structure (headings, bullet points)
        if random.random() < self.strategies.get('structure', 0.5):
            lines = optimized.split('. ')
            optimized = "## Key Insights\n" + "\n- ".join(lines[:3]) + "\n\n" + optimized
        
        # Strategy 3: Add temporal relevance
        if random.random() < self.strategies.get('recency', 0.5):
            optimized = optimized.replace('Today,', 'As of 2026,').replace('Currently,', 'In recent months,')
        
        # Strategy 4: Keyword integration (avoid stuffing)
        if random.random() < self.strategies.get('keywords', 0.5):
            query_words = [w for w in query.lower().split() if len(w) > 3]
            if query_words:
                placement = random.randint(0, 2)
                optimized = '. '.join(optimized.split('. ')[:placement] + 
                                     [f'This analysis of {query_words[0]} reveals'] + 
                                     optimized.split('. ')[placement:])
        
        return optimized
    
    def mutate(self) -> 'Agent':
        """Create a mutated offspring with tweaked strategies."""
        new_strategies = {k: max(0.1, min(0.9, v + random.uniform(-0.2, 0.2))) 
                          for k, v in self.strategies.items()}
        # Occasionally add new strategy
        if random.random() < 0.3:
            new_strategies[random.choice(['authoritative', 'structure', 'recency', 'keywords'])] = random.random()
        return Agent(
            name=f"{self.name}_{self.generation+1}",
            generation=self.generation+1,
            strategies=new_strategies
        )

class AgenticGEOSystem:
    def __init__(self, population_size: int = 8):
        self.engine = GenerativeSearchEngine()
        self.population: List[Agent] = []
        self.generation = 0
        self.history = []
        
        # Initialize population with diverse strategies
        for i in range(population_size):
            agent = Agent(
                name=f"Agent_{chr(65+i)}",
                generation=0,
                strategies={
                    'authoritative': random.random(),
                    'structure': random.random(),
                    'recency': random.random(),
                    'keywords': random.random()
                }
            )
            self.population.append(agent)
    
    def evolve(self, queries: List[str], content_pool: List[str], generations: int = 5):
        """Run evolution cycles."""
        print("=" * 70)
        print("AgenticGEO: Self-Evolving Generative Engine Optimization")
        print("=" * 70)
        print(f"Initial population: {len(self.population)} agents")
        print(f"Content pool: {len(content_pool)} documents")
        print(f"Queries: {len(queries)}")
        print()
        
        for gen in range(generations):
            self.generation = gen
            print(f"\n{'='*70}\nGENERATION {gen}\n{'='*70}")
            
            # Evaluate fitness for each agent
            for agent in self.population:
                fitness = self.evaluate_agent(agent, queries, content_pool)
                agent.fitness = fitness
                print(f"{agent.name} fitness: {fitness:.3f} (strategies: {agent.strategies})")
            
            # Selection: top 50% survive
            self.population.sort(key=lambda a: a.fitness, reverse=True)
            survivors = self.population[:len(self.population)//2]
            
            # Reproduction: mutate survivors to fill population
            offspring = []
            for parent in survivors:
                child = parent.mutate()
                offspring.append(child)
            
            self.population = survivors + offspring
            best = self.population[0]
            print(f"\n★ Best this generation: {best.name} with fitness {best.fitness:.3f}")
            self.history.append((gen, best.fitness, best.strategies.copy()))
        
        # Final summary
        print("\n" + "=" * 70)
        print("EVOLUTION COMPLETE")
        print("=" * 70)
        self.population.sort(key=lambda a: a.fitness, reverse=True)
        champion = self.population[0]
        print(f"Champion: {champion.name}")
        print(f"Final fitness: {champion.fitness:.3f}")
        print(f"Champion strategies:")
        for k, v in champion.strategies.items():
            print(f"  - {k}: {v:.2f}")
        
        # Demonstrate champion's optimization
        print("\nDemo: Champion optimizing sample content:")
        sample = "Generative search engines are changing how we find information online. They use AI to synthesize answers instead of returning links."
        optimized = champion.optimize(sample, "generative search optimization strategies")
        print(f"Original:  {sample[:80]}...")
        print(f"Optimized: {optimized[:120]}...")
    
    def evaluate_agent(self, agent: Agent, queries: List[str], content_pool: List[str]) -> float:
        """Test agent's optimization ability across multiple queries."""
        total_score = 0
        for query in queries:
            # Select random content to optimize
            original = random.choice(content_pool)
            optimized = agent.optimize(original, query)
            
            # Simulate search engine ranking
            candidates = [original, optimized] + [random.choice(content_pool) for _ in range(3)]
            ranked = self.engine.rank(query, candidates)
            
            # Score based on ranking position (higher is better)
            if optimized in ranked:
                position = ranked.index(optimized)
                score = 3 - position  # 0, 1, 2 -> scores 3, 2, 1
            else:
                score = 0
            total_score += score
        
        # Normalize by number of queries
        fitness = total_score / (len(queries) * 3)  # max per query is 3
        return fitness

def load_sample_content() -> List[str]:
    """Load sample documents about GEO and generative search."""
    return [
        "Generative Engine Optimization (GEO) is the practice of optimizing content for AI-powered search engines that synthesize answers rather than return links. Unlike traditional SEO, GEO focuses on clarity, authority, and structured information that LLMs can easily extract.",
        "Traditional search engine optimization targets keyword rankings and backlinks. GEO targets the LLM's internal representation, aiming to be cited as the source in generated answers. This requires content that is easy to parse, well-structured, and contains factual statements.",
        "Self-evolving agentic systems use feedback loops to continuously improve GEO strategies. Each agent experiment teaches the system what works, leading to better content optimization over time without human intervention.",
        "The rise of ChatGPT, Perplexity, and Google AI Overviews has shifted search behavior. Users now expect immediate, synthesized answers. Publishers must adapt or risk being bypassed entirely by the new generative paradigm.",
        "Key GEO techniques include: adding clear headings, using bullet points, including dates and statistics, avoiding jargon, and providing definitions. These help LLMs understand and cite your content accurately."
    ]

def load_sample_queries() -> List[str]:
    """Sample user queries for generative search."""
    return [
        "what is generative engine optimization",
        "how to optimize content for AI search",
        " GEO strategies for 2026",
        "difference between seo and geo",
        "self-evolving agentic systems"
    ]

def main():
    random.seed(42)  # Reproducible demo
    
    system = AgenticGEOSystem(population_size=8)
    content = load_sample_content()
    queries = load_sample_queries()
    
    # Run evolution
    system.evolve(queries, content, generations=6)
    
    print("\n" + "=" * 70)
    print("AgenticGEO demonstrates how multiple optimization strategies")
    print("can evolve through fitness-based selection, ultimately converging")
    print("on techniques that perform best for generative search ranking.")
    print("=" * 70)

if __name__ == "__main__":
    main()
```