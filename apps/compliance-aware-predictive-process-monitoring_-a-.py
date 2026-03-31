```python
#!/usr/bin/env python3
import random
from collections import defaultdict

# Simplified business process: activities A, B, C, D, E
# Goal: predict next activity, but must respect compliance rules
ACTIVITIES = ['start', 'review', 'approve', 'reject', 'end']
TRANSITIONS = {
    'start': ['review'],
    'review': ['approve', 'reject'],
    'approve': ['end'],
    'reject': ['end'],
    'end': []
}

# Compliance rules (hard constraints)
COMPLIANCE_RULES = [
    # Rule 1: Cannot go from 'reject' back to 'review' (no Wiederaufnahme after rejection)
    lambda prev, cur: not (prev == 'reject' and cur == 'review'),
    # Rule 2: Must have exactly one 'approve' or 'reject' after 'review' (no multiple decisions)
    lambda prev, cur: not (prev in ['approve', 'reject'] and cur in ['approve', 'reject']),
]

class NeuralPredictor:
    """Sub-symbolic predictor: learns transition probabilities from data (simulated)."""
    def __init__(self):
        # Count transitions from synthetic data
        self.counts = defaultdict(lambda: defaultdict(int))
        self.total = defaultdict(int)
        self.train(1000)
    
    def train(self, n):
        for _ in range(n):
            seq = ['start']
            while seq[-1] != 'end':
                prev = seq[-1]
                # Simulate compliant process
                allowed = TRANSITIONS[prev]
                nxt = random.choice(allowed)
                seq.append(nxt)
            for i in range(len(seq)-1):
                self.counts[seq[i]][seq[i+1]] += 1
                self.total[seq[i]] += 1
    
    def predict_next(self, current):
        """Return probability distribution over next activities."""
        if self.total[current] == 0:
            return {a: 1.0/len(ACTIVITIES) for a in ACTIVITIES}
        probs = {}
        for a in ACTIVITIES:
            probs[a] = (self.counts[current][a] + 1) / (self.total[current] + len(ACTIVITIES))  # Laplace smoothing
        return probs

class ComplianceAwarePredictor:
    """Neuro-symbolic wrapper that ensures predictions obey compliance rules."""
    def __init__(self, neural):
        self.neural = neural
    
    def predict(self, current, history):
        """Return next activity respecting compliance."""
        # Get neural distribution
        probs = self.neural.predict_next(current)
        
        # Apply symbolic compliance filters
        valid = {}
        for a, p in probs.items():
            # Check all rules with respect to current->next and longer history
            if all(rule(current, a) for rule in COMPLIANCE_RULES):
                valid[a] = p
            else:
                valid[a] = 0.0
        
        # Renormalize if needed
        total = sum(valid.values())
        if total > 0:
            for a in valid:
                valid[a] /= total
        else:
            # Fallback: pick any valid action arbitrarily
            for a in ACTIVITIES:
                if all(rule(current, a) for rule in COMPLIANCE_RULES):
                    valid[a] = 1.0
                    break
        
        # Return most likely valid action
        return max(valid, key=valid.get)

def simulate_process(predictor, max_steps=20):
    """Run a process simulation using the predictor."""
    seq = ['start']
    while seq[-1] != 'end' and len(seq) < max_steps:
        nxt = predictor.predict(seq[-1], seq)
        seq.append(nxt)
    return seq

def main():
    random.seed(42)
    
    # Train neural predictor on compliant data
    neural = NeuralPredictor()
    print("Neural predictor trained on synthetic compliant logs.")
    
    # Wrap with compliance
    compliant_predictor = ComplianceAwarePredictor(neural)
    
    # Test scenarios
    scenarios = [
        (['review'], "After review"),
        (['approve'], "After approve"),
        (['reject'], "After reject"),
        (['review', 'approve'], "After approve, mistakenly trying to go back?"),
    ]
    
    print("\nCompliance-aware predictions:")
    for history, desc in scenarios:
        current = history[-1]
        pred = compliant_predictor.predict(current, history)
        print(f"  {desc} (hist={history}) -> next={pred}")
    
    # Full simulation
    print("\nSimulated compliant process:")
    sim = simulate_process(compliant_predictor)
    print(" -> ".join(sim))
    
    # Show what raw neural would suggest (possibly non-compliant)
    print("\nRaw neural predictions (may violate rules):")
    for current in ['review', 'approve', 'reject']:
        dist = neural.predict_next(current)
        top = max(dist, key=dist.get)
        print(f"  From {current}: top={top} (p={dist[top]:.2f})")
    print("  Note: raw neural might suggest 'review' after 'reject', which is non-compliant.")

if __name__ == "__main__":
    main()
```