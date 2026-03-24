#!/usr/bin/env python3
import numpy as np

# Define states
states = ['high', 'low']
n_states = len(states)

# Transition matrix: rows from, columns to
A = np.array([[0.9, 0.1],
              [0.2, 0.8]])

# Prior
pi = np.array([0.5, 0.5])

# Emission: For each state, probability of observation bins.
# Bins: 0: fast (rt < 300), 1: medium (300–500), 2: slow (>500)
# Generate synthetic data to estimate emission probabilities
np.random.seed(42)
n_samples = 1000
# High awareness: faster reaction times
high_rt = np.random.normal(200, 30, n_samples)
# Low awareness: slower reaction times
low_rt = np.random.normal(500, 70, n_samples)

# Bin edges
def bin_rt(rt):
    if rt < 300: return 0
    elif rt < 500: return 1
    else: return 2

# Compute emission probabilities: P(bin|state)
B = np.zeros((n_states, 3))
for i, rt_list in enumerate([high_rt, low_rt]):
    bins_idx = [bin_rt(rt) for rt in rt_list]
    counts = np.bincount(bins_idx, minlength=3)
    B[i] = counts / counts.sum()

# Test sequence (simulate a monitoring session)
test_rt = [180, 220, 310, 480, 520, 190, 210, 290, 530, 490, 200, 210, 300, 310, 500, 510, 200, 210, 220, 530]
test_bins = [bin_rt(rt) for rt in test_rt]

# Forward algorithm for dynamic Bayesian inference
def forward(obs):
    T = len(obs)
    alpha = np.zeros((T, n_states))
    # t=0
    alpha[0] = pi * B[:, obs[0]]
    alpha[0] /= alpha[0].sum()  # normalize
    # t>0
    for t in range(1, T):
        for j in range(n_states):
            alpha[t, j] = np.sum(alpha[t-1] * A[:, j]) * B[j, obs[t]]
        alpha[t] /= alpha[t].sum()  # normalize to avoid underflow
    return alpha

alpha = forward(test_bins)

# Print results
print("Time  RT(ms)  P(high)  P(low)")
for t, (rt, bin_idx) in enumerate(zip(test_rt, test_bins)):
    print(f"{t:4d}  {rt:6.0f}   {alpha[t,0]:.3f}    {alpha[t,1]:.3f}")

# Simple decision rule: if P(high) > 0.5 then high awareness else low
predictions = ['high' if a[0] > 0.5 else 'low' for a in alpha]
print("\nPredictions (per time step):", predictions)