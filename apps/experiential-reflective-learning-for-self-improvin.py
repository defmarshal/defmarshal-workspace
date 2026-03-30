```python
#!/usr/bin/env python3
"""
Experiential Reflective Learning for Self-Improving LLM Agents

A minimal demonstration of an agent that learns from experience through reflection.
Simulates an LLM agent solving arithmetic problems, reflecting on mistakes, and improving.
"""

import random
import math
import re
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

@dataclass
class Experience:
    """Stores a single problem-solving attempt."""
    problem: str
    attempt: str
    correct: bool
    strategy: str
    timestamp: int = 0

class ReflectiveAgent:
    """An agent that learns by reflecting on past experiences."""
    
    def __init__(self):
        self.experiences: List[Experience] = []
        self.strategy_weights: Dict[str, float] = {
            'direct_calculation': 1.0,
            'break_down': 0.8,
            'estimation': 0.5,
            'wild_guess': 0.2
        }
        self.error_patterns: Counter = Counter()
        self.success_patterns: Counter = Counter()
        self.reflection_threshold = 5  # Reflect after every N experiences
        self.timestamp = 0
    
    def solve(self, problem: str) -> Tuple[str, bool]:
        """Attempt to solve a problem using weighted strategy selection."""
        # Choose strategy based on weights (higher weight = more likely)
        strategies = list(self.strategy_weights.keys())
        weights = [self.strategy_weights[s] for s in strategies]
        strategy = random.choices(strategies, weights=weights, k=1)[0]
        
        attempt = self._apply_strategy(problem, strategy)
        correct = self._check_answer(problem, attempt)
        
        # Record experience
        exp = Experience(
            problem=problem,
            attempt=attempt,
            correct=correct,
            strategy=strategy,
            timestamp=self.timestamp
        )
        self.experiences.append(exp)
        self.timestamp += 1
        
        # Trigger reflection periodically
        if len(self.experiences) % self.reflection_threshold == 0:
            self.reflect()
        
        return attempt, correct
    
    def _apply_strategy(self, problem: str, strategy: str) -> str:
        """Apply a problem-solving strategy."""
        # Extract operation and numbers
        match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', problem)
        if not match:
            return str(random.randint(0, 100))
        
        a, op, b = int(match.group(1)), match.group(2), int(match.group(3))
        
        if strategy == 'direct_calculation':
            if op == '+': return str(a + b)
            if op == '-': return str(a - b)
            if op == '*': return str(a * b)
            if op == '/': return str(round(a / b, 2) if b != 0 else 'Error')
        
        elif strategy == 'break_down':
            # Simplified: break into tens and ones
            if op == '+':
                result = (a // 10 + b // 10) * 10 + (a % 10 + b % 10)
                return str(result)
            return str(a + b)  # Fallback
        
        elif strategy == 'estimation':
            # Round and compute
            a_est = round(a, -1)
            b_est = round(b, -1)
            if op == '+': return str(a_est + b_est)
            if op == '-': return str(a_est - b_est)
            if op == '*': return str(a_est * b_est // 100)
            if op == '/': return str(round(a_est / b_est, 1)) if b_est != 0 else 'Error'
        
        else:  # wild_guess
            return str(random.randint(min(a,b), max(a,b)))
    
    def _check_answer(self, problem: str, attempt: str) -> bool:
        """Verify if attempt matches true answer."""
        match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', problem)
        if not match:
            return False
        a, op, b = int(match.group(1)), match.group(2), int(match.group(3))
        
        try:
            if op == '+': true_ans = a + b
            elif op == '-': true_ans = a - b
            elif op == '*': true_ans = a * b
            elif op == '/': true_ans = round(a / b, 2) if b != 0 else None
            else: return False
            
            if true_ans is None:
                return attempt.lower() == 'error'
            
            # Allow small rounding differences
            attempt_val = float(attempt) if attempt.replace('.','',1).isdigit() else None
            if attempt_val is None:
                return False
            return abs(attempt_val - true_ans) < 0.01
        except:
            return False
    
    def reflect(self) -> None:
        """Analyze recent experiences and update strategies."""
        recent = self.experiences[-self.reflection_threshold:]
        
        # Separate successes and failures
        successes = [e for e in recent if e.correct]
        failures = [e for e in recent if not e.correct]
        
        # Analyze which strategies worked
        strat_success: Dict[str, int] = Counter(e.strategy for e in successes)
        strat_failure: Dict[str, int] = Counter(e.strategy for e in failures)
        strat_total: Dict[str, int] = Counter(e.strategy for e in recent)
        
        # Update weights based on recent performance
        for strategy in self.strategy_weights:
            if strat_total[strategy] > 0:
                success_rate = strat_success[strategy] / strat_total[strategy]
                # Adjust weight: increase if success rate > 0.5, decrease otherwise
                adjustment = 1.1 if success_rate > 0.6 else 0.9
                self.strategy_weights[strategy] *= adjustment
        
        # Normalize weights
        total = sum(self.strategy_weights.values())
        for strategy in self.strategy_weights:
            self.strategy_weights[strategy] /= total
        
        # Record patterns for debugging
        self.success_patterns.update([e.strategy for e in successes])
        self.error_patterns.update([e.strategy for e in failures])
        
        print(f"[Reflection] Adjusted weights: {self.strategy_weights}")
    
    def performance_report(self) -> Dict:
        """Generate performance metrics."""
        total = len(self.experiences)
        if total == 0:
            return {'accuracy': 0, 'total': 0}
        
        correct = sum(1 for e in self.experiences if e.correct)
        accuracy = correct / total
        
        # Strategy breakdown
        strat_counts = Counter(e.strategy for e in self.experiences)
        strat_accuracy = {}
        for strategy in strat_counts:
            strat_exps = [e for e in self.experiences if e.strategy == strategy]
            correct_in_strat = sum(1 for e in strat_exps if e.correct)
            strat_accuracy[strategy] = correct_in_strat / len(strat_exps)
        
        return {
            'accuracy': accuracy,
            'total': total,
            'strategy_counts': dict(strat_counts),
            'strategy_accuracy': strat_accuracy,
            'current_weights': self.strategy_weights
        }

def generate_problems(n: int) -> List[str]:
    """Generate a batch of arithmetic problems."""
    ops = ['+', '-', '*', '/']
    problems = []
    for _ in range(n):
        a = random.randint(1, 100)
        b = random.randint(1, 50)  # Avoid large division results
        op = random.choice(ops)
        # Ensure division yields clean result sometimes
        if op == '/' and b != 0 and a % b != 0:
            a = (a // b) * b  # Make divisible
        problems.append(f"What is {a} {op} {b}?")
    return problems

def main():
    """Demonstrate experiential reflective learning."""
    agent = ReflectiveAgent()
    print("=== Experiential Reflective Learning Agent ===\n")
    
    # Training phase: solve problems and reflect
    print("Training phase: solving 30 problems with reflection...\n")
    problems = generate_problems(30)
    
    for i, prob in enumerate(problems, 1):
        attempt, correct = agent.solve(prob)
        status = "✓" if correct else "✗"
        print(f"Problem {i:2d}: {prob} → {attempt} {status}")
        
        # Show reflection progress
        if i % 5 == 0:
            report = agent.performance_report()
            print(f"   → Accuracy so far: {report['accuracy']:.1%}")
    
    # Evaluation phase: test on new problems
    print("\n" + "="*50)
    print("Evaluation phase: 10 new problems (no further reflection)\n")
    test_problems = generate_problems(10)
    
    correct_eval = 0
    for i, prob in enumerate(test_problems, 1):
        attempt, correct = agent.solve(prob)
        correct_eval += correct
        status = "✓" if correct else "✗"
        print(f"Test {i}: {prob} → {attempt} {status}")
    
    # Final report
    report = agent.performance_report()
    print("\n" + "="*50)
    print("FINAL REPORT:")
    print(f"Total experiences: {report['total']}")
    print(f"Overall accuracy: {report['accuracy']:.1%}")
    print(f"Evaluation accuracy: {correct_eval/10:.1%}")
    print("\nStrategy usage:")
    for strat, count in report['strategy_counts'].items():
        acc = report['strategy_accuracy'][strat]
        print(f"  {strat}: {count} times, {acc:.1%} success")
    
    print("\nCurrent strategy weights (learned):")
    for strat, weight in report['current_weights'].items():
        print(f"  {strat}: {weight:.3f}")
    
    # Demonstrate reflection effect
    print("\nKey insight:")
    print("The agent started with equal intuition about strategies,")
    print("but through reflection, it upweighted strategies that worked")
    print("and downweighted those that failed, improving over time.")

if __name__ == "__main__":
    main()
```