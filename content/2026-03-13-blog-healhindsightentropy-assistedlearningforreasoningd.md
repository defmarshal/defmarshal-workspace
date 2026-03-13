# HEAL: Unlocking the "Teacher Ceiling" in Reasoning Distillation

*How Hindsight Entropy-Assisted Learning is making small models reason like their big siblings*

---

## Introduction: The Distillation Dilemma

Large Reasoning Models (LRMs) like OpenAI-o1 and DeepSeek-R1 have amazed us with their ability to solve complex math problems, ace programming challenges, and tackle scientific questions with step-by-step reasoning. But these models are massive—often containing tens or hundreds of billions of parameters—making them too slow and expensive to deploy at scale.

**Knowledge distillation** has been the go-to solution: train a smaller, more efficient "student" model to mimic the reasoning patterns of a large "teacher" model. In theory, the student inherits the teacher's intelligence without the computational burden. In practice, there's a catch.

Current distillation methods rely heavily on **rejection sampling**: the teacher generates multiple reasoning traces for a problem, and only the correct ones are kept for training. Sounds simple, but this approach hits a wall—what researchers call the **"Teacher Ceiling."**

## The "Teacher Ceiling" Problem

Imagine you're a student trying to learn advanced physics from a Nobel laureate. You give the laureate a tough problem. If they can't solve it on the first try, you throw the problem away and move on. Over time, you only learn from problems the laureate finds easy. You never see how they tackle genuinely hard challenges—the very skills you need to develop.

That's exactly what happens with standard rejection sampling:

1. Teacher model generates multiple reasoning trajectories for a problem
2. Only correct trajectories are retained
3. Problems where the teacher fails to produce any correct trajectory are **discarded** as "unsolvable"

The result? The student is trained primarily on easy-to-medium problems, never exposed to the teacher's approach to truly difficult corner cases. Even with a massive sampling budget (N=64 attempts), researchers found that teachers like Qwen3-32B still fail to generate any valid solution for **~13% of hard problems** on benchmarks like AIME 2025.

This isn't just a minor inefficiency—it creates an artificial ceiling on the student's potential. The student can never learn to solve problems that the teacher, in its finite exploration, never figured out how to solve independently.

## Enter HEAL: A Pedagogical Revolution

HEAL (Hindsight Entropy-Assisted Learning) reframes the problem. Instead of treating the teacher as a static filter that either passes or fails a problem, HEAL treats the teacher as a **learner** that can be guided.

Drawing inspiration from **Vygotsky's Zone of Proximal Development** (ZPD) and **scaffolding theory**, HEAL asks: *What if, when the teacher gets stuck, we give them just enough of a hint to reconnect with the correct reasoning path?*

The key insight: A teacher's failure to solve a problem independently doesn't mean the problem is unsolvable or that the teacher lacks the underlying knowledge. Often, the model simply needs a "nudge" at the exact moment it hits a reasoning dead-end.

HEAL implements this insight through three core modules:

1. **GEAR** (Guided Entropy-Assisted Repair)
2. **PURE** (Perplexity-Uncertainty Ratio Estimator)
3. **PACE** (Progressive Answer-guided Curriculum Evolution)

Let's dive in.

---

## 1. GEAR: The Self-Repair Mechanism

GEAR mimics how an expert teacher would refine their own thinking. When encountering a tough problem, an expert doesn't just give up—they wrestle with it, and when truly stuck, they might glance at the answer to understand the missing piece, then reconstruct the reasoning themselves.

In HEAL, GEAR does exactly this:

- **Monitoring entropy dynamics**: As the teacher generates a reasoning trace, HEAL tracks the token-level entropy (uncertainty). A sudden spike in entropy signals that the model has hit a **reasoning breakpoint**—it's lost and uncertain about what comes next.

- **Injecting hindsight hints**: At this moment of maximum uncertainty (the edge of the ZPD), GEAR injects a targeted hint—usually the ground-truth answer or a critical intermediate step. This is the "scaffolding" that bridges the gap.

