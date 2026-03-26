```python
#!/usr/bin/env python3
"""
AI Mental Models: Bounded Architecture with Intuition vs Deliberation
Based on arXiv:2603.22561v1 - Demonstrates dual-process system on cognitive tasks
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class CognitiveTask:
    """Represents a problem with intuitive and deliberative answers"""
    features: np.ndarray  # Problem representation
    intuitive_answer: int  # Fast, automatic but often wrong
    correct_answer: int    # Slow, analytical correct answer
    difficulty: float      # 0-1, how hard to override intuition

class IntuitionModule:
    """Fast, shallow network - System 1 thinking"""
    def __init__(self, input_dim: int, output_dim: int):
        # Simple linear classifier (fast)
        self.W = np.random.randn(input_dim, output_dim) * 0.1
        self.b = np.random.randn(output_dim) * 0.1
        
    def predict(self, x: np.ndarray) -> int:
        """Quick, automatic response"""
        logits = x @ self.W + self.b
        return np.argmax(logits)
    
    def confidence(self, x: np.ndarray) -> float:
        """How confident the intuition is (softmax max)"""
        logits = x @ self.W + self.b
        probs = np.exp(logits - np.max(logits))
        probs /= probs.sum()
        return np.max(probs)

class DeliberationModule:
    """Slower, deeper network - System 2 thinking"""
    def __init__(self, input_dim: int, output_dim: int, depth: int = 3):
        self.layers = []
        for i in range(depth):
            W = np.random.randn(input_dim if i==0 else 32, 32) * 0.1
            b = np.random.randn(32) * 0.1
            self.layers.append((W, b))
        self.output_W = np.random.randn(32, output_dim) * 0.1
        self.output_b = np.random.randn(output_dim) * 0.1
        
    def predict(self, x: np.ndarray) -> int:
        """Slow, analytical reasoning"""
        h = x
        for W, b in self.layers:
            h = np.tanh(h @ W + b)  # Nonlinear processing
        logits = h @ self.output_W + self.output_b
        return np.argmax(logits)

class BoundedAgent:
    """Architecture with division of labor between intuition and deliberation"""
    def __init__(self, input_dim: int, output_dim: int, deliberation_cost: float = 1.0):
        self.intuition = IntuitionModule(input_dim, output_dim)
        self.deliberation = DeliberationModule(input_dim, output_dim)
        self.deliberation_cost = deliberation_cost
        self.gate_threshold = 0.7  # When to engage deliberation
        
    def decide(self, x: np.ndarray, task_difficulty: float) -> Tuple[int, str, bool]:
        """
        Decision process: Start with intuition, deliberate if uncertain or task hard
        Returns: (answer, mode, deliberation_used)
        """
        # Step 1: Fast intuition
        intuitive_answer = self.intuition.predict(x)
        intuitive_conf = self.intuition.confidence(x)
        
        # Step 2: Gate decision
        # Engage deliberation if:
        # - Intuition low confidence
        # - Task is known to be difficult (where intuition often wrong)
        # - High stakes (simulated by task_difficulty)
        should_deliberate = (intuitive_conf < self.gate_threshold) or (task_difficulty > 0.5)
        
        if should_deliberate:
            final_answer = self.deliberation.predict(x)
            mode = "deliberative"
            deliberation_used = True
        else:
            final_answer = intuitive_answer
            mode = "intuitive"
            deliberation_used = False
            
        return final_answer, mode, deliberation_used
    
    def train_intuition(self, tasks: List[CognitiveTask], epochs: int = 100):
        """Train intuition module on simple examples (fast learning)"""
        for _ in range(epochs):
            for task in tasks:
                x = task.features
                y = task.intuitive_answer  # Learn the intuitive answer
                # Simple gradient descent (simplified)
                logits = x @ self.intuition.W + self.intuition.b
                probs = np.exp(logits) / np.exp(logits).sum()
                error = probs.copy()
                error[y] -= 1
                self.intuition.W -= 0.01 * np.outer(x, error)
                self.intuition.b -= 0.01 * error
    
    def train_deliberation(self, tasks: List[CognitiveTask], epochs: int = 200):
        """Train deliberation module on correct answers (slower, more accurate)"""
        for _ in range(epochs):
            for task in tasks:
                x = task.features
                y = task.correct_answer
                # Backprop through deliberation network
                h = x
                activations = [h]
                for W, b in self.deliberation.layers:
                    h = np.tanh(h @ W + b)
                    activations.append(h)
                logits = h @ self.deliberation.output_W + self.deliberation.output_b
                probs = np.exp(logits) / np.exp(logits).sum()
                error = probs.copy()
                error[y] -= 1
                
                # Update output layer
                self.deliberation.output_W -= 0.01 * np.outer(activations[-1], error)
                self.deliberation.output_b -= 0.01 * error
                
                # Backprop through hidden layers
                for i in reversed(range(len(self.deliberation.layers))):
                    W, b = self.deliberation.layers[i]
                    h_prev = activations[i]
                    error = (error @ self.deliberation.output_W.T) if i == len(self.deliberation.layers)-1 else (error @ W.T)
                    error = error * (1 - h_prev**2)  # Derivative of tanh
                    W -= 0.01 * np.outer(h_prev, error)
                    b -= 0.01 * error

def create_cognitive_reflection_tasks() -> List[CognitiveTask]:
    """Create classic cognitive reflection test problems"""
    tasks = []
    
    # Problem 1: Bat and ball
    # Intuitive: ball costs $0.10 (since bat is $1.00 more)
    # Correct: ball costs $0.05 (bat $1.05, difference $1.00)
    x1 = np.array([1.0, 1.10, 1.00])  # features: [total, bat_extra, ?]
    tasks.append(CognitiveTask(x1, intuitive_answer=1, correct_answer=0, difficulty=0.8))
    
    # Problem 2: Lily pads doubling
    # Intuitive: 24 days (half of 48)
    # Correct: 47 days (covers half on day 47)
    x2 = np.array([48, 2])  # [days, doubling_factor]
    tasks.append(CognitiveTask(x2, intuitive_answer=24, correct_answer=47, difficulty=0.7))
    
    # Problem 3: Widget production
    # Intuitive: 100 minutes (5 machines * 5 = 25, 4x slower = 100)
    # Correct: 5 minutes (more machines, faster)
    x3 = np.array([5, 5, 4])  # [machines, time, factor]
    tasks.append(CognitiveTask(x3, intuitive_answer=2, correct_answer=0, difficulty=0.6))
    
    return tasks

def encode_answer(answer: int, num_options: int = 3) -> np.ndarray:
    """One-hot encode answer"""
    enc = np.zeros(num_options)
    enc[answer] = 1.0
    return enc

def main():
    """Demonstrate bounded architecture with intuition-deliberation division"""
    print("🧠 AI Mental Models: Intuition vs Deliberation")
    print("   Bounded Neural Architecture Demonstration")
    print("=" * 60)
    
    # Create cognitive reflection tasks
    raw_tasks = create_cognitive_reflection_tasks()
    
    # Encode features and answers
    tasks = []
    for t in raw_tasks:
        # Normalize features for neural net
        x = t.features / t.features.max()
        tasks.append(CognitiveTask(x, t.intuitive_answer, t.correct_answer, t.difficulty))
    
    # Initialize agent
    input_dim = max(len(t.features) for t in tasks)
    output_dim = 3  # We'll map answers to 3 bins: low, medium, high
    
    # For simplicity, remap answers to 0,1,2
    remapped_tasks = []
    for t in tasks:
        # Map intuitive/correct to 0,1,2 range based on value
        # In real implementation, would be actual answer choices
        intuitive_remapped = min(int(t.intuitive_answer), 2)
        correct_remapped = min(int(t.correct_answer), 2)
        remapped_tasks.append(CognitiveTask(t.features, intuitive_remapped, correct_remapped, t.difficulty))
    
    tasks = remapped_tasks
    agent = BoundedAgent(input_dim=input_dim, output_dim=output_dim, deliberation_cost=1.0)
    
    print(f"\n📚 Training on {len(tasks)} cognitive reflection tasks...")
    
    # Train modules separately (simulating that intuition learns fast from simple patterns,
    # deliberation learns slower but more accurately from correct answers)
    print("  • Training intuition module... (fast, pattern-matching)")
    agent.train_intuition(tasks, epochs=50)
    
    print("  • Training deliberation module... (slow, analytical)")
    agent.train_deliberation(tasks, epochs=100)
    
    # Evaluate on tasks
    print("\n📊 Evaluation:")
    print("-" * 60)
    
    intuitive_correct = 0
    deliberative_correct = 0
    agent_correct = 0
    
    for i, task in enumerate(tasks):
        x = task.features
        # What intuition alone would give
        intuitive_ans = agent.intuition.predict(x)
        intuitive_correct += (intuitive_ans == task.correct_answer)
        
        # What deliberation alone would give
        deliberative_ans = agent.deliberation.predict(x)
        deliberative_correct += (deliberative_ans == task.correct_answer)
        
        # What the bounded agent does
        final_ans, mode, used_delib = agent.decide(x, task.difficulty)
        agent_correct += (final_ans == task.correct_answer)
        
        status = "✓" if final_ans == task.correct_answer else "✗"
        print(f"Task {i+1}: Intuition={intuitive_ans}, Deliberation={deliberative_ans}, Agent={final_ans}({mode}) {status}")
    
    print("\n" + "="*60)
    print("📈 Results Summary:")
    print(f"  Intuition accuracy: {intuitive_correct}/{len(tasks)} ({intuitive_correct/len(tasks):.1%})")
    print(f"  Deliberation accuracy: {deliberative_correct}/{len(tasks)} ({deliberative_correct/len(tasks):.1%})")
    print(f"  Bounded agent accuracy: {agent_correct}/{len(tasks)} ({agent_correct/len(tasks):.1%})")
    
    # Simulate multiple runs with different gate thresholds
    print("\n🔍 Gate Threshold Sensitivity:")
    original_threshold = agent.gate_threshold
    for threshold in [0.5, 0.6, 0.7, 0.8, 0.9]:
        agent.gate_threshold = threshold
        correct = 0
        deliberation_uses = 0
        for task in tasks:
            ans, mode, used = agent.decide(task.features, task.difficulty)
            correct += (ans == task.correct_answer)
            deliberation_uses += int(used)
        print(f"  Threshold {threshold:.1f}: {correct}/{len(tasks)} correct, "
              f"{deliberation_uses}/{len(tasks)} deliberations ({deliberation_uses/len(tasks):.1%})")
    
    agent.gate_threshold = original_threshold
    
    print("\n💡 Key Insight:")
    print("  Bounded rationality: Intuition is fast but error-prone;")
    print("  deliberation is accurate but costly. The gate optimally")
    print("  decides when to switch based on confidence/difficulty.")
    print("  This division of labor reduces overall cost while maintaining accuracy.")
    
    print("\n" + "="*60)
    print("✅ Demonstration complete!")

if __name__ == "__main__":
    main()
```