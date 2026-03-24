```python
#!/usr/bin/env python3
import numpy as np

# Stakeholders: regulator, manufacturer, user, safety_expert
stakeholders = {
    'Regulator':     {'safety': 0.4, 'efficiency': 0.1, 'comfort': 0.1, 'cost': 0.1, 'transparency': 0.3},
    'Manufacturer':  {'safety': 0.2, 'efficiency': 0.3, 'comfort': 0.2, 'cost': 0.2, 'transparency': 0.1},
    'User':          {'safety': 0.25, 'efficiency': 0.1, 'comfort': 0.4, 'cost': 0.2, 'transparency': 0.05},
    'Safety_Expert': {'safety': 0.5, 'efficiency': 0.05, 'comfort': 0.1, 'cost': 0.05, 'transparency': 0.3}
}

# Interface requirements categories
requirements = ['controls', 'displays', 'alerts', 'redundancy', 'data_logging']

# Initial arbitrary weights for requirements (same for all)
req_weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

def softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum()

def consensus_distance(prefs):
    """Average pairwise L2 distance between stakeholder preference vectors."""
    vectors = np.array([p for p in prefs.values()])
    n = len(vectors)
    dists = []
    for i in range(n):
        for j in range(i+1, n):
            dists.append(np.linalg.norm(vectors[i] - vectors[j]))
    return np.mean(dists)

def coordinate_step(prefs, req_weights, alpha=0.1):
    """One coordination iteration: move each stakeholder toward group average."""
    vectors = np.array([p for p in prefs.values()])
    avg_vec = vectors.mean(axis=0)
    new_prefs = {}
    for name, vec in prefs.items():
        new_vec = (1 - alpha) * vec + alpha * avg_vec
        new_prefs[name] = new_vec / new_vec.sum()
    # Adjust requirement weights similarly (using same alpha)
    avg_req = req_weights
    new_req = (1 - alpha) * req_weights + alpha * avg_req
    new_req = new_req / new_req.sum()
    return new_prefs, new_req

# Run coordination
print("Stakeholder coordination for AV performance indicators and interface requirements")
print("=" * 70)
print("\nInitial preferences (indicators):")
for s, w in stakeholders.items():
    print(f"  {s}: " + " ".join([f"{k}={v:.2f}" for k,v in w.items()]))

print("\nInitial requirement weights:")
for r, w in zip(requirements, req_weights):
    print(f"  {r}: {w:.2f}")

dist = consensus_distance(stakeholders)
print(f"\nInitial consensus distance: {dist:.4f}")

for iteration in range(1, 21):
    stakeholders, req_weights = coordinate_step(stakeholders, req_weights, alpha=0.15)
    dist = consensus_distance(stakeholders)
    if iteration % 5 == 0:
        print(f"\nAfter iteration {iteration}: consensus distance = {dist:.4f}")
    if dist < 0.05:
        break

print("\n" + "=" * 70)
print("Coordinated preferences (indicators):")
for s, w in stakeholders.items():
    print(f"  {s}: " + " ".join([f"{k}={v:.2f}" for k,v in w.items()]))

print("\nCoordinated requirement weights:")
for r, w in zip(requirements, req_weights):
    print(f"  {r}: {w:.2f}")

print(f"\nFinal consensus distance: {dist:.4f}")
print("\nInterpretation: stakeholders have converged on a balanced set of performance")
print("indicators and interface requirements for automated vehicles.")
```