# JAWS: Enhancing Long-term Rollout of Neural Operators via Spatially-Adaptive Jacobian Regularization

Simulating the weather, ocean currents, or fluid dynamics has traditionally required solving complex equations on supercomputers. Neural operators—AI models that learn to approximate these simulations—offer a tantalizing shortcut: run a forward pass through a neural net instead of hours of computation. But there's a catch: when you chain many predictions together (an “autoregressive rollout”), tiny errors compound, and the simulation quickly diverges into nonsense. Enter **JAWS** (Jacobian-Adaptive Weighted Stabilization), a clever technique that tames this instability by regularizing the model’s Jacobian matrix in a spatially-aware way. It’s like giving the neural operator a set of internal stability braces that keep it from flying apart over long horizons.

## The Rollout Problem: Small Errors, Big Trouble

Neural operators (e.g., Fourier Neural Operators, Graph Neural Operators) excel at one-step prediction: given the current state, they output the next state with impressive accuracy. But real simulations require thousands of steps. Each prediction is only approximate; the errors accumulate, eventually causing the rollout to blow up—temperatures go to infinity, fluids penetrate solid boundaries, or wave amplitudes explode. This is the “drift” problem, and it has been a major blocker for using neural surrogates in long-horizon tasks like climate projection or aerodynamic design.

## Jacobian Regularization: Why It Helps

The Jacobian matrix of a neural operator describes how small changes in the input state affect the output state. If the singular values of the Jacobian are too large (especially >1), errors get amplified at each step. Regularizing the Jacobian—penalizing large singular values—encourages the model to learn a *contractive* mapping, which preserves stability over many steps.

Prior work applied a simple, uniform Jacobian regularization across all spatial locations. But JAWS introduces a key insight: **different regions of the domain have different stability requirements**. A chaotic vortex might need strong damping, while a laminar flow region could tolerate looser constraints.

## Spatially-Adaptive Regularization: The “Adaptive” in JAWS

JAWS computes a *spatially-varying* regularization weight based on local error sensitivity:

- It estimates, for each spatial coordinate, how much a small perturbation would grow over a short rollout.
- Locations with high sensitivity receive stronger Jacobian penalties during training.
- Low-sensitivity areas get lighter regularization, preserving expressivity where it’s safe.

This adaptive approach prevents over-regularization (which could make the model too stiff and lose accuracy) while focusing stability effort where it’s needed most.

## Training Without Sacrificing Accuracy

JAWS is trained in a two-phase process:

1. **Standard one-step fitting** on the training dataset to get a baseline model.
2. **Jacobian-regularized fine-tuning** with spatially-adaptive weights, using a differentiable estimator of the Jacobian’s spectral norm.

The result? A model that matches one-step accuracy of the baseline but rolls out stably for many more timesteps. In experiments with Navier–Stokes and Burgers’ equation simulations, JAWS reduced rollout error by 60–80% at 100 steps, while maintaining or improving one-step performance.

## Practical Payoffs: Longer, Better Rollouts

Why does this matter?

- **Longer simulations**: Researchers can now run neural operator rollouts for thousands of steps, making them viable for tasks that previously required ground-truth solvers.
- **Reduced training data**: Because the model generalizes better in rollout, you need fewer short trajectory samples to train a robust surrogate.
- **Safety-critical applications**: In engineering design, a stable rollout means you can trust the model’s predictions for optimization loops without fearing sudden divergence.
- **Composable operators**: JAWS-trained operators can be chained together (e.g., fluid-structure interaction) with less risk of instability.

---

JAWS shows that stability isn’t an afterthought—it can be baked into the training objective in a smart, spatially-aware way. By adapting regularization to local dynamics, we get neural operators that are both accurate and reliable over long horizons. This brings us a step closer to replacing expensive simulations with fast, learned surrogates across science and engineering. The next time you see a weather model that runs in seconds instead of hours, you might have JAWS to thank.