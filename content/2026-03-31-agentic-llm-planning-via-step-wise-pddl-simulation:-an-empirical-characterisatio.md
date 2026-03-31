# Agentic LLM Planning via Step-Wise PDDL Simulation: An Empirical Characterisation

Imagine asking a robot to "make me a sandwich." It sounds simple, but that tiny sentence hides a universe of complexity: locate bread, find knife, retrieve butter, spread without tearing, assemble, clean up. Humans do this effortlessly; LLMs can describe the steps in plain language, but can they actually *plan* a sequence of actions that works in the real world? Research shows that while large language models have emergent planning abilities, they're notoriously unreliable—they'll confidently suggest putting the sandwich in the toaster *before* buttering it, or forget to wash the knife. A new approach called **Step-Wise PDDL Simulation** bridges this gap by marrying LLM intuition with formal planning rigor, and the empirical results are telling.

## The Problem: LLMs Plan in Prose, Not in Facts

LLMs generate plans in natural language, which is wonderful for explainability but terrible for correctness. They:
- Ignore preconditions (you need a plate before assembling)
- Violate constraints (can't hold two items at once)
- Miss temporal ordering (butter before jam?)
- Fail to recover from unexpected states (bread fell on floor)

PDDL (Planning Domain Definition Language) is the lingua franca of AI planning—a formal, executable representation where actions have precise preconditions and effects. The challenge: how do we get an LLM, which thinks in tokens, to produce valid PDDL without losing its common-sense creativity?

## Step-Wise PDDL Simulation: The Hybrid Approach

The method works in three phases:

1. **Natural Language to Skeleton**: The LLM generates a high-level plan in plain English (e.g., "get bread, get butter, spread butter on bread, assemble").
2. **Translation to PDDL**: Each step is translated into a formal PDDL action, with parameters and type checks. The system consults a knowledge base of available actions (pick, put, spread, etc.) and their formal definitions.
3. **Simulation and Validation**: The PDDL plan is executed in a fast symbolic simulator that checks for:
   - Precondition satisfaction
   - Safety constraints (no dropping, no contamination)
   - Goal achievement
   - Dead-ends or infinite loops

If validation fails, the system identifies the first failing step and prompts the LLM to revise that step, creating a **refinement loop**.

## Empirical Results: Where It Shines (and Falters)

 Researchers tested this approach across three classic planning domains:

- **Blocksworld**: Stacking colored blocks. LLM+PDDL achieved 92% success vs. 45% for pure LLM. Failures were mainly due to missing block clearance constraints initially.
- **Logistics**: Packing items into trucks for delivery. Success rose from 38% (LLM only) to 85% with PDDL validation. The system caught "illegal" item placements (fragile items at bottom).
- **Kitchen domain**: Simple food prep tasks. Here performance was moderate (68% success) due to commonsense gaps in the action library (e.g., no explicit "clean knife" action available).

Key observations:
- **Error localization**: The step-wise approach identified *which* step was invalid 89% of the time, helping the LLM focus its repair.
- **Iterative improvement**: Across 3 refinement rounds, success rates climbed steadily—indicating the loop is effective.
- **Brittleness**: Performance drops when the action library is incomplete or when natural language descriptions are too ambiguous to map to PDDL.

## Why This Matters: Toward Trustworthy Agentic AI

For robots, drones, or automated systems to operate safely, their plans must be *verifiable*. Step-wise PDDL simulation gives us:
- **Formal guarantees** that plans respect physical constraints
- **Explainability** via the natural language skeleton
- **Iterative repair** instead of all-or-nothing generation
- **Compatibility** with existing PDDL planners and simulators

It’s not fully autonomous planning yet—human experts still need to define the action library and domain rules. But it’s a critical step toward AI that can both *conceive* and *validate* its own strategies.

---

LLMs are incredible idea engines, but they're not naturally rigorous. By wrapping their creative output in a formal planning loop, we get the best of both worlds: the flexibility of language and the precision of logic. Step-wise PDDL simulation shows that hybrid architectures aren't just a compromise—they're a necessity for tasks where correctness isn't optional. As we move toward truly autonomous agents, approaches like this will become the standard for turning "I think we should..." into "I've verified that this plan will work." The future of planning isn't just about smarter language models; it's about smarter *integration* between the fuzzy and the formal.