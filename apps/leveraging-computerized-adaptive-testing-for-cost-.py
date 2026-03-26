```python
#!/usr/bin/env python3
"""
CAT for LLM Medical Evaluation - Computerized Adaptive Testing demo
Based on arXiv:2603.23506v1 - Cost-effective LLM benchmarking using IRT
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ExamItem:
    """A medical benchmark question with IRT parameters"""
    id: int
    difficulty: float  # 0=easy, 1=hard (θ=0 is average ability)
    discrimination: float  # How well item distinguishes ability levels (0.5-2.0)
    content: str  # Question text
    answer: int  # Correct: 0 or 1 (binary for simplicity)

class IRTModel:
    """1-parameter logistic (Rasch) model for binary items"""
    @staticmethod
    def probability(ability: float, difficulty: float, discrimination: float = 1.0) -> float:
        """P(correct | ability θ, item difficulty β)"""
        return 1.0 / (1.0 + np.exp(-discrimination * (ability - difficulty)))
    
    @staticmethod
    def log_likelihood(ability: float, responses: List[Tuple[ExamItem, int]]) -> float:
        """Log-likelihood of ability given response history"""
        ll = 0.0
        for item, response in responses:
            p = IRTModel.probability(ability, item.difficulty, item.discrimination)
            # Avoid log(0)
            p = np.clip(p, 1e-6, 1-1e-6)
            ll += response * np.log(p) + (1-response) * np.log(1-p)
        return ll

class AdaptiveTester:
    """Computerized Adaptive Testing engine for LLM evaluation"""
    def __init__(self, item_pool: List[ExamItem], 
                 ability_prior_mean: float = 0.0,
                 ability_prior_sd: float = 1.0,
                 min_items: int = 5,
                 max_items: int = 20,
                 se_threshold: float = 0.3):
        self.item_pool = item_pool
        self.ability = ability_prior_mean
        self.ability_sd = ability_prior_sd
        self.min_items = min_items
        self.max_items = max_items
        self.se_threshold = se_threshold
        self.responses = []  # List of (item, response)
        self.administered_items = set()
        
    def next_item(self) -> ExamItem:
        """Select next item using maximum information criterion"""
        # Exclude already administered items
        available = [item for item in self.item_pool if item.id not in self.administered_items]
        
        if not available:
            raise ValueError("No items left!")
            
        # If we have few items, favor medium difficulty items for better initial estimate
        if len(self.responses) < 3:
            # Choose item closest to current ability estimate
            info = [(abs(item.difficulty - self.ability), item) for item in available]
        else:
            # Maximum Fisher Information: I(θ) = p(θ)*(1-p(θ)) for each item
            info = []
            for item in available:
                p = IRTModel.probability(self.ability, item.difficulty, item.discrimination)
                fisher_info = p * (1 - p) * (item.discrimination ** 2)
                # Prefer items with highest information at current ability
                info.append((-fisher_info, item))  # Negative for min-heap effect
        
        # Return item with max info / closest difficulty
        return min(info, key=lambda x: x[0])[1]
    
    def update_ability(self):
        """Update ability estimate using Newton-Raphson on log-likelihood"""
        if not self.responses:
            return
        
        # Simple Newton-Raphson for Rasch model
        # θ_new = θ_old + (dLL/dθ) / (d²LL/dθ²)
        # For Rasch: dLL/dθ = Σ (r_i - p_i(θ)) * a_i
        #            d²LL/dθ² = - Σ a_i² * p_i(θ) * (1 - p_i(θ))
        
        a = np.array([item.discrimination for item, _ in self.responses])
        r = np.array([response for _, response in self.responses])
        
        # Compute probabilities at current ability
        p = np.array([IRTModel.probability(self.ability, item.difficulty, item.discrimination) 
                      for item, _ in self.responses])
        
        # First derivative
        dll = np.sum(a * (r - p))
        
        # Second derivative (negative, so take absolute)
        d2ll = -np.sum(a**2 * p * (1 - p))
        
        if abs(d2ll) < 1e-6:
            return  # No update
        
        delta = dll / d2ll
        self.ability += delta
        # Update standard error (approximate)
        self.ability_sd = 1.0 / np.sqrt(-d2ll)
    
    def administer_item(self, item: ExamItem, llm_response: int) -> bool:
        """Give item to LLM, record response, update estimate"""
        self.administered_items.add(item.id)
        self.responses.append((item, llm_response))
        self.update_ability()
        return llm_response == item.answer
    
    def should_continue(self) -> bool:
        """Check stopping criteria"""
        if len(self.responses) < self.min_items:
            return True
        if len(self.responses) >= self.max_items:
            return False
        # Stop when standard error is low enough
        return self.ability_sd > self.se_threshold
    
    def get_final_score(self) -> Tuple[float, float]:
        """Return (ability estimate, standard error)"""
        return self.ability, self.ability_sd

class MockMedicalLLM:
    """Simulates an LLM answering medical questions with varying ability"""
    def __init__(self, true_ability: float, consistency: float = 0.9):
        self.true_ability = true_ability  # θ parameter
        self.consistency = consistency  # Probability of answering correctly given ability
    
    def answer(self, item: ExamItem) -> int:
        """Generate answer based on IRT probability"""
        p_correct = IRTModel.probability(self.true_ability, item.difficulty, item.discrimination)
        # Adjust by consistency (LLM isn't perfectly rational)
        p_correct = p_correct * self.consistency + (1 - self.consistency) * 0.5
        return 1 if np.random.random() < p_correct else 0

def generate_item_pool(num_items: int = 50) -> List[ExamItem]:
    """Generate synthetic medical benchmark items"""
    items = []
    medical_terms = [
        "myocardial infarction", "pneumonia", "diabetes type 2", "hypertension",
        "COPD", "asthma", "renal failure", "hepatitis", "sepsis", "stroke"
    ]
    
    for i in range(num_items):
        difficulty = np.random.beta(2, 5)  # Most items medium difficulty
        discrimination = np.random.uniform(0.8, 2.0)
        term = np.random.choice(medical_terms)
        content = f"What is the first-line treatment for {term}?"
        # Simulate that harder items have lower correct answer probability on average
        correct = 1 if np.random.random() > difficulty else 0
        items.append(ExamItem(i, difficulty, discrimination, content, correct))
    
    return items

def compare_fixed_vs_adaptive(llm: MockMedicalLLM, item_pool: List[ExamItem], 
                             fixed_length: int = 20) -> dict:
    """Compare fixed-length test vs adaptive"""
    # Fixed test: random items
    fixed_items = np.random.choice(item_pool, fixed_length, replace=False)
    fixed_responses = [(item, llm.answer(item)) for item in fixed_items]
    fixed_score = sum(r for _, r in fixed_responses) / fixed_length
    
    # Adaptive test
    adaptive = AdaptiveTester(item_pool, min_items=5, max_items=fixed_length, se_threshold=0.25)
    num_adaptive = 0
    while adaptive.should_continue():
        item = adaptive.next_item()
        response = llm.answer(item)
        adaptive.administer_item(item, response)
        num_adaptive += 1
    
    adaptive_score = sum(r for _, r in adaptive.responses) / len(adaptive.responses) if adaptive.responses else 0
    adaptive_ability, adaptive_se = adaptive.get_final_score()
    
    return {
        'fixed_score': fixed_score,
        'adaptive_score': adaptive_score,
        'fixed_items': fixed_length,
        'adaptive_items': num_adaptive,
        'adaptive_ability': adaptive_ability,
        'adaptive_se': adaptive_se
    }

def main():
    """Demonstrate CAT for LLM medical evaluation"""
    print("🏥 Computerized Adaptive Testing for LLM Medical Benchmarking")
    print("   arXiv:2603.23506v1 Demonstration")
    print("=" * 60)
    
    # Generate item pool
    print("\n📝 Generating synthetic medical question pool...")
    item_pool = generate_item_pool(100)
    print(f"   Created {len(item_pool)} items with varying difficulty/discrimination")
    
    # Create LLMs with different abilities
    llms = [
        ("Resident", 0.5, 0.85),   # Average medical knowledge
        ("Fellow", 1.2, 0.90),     # Specialist level
        ("Expert", 2.0, 0.95),     # Top-tier
    ]
    
    print("\n🎯 Comparing Fixed vs Adaptive testing strategies:")
    print("-" * 60)
    
    results = []
    for name, ability, consistency in llms:
        llm = MockMedicalLLM(ability, consistency)
        comparison = compare_fixed_vs_adaptive(llm, item_pool, fixed_length=20)
        results.append((name, comparison))
        
        print(f"\n{name} (θ={ability:.1f}, consistency={consistency:.0%}):")
        print(f"  Fixed 20-item test:    score={comparison['fixed_score']:.1%}")
        print(f"  Adaptive test:         score={comparison['adaptive_score']:.1%} "
              f"({comparison['adaptive_items']} items, SE={comparison['adaptive_se']:.3f})")
        
        reduction = comparison['fixed_items'] - comparison['adaptive_items']
        savings = (reduction / comparison['fixed_items']) * 100
        print(f"  → Item reduction: {reduction} items ({savings:.0f}% fewer)")
    
    # Summary statistics
    print("\n" + "="*60)
    print("📊 Summary:")
    avg_savings = np.mean([r[1]['fixed_items'] - r[1]['adaptive_items'] for r in results])
    print(f"  Average items saved per evaluation: {avg_savings:.1f}")
    print(f"  Cost reduction: ~{(avg_savings/20)*100:.0f}% for 20-item baseline")
    
    print("\n💡 Key Insight:")
    print("  Adaptive testing focuses on items that best discriminate")
    print("  the LLM's ability level, achieving same precision with")
    print("  fewer items. This dramatically reduces evaluation cost.")
    
    print("\n" + "="*60)
    print("✅ CAT demonstration complete!")
    print("   Next: Apply to real LLM APIs with actual medical questions")

if __name__ == "__main__":
    main()
```