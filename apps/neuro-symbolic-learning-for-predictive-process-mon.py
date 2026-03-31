```python
#!/usr/bin/env python3
import random
from collections import defaultdict, Counter

# Synthetic event log: sequences of activities (A, B, C, D, E)
# Label: 1 if anomalous (E after A without B), else 0
def generate_sample():
    seq_len = random.randint(3, 6)
    events = random.choices(['A', 'B', 'C', 'D'], k=seq_len)
    # Inject anomaly pattern occasionally
    if 'A' in events and 'E' in events and events.index('E') > events.index('A') and 'B' not in events:
        label = 1
    else:
        label = 0
    return events, label

# Symbolic rules as simple conditions over event pairs
def compile_rules():
    rules = [
        lambda s: 1 if ('A', 'E') in zip(s, s[1:]) and 'B' not in s else 0,  # anomaly pattern
        lambda s: 1 if s.count('C') > 2 else 0,                            # too many C
        lambda s: 1 if s[-1] == 'D' else 0,                               # ends with D (benign)
    ]
    return rules

# Simple neural-ish feature: n-gram presence
def extract_features(seq):
    bigrams = [seq[i]+seq[i+1] for i in range(len(seq)-1)]
    return Counter(bigrams)

def train_two_stage(num_samples=500):
    # Generate data
    data = [generate_sample() for _ in range(num_samples)]
    X = [extract_features(seq) for seq, _ in data]
    y = [label for _, label in data]
    
    # Stage 1: Learn importance weights for bigrams (neural-ish)
    bigram_weights = defaultdict(float)
    for feats, label in zip(X, y):
        for bg, cnt in feats.items():
            if label == 1:
                bigram_weights[bg] += cnt
            else:
                bigram_weights[bg] -= cnt
    # Normalize
    maxw = max(abs(w) for w in bigram_weights.values()) or 1
    for bg in bigram_weights:
        bigram_weights[bg] /= maxw
    
    # Stage 2: Apply symbolic rules as "logical neurons"
    rules = compile_rules()
    rule_outputs = []
    for seq, label in data:
        rule_preds = [int(rule(seq)) for rule in rules]
        rule_outputs.append(rule_preds)
    
    # Evaluate individual rules
    rule_accs = []
    for ridx in range(len(rules)):
        preds = [r[ridx] for r in rule_outputs]
        acc = sum(p == l for p, l in zip(preds, y)) / len(y)
        rule_accs.append(acc)
    
    print("Rule accuracies (before pruning):", [round(a, 3) for a in rule_accs])
    
    # Rule pruning: keep only rules with accuracy > random guess (0.5) AND not correlated to others
    kept_idxs = [i for i, a in enumerate(rule_accs) if a > 0.55]
    print("Pruned to rules:", kept_idxs)
    
    # Combined predictor: weighted sum of neural features + kept rule votes
    def predict(seq):
        feats = extract_features(seq)
        neural_score = sum(bigram_weights[bg] * feats.get(bg, 0) for bg in bigram_weights)
        rule_score = sum([rules[i](seq) for i in kept_idxs])
        return 1 if neural_score > 0.2 or rule_score > 0 else 0
    
    # Test
    test_data = [generate_sample() for _ in range(100)]
    correct = sum(predict(seq) == label for seq, label in test_data)
    print(f"Test accuracy: {correct/100:.2%}")
    print("Kept rules (interpretable):", [f"R{i}" for i in kept_idxs])
    print("Top bigram weights:", dict(sorted(bigram_weights.items(), key=lambda x: abs(x[1]), reverse=True)[:5]))

def main():
    random.seed(42)
    train_two_stage()

if __name__ == "__main__":
    main()
```