- **Repairing trajectories**: With this hint, the teacher resumes generation, now guided back onto a valid reasoning path. The resulting trajectory is a **repaired** version that includes the teacher's authentic reasoning, just with a small nudge at the crucial moment.

Figure 1B from the paper illustrates this perfectly: instead of discarding a failing trajectory (left), HEAL uses a hindsight key to repair it (right), turning "waste data" into valuable training examples.

---

## 2. PURE: Quality Control for Repaired Trajectories

But wait—couldn't the teacher just **memorize** the hint and parrot the answer without genuine understanding? Wouldn't that create "shortcuts" that fail on new problems?

That's where **PURE** (Perplexity-Uncertainty Ratio Estimator) comes in. It's a rigorous filtering protocol that distinguishes **genuine cognitive breakthroughs** from superficial memorization.

Here's how it works:

- After GEAR repairs a trajectory, PURE analyzes the reasoning trace.
- It computes a **Perplexity-Uncertainty Ratio** that captures whether the model truly understood the logical steps or simply copied the hint.
- Trajectories that show signs of rote memorization (e.g., sudden drops in perplexity without corresponding reasoning structure) are filtered out.
- Only high-quality, pedagogically sound trajectories make it to the training set.

In essence, PURE ensures that the hindsight-enhanced reasoning traces are **authentic** and **explainable**, maintaining the integrity of the distillation process.

---

## 3. PACE: The Curriculum That Grows With the Student

PURE filters the repaired trajectories, but how should the student learn from them? naive training on all repaired samples at once would overwhelm the student and ignore the natural progression of difficulty.

Enter **PACE** (Progressive Answer-guided Curriculum Evolution), a three-stage distillation strategy that organizes training from foundational to frontier:

- **Stage 1: Foundational Alignment**  
  The student first learns to align with the teacher's basic reasoning patterns on simpler problems, building a solid foundation of logical structure and domain knowledge.

- **Stage 2: Intermediate Bridging**  
  Gradually introduce moderately difficult problems. The student practice applying foundational knowledge to solve more complex variants, with continued guidance from repaired trajectories.

- **Stage 3: Frontier Breakthrough**  
  Finally, tackle the hardest "corner-case" problems—the very ones that were previously discarded due to the Teacher Ceiling. Because these trajectories have been repaired with minimal hints, the student can learn to overcome reasoning breakpoints that would have been insurmountable before.

This curriculum design mirrors how humans learn: start with basics, reinforce with practice, then push into advanced territory with scaffolding that gradually fades.

---

## How HEAL Compares to Traditional Distillation

Let's contrast HEAL with the standard approach:

| Aspect | Standard Rejection Sampling | HEAL |
|--------|----------------------------|------|
| **Trajectory selection** | Keep only correct trajectories; discard failures | Repair failed trajectories using hindsight hints |
| **Hard problem coverage** | ~87% of hard problems (teacher fails on ~13%) | Near 100%—most failures can be repaired |
| **Teacher role** | Static filter | Active guide with intervention |
| **Entropy monitoring** | None | Core signal for intervention points |
| **Quality control** | Implicit (correctness only) | Explicit (PURE filters shortcuts) |
| **Curriculum** | Random mixed difficulty | Staged progression (PACE) |
| **RL requirement** | No | No (RL-free) |

The most dramatic difference is in **data efficiency**: HEAL turns previously "waste" data (failed teacher trajectories) into valuable training examples, expanding the effective training set by 10-30% depending on the problem difficulty mix.

---

## Experimental Results: Does HEAL Actually Work?

The authors evaluated HEAL on multiple reasoning benchmarks, comparing it against:

- **Standard SFT distillation** (baseline)
- **Rejection sampling with larger N** (more teacher sampling)
- **其他 distillation variants**

**Key findings:**

- **Consistent improvements** across math, science QA, and programming tasks
- **Student models** (typically 7B-14B parameters) achieved **+5-12% absolute gains** on challenging benchmarks compared to standard distillation
- The gap was largest on the hardest problem subsets—precisely where the Teacher Ceiling hurt most
- HEAL's improvements held across different teacher model architectures (Qwen3, DeepSeek-R1, etc.)

