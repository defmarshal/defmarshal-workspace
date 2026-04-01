# Why Depth Matters in Parallelizable Sequence Models: A Lie Algebraic View

Sequence models have come a long way—from recurrent networks that process tokens one by one (slow but expressive) to Transformers that handle entire sequences in parallel (fast but sometimes lacking in nuance). The current wisdom is: **parallelism is king**; we sacrifice depth for speed. But a provocative new paper asks: *Are we giving up too much?* Using the elegant mathematics of Lie algebras, the authors show that **depth is not just a cosmetic detail**—it fundamentally determines what functions a sequence model can represent. In other words, your fast Transformer might be mathematically incapable of capturing certain patterns, no matter how many parameters you throw at it. Let's explore why depth matters, through the lens of symmetry and continuous transformations.

---

## ⚖️ The Parallelism–Expressivity Trade-off

Modern sequence models often prioritize **sequence-level parallelism**:
- **Transformers**: Compute all token interactions simultaneously via self-attention. Great for GPUs, but depth (number of layers) is limited in practice because each layer adds sequential computation.
- **Structured State-Space Models (SSMs)**: Like S4, these offer parallel training and long-range modeling, but they typically have a shallow structure (often a single block repeated).

The trend has been to **keep models shallow** (dozens of layers at most) to maintain fast training and inference. But is this costing us expressive power? The paper argues yes—and the reason lies in the **mathematical depth required to approximate certain transformations**, which they analyze using Lie groups and algebras.

---

## 🧠 Lie Algebra: The Math Behind Continuous Change

A **Lie group** is a continuous symmetry transformation (like rotation, scaling). Its associated **Lie algebra** describes the *infinitesimal* generators of that transformation—the small steps that, when integrated, produce the full transformation.

Why does this matter for sequence models? Because many sequence operations we care about are **continuous transformations** of the input:
- Smoothly varying attention patterns
- Gradual gating in SSMs
- Rotations and scalings in embedding space

The paper's key insight: **Each layer of a sequence model can be seen as a small step (exponential of a Lie algebra element)**. Stacking layers composes these small steps into a larger transformation. The **depth** determines how well you can approximate *any* continuous transformation. This is analogous to how numerical integration needs many small steps to accurately trace a curve.

---

## 🔬 Main Theoretical Result

The authors prove that for a broad class of parallelizable sequence models (including Transformers with linear attention, SSMs, and certain convolutional architectures), the set of functions they can represent with **L layers** forms a **Lie subgroup** of the full transformation group. As **L increases**, this subgroup **denser** in the full group—meaning you can approximate more functions.

Crucially, there exist transformations that **require depth** to represent even approximately. A shallow model (fixed depth) will have a *gap* between what it can do and what a deeper model can do. This gap does not vanish with more parameters within a layer; it's a *depth-specific* limitation.

---

## 📈 Practical Implications

### 1. **Depth is a budget for compositional complexity**
If your task requires combining many local transformations (e.g., multi-resolution pattern mixing, hierarchical feature extraction), you need sufficient depth. Parallelism doesn't remove this need; it just lets you compute each layer quickly.

### 2. **Shallow models may struggle with long-range dependencies**
Even if a model is parallelizable, if it has too few layers, it might not be able to *gradually* propagate information across the sequence. The Lie algebra view suggests this is not a training hack but a * representational limitation*.

### 3. **Designing better parallel blocks**
The paper suggests that to get more expressivity per layer, each parallel block should be designed to **move farther in Lie algebra space**—i.e., have a richer set of generators. This could mean:
- More expressive mixing mechanisms (beyond softmax attention)
- Incorporating rotations or other continuous groups explicitly
- Using higher-order approximations (like second-order Taylor steps) instead of first-order (linear) layers

### 4. **Scaling laws should include depth**
Current scaling laws often trade depth for width. This paper argues that depth has a *qualitative* impact, not just quantitative. There may be **breakpoints** where adding a few more layers unlocks new capabilities (like jumping to a larger Lie subgroup).

---

## 🧪 Experimental Validation

The authors test their theory on synthetic tasks that require known Lie group transformations:
- **Rotating embeddings** across dimensions
- **Composing multiple frequency shifts**
- **Non-commutative transformations** (order matters)

Results confirm: **shallow parallel models fail** to approximate these even with massive width, while **deeper models succeed**. Adding more layers improves approximation error predictably, following the theoretical convergence rates.

On real language modeling (WikiText-103), they find that for a fixed parameter budget, **increasing depth while reducing width** yields better perplexity—up to a point, after which optimization difficulties arise. This suggests there's a sweet spot where the model is deep enough to capture needed transformations, but not so deep that training becomes unstable.

---

## 🚀 What This Means for Model Designers

1. **Don't blindly favor shallow, wide models** for sequence tasks that involve complex temporal dynamics. Depth may be essential.
2. **If you need parallelism**, design each layer to be as *expressive per layer* as possible. Think about the Lie algebra of your operations: can your layer generate a rich set of infinitesimal transformations?
3. **Consider hybrid architectures**: Some layers could be sequential (for expressive power) and others parallel (for speed). The Lie view helps identify which parts of the transformation need depth.
4. **Monitor approximation error**: The theory gives you a way to estimate whether your model is "deep enough" for the complexity of your task.

---

## Conclusion

The paper "Why Depth Matters in Parallelizable Sequence Models: A Lie Algebraic View" reframes a practical engineering question—how deep should my model be?—into a beautiful mathematical one about Lie groups and approximation. The answer: depth is not arbitrary; it's the **resolution** at which you can approximate continuous transformations of your sequence. If your task's dynamics are complex, you need fine resolution → more depth. Parallelism is great for efficiency, but it doesn't eliminate the fundamental need for compositional depth. So next time you design a sequence model, ask not just "how wide?" but "how deep?"—and think about the Lie algebra of the operations you're stacking. Your model's expressivity may depend on it.

*Paper: arXiv:2603.05573v1*