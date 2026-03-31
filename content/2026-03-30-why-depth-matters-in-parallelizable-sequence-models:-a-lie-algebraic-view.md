# Why Depth Matters in Parallelizable Sequence Models: A Lie Algebraic View

We live in an era where Transformers and state-space models (SSMs) dominate sequence processing—and for good reason. They parallelize beautifully across sequences, making training on million‑token documents a breeze. But there’s a subtle cost: in our rush for speed, we often sacrifice *expressivity power*. That nagging question—could we have both?—has been lurking in the background. A fresh perspective from **Lie algebra** now shines a light on why *depth* is the unsung hero that lets parallelizable models have their cake and eat it too.

## The Hidden Trade-Off: Speed vs. Expressivity

Sequence models like the vanilla Transformer achieve lightning‑fast training by processing all tokens in parallel. However, this convenience comes with a mathematical constraint: the per‑token transformations are shallow (often linear projections plus a few non‑linearities). Such shallow operations, when composed across layers, may not fully capture the complex, long‑range dependencies that deeper, recurrent architectures naturally model. In other words, parallelism can flatten the model’s ability to represent intricate functions. Recognizing this trade‑off is the first step toward designing better architectures.

## A Lie Algebraic Lens: Modeling Transformations as Manifolds

Lie algebra enters the story by treating each layer’s transformation as an *infinitesimal* element of a continuous group. When you stack many such layers, their combined effect is like integrating a vector field along the depth axis—a path on a manifold. This viewpoint reveals that *depth* corresponds to the “length” of that integration path. Sufficient depth allows the model to reach regions of the function space that shallow, parallelizable layers simply cannot. The key insight: parallelizability (across sequence) and expressive depth (along layers) are orthogonal dimensions; you can have both if you build deep enough.

## Depth Restores Expressivity Without Breaking Parallelism

Here’s the beautiful part: because each layer’s operation remains parallelizable across tokens, adding more layers *doesn’t* reintroduce sequential computation. You simply increase the number of parallel layers. The Lie algebraic analysis shows that the expressive gap between a deep parallelizable model and a theoretically ideal sequential model is proportional to the *integral of the Lie bracket* along the depth path. In plain English: deeper parallel models can approximate the same function class as recurrent ones, provided we let them grow sufficiently deep. This flips the narrative—depth isn’t the enemy of parallelism; it’s its enabler.

## Practical Takeaways: Build Deeper, Design Smarter

For practitioners, the message is clear: when you’re hitting performance walls with a shallow Transformer or SSM, don’t immediately reach for recurrence. Try adding more layers first. But depth alone isn’t a silver bullet; the Lie algebra perspective also suggests we optimize the *path* of transformations—for instance, using residual connections to smooth the integration, or designing layer types with richer Lie brackets (e.g., rotating, shearing transformations). The goal is to maximize the expressive “distance” traveled per layer while keeping computations parallelizable.

## Conclusion: Embracing Depth in the Age of Parallelism

The drive for parallelizability has led many to flatten their sequence models, sometimes at the expense of capability. Lie theory reminds us that depth is not an anti‑pattern—it’s a fundamental lever for expressivity. By understanding the geometric meaning of layer composition, we can build models that are both fast *and* powerful, finally reconciling scalability with representational richness. So next time you design a sequence model, ask not “how shallow can I go?” but “how deep can I afford to go while staying parallel?” The answer may just lie in the algebra.