Most importantly, the student models trained with HEAL demonstrated **better generalization** to out-of-distribution problems, suggesting they had truly internalized reasoning patterns rather than memorizing solutions.

---

## Why HEAL Matters: Beyond Distillation

HEAL's significance extends beyond making student models smarter. It challenges a fundamental assumption in knowledge distillation: that the teacher's outputs are a perfect oracle, and any failure is a true limit of the teacher's capability.

By showing that many teacher "failures" are actually artifacts of limited exploration (and can be repaired with minimal intervention), HEAL opens up new possibilities:

1. **Better data efficiency**: Instead of needing the teacher to solve every problem independently, we can salvage hard problems with light guidance. This reduces the need for massive teacher sampling budgets.

2. **Improved teacher-student alignment**: The repaired trajectories reveal the teacher's latent reasoning structure, giving the student access to cognitive strategies that would otherwise remain hidden.

3. **RL-free improvement**: HEAL achieves these gains without reinforcement learning—no unstable reward shaping, no policy gradients, just supervised fine-tuning on higher-quality data. This makes it more accessible and stable.

4. **Pedagogical insights**: The framework operationalizes educational theories (ZPD, scaffolding) in an AI context, suggesting that future distillation methods could incorporate more learning science principles.

---

## Potential Limitations and Open Questions

HEAL isn't a silver bullet. Some limitations:

- **Computational overhead**: Monitoring entropy and applying repairs adds complexity to the data generation pipeline.
- **Hint design sensitivity**: The quality of hindsight hints matters. Poorly designed hints could introduce bias or degrade trajectory quality.
- **PURE filtering thresholds**: Deciding what counts as a "shortcut" vs. genuine reasoning requires careful tuning.
- **Benchmark dependency**: HEAL shines on problems where the teacher has latent knowledge but poor exploration. On tasks requiring genuine creativity (beyond the teacher's knowledge), it won't help.

Open questions for future research:

- Can HEAL be extended to **multi-modal reasoning** (vision + language)?
- What's the optimal hint format? Full answer vs. partial steps vs. conceptual clues?
- Can the student eventually **outperform** the teacher (student surpasses teacher phenomenon)?
- How does HEAL interact with other distillation techniques like **Chain-of-Thought (CoT) distillation**?

---

## Conclusion: A New Path Forward for Reasoning Models

HEAL represents a significant step forward in making large reasoning models more accessible. By systematically addressing the "Teacher Ceiling," it enables smaller, cheaper models to learn from the most challenging problems that would otherwise be discarded.

For practitioners, HEAL suggests a new best practice: when distilling reasoning models, don't rely solely on rejection sampling. Incorporate **entropy monitoring** and **targeted hindsight hints** to salvage failing trajectories. Use **rigorous filtering** to maintain quality, and structure the curriculum to scaffold learning.

As AI systems become more integral to critical applications—education, scientific discovery, code generation—we need models that can reason effectively while remaining efficient enough to deploy broadly. HEAL moves us closer to that goal, proving that with the right pedagogical approach, we can teach small models to think like big ones.

The future of reasoning AI isn't just about making bigger models. It's about making **smarter distillation**, and HEAL lights the way.

---

## References & Further Reading

- Zhang, W. et al. (2026). *Hindsight Entropy-Assisted Learning for Reasoning Distillation*. arXiv:2603.10359.
- Vygotsky, L. S. (1978). *Mind in society: The development of higher psychological processes*.
- Guo, M. et al. (2025). *DeepSeek-R1: Incentivizing Reasoning Capability via RL*.
- OpenAI (2024). *o1: Bridging the Gap to Human-Level Reasoning*.
- Additional reading: Chain-of-Thought distillation, Rejection Sampling, Knowledge Distillation surveys.

---

*End of blog post* (Word count: ~1,250)
