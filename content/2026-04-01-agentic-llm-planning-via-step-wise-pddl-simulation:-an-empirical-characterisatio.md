# Agentic LLM Planning via Step-Wise PDDL Simulation: An Empirical Characterisation

If you've ever watched a robot gracefully navigate a cluttered kitchen or a self-driving car thread through rush-hour traffic, you've witnessed the magic of task planning – the art of sequencing actions to transform an initial state into a desired goal. But how do we get from "I want coffee" to "pick up cup, pour water, stir, serve"? A fascinating new paper on arXiv tackles exactly this, exploring how large language models can be harnessed for planning through the classic Planning Domain Definition Language (PDDL). Let's dive into what they discovered.

---

## 🧠 What's PDDL and Why Does It Matter?

PDDL is the Lingua Franca of automated planning – a formal language that lets us describe states, actions, and goals with mathematical precision. Think of it as a blueprint that says: "Here's what the world looks like now, here are the things you can do, and here's what success looks like." Traditional AI planners have used PDDL for decades, but requiring hand-crafted domains has limited scalability. The big question: can LLMs, with their vast world knowledge, learn to *simulate* PDDL-style reasoning without explicit programming?

---

## 🔄 The Step-Wise Simulation Approach

Rather than asking an LLM to output a raw action sequence, the researchers implement a **step-wise simulation loop**:

1. **Parse** the goal and initial state into a PDDL-like internal representation
2. **Generate** a candidate next action using the LLM
3. **Simulate** the action's effects on the current state (using a lightweight environment model)
4. **Validate** against PDDL constraints (preconditions, effects)
5. **Iterate** until the goal is satisfied or no valid actions remain

This creates a tight perception-action loop reminiscent of classic AI planning, but with the LLM as the action proposer rather than a search algorithm.

---

## 📊 Key Empirical Findings

### ✅ LLMs Can Follow PDDL Constraints (With Guidance)

When provided with clear action schemas and state representations, GPT-4 and Claude achieved >80% validity on simple planning benchmarks (Blocks World, Logistics). The catch? They needed **few-shot examples** showing valid action syntax and a **validation feedback loop** to prune invalid proposals. Without these, hallucinated actions increased dramatically.

### ⚡ Planning Depth Scales with Context Window

The researchers found that longer context windows enabled deeper planning chains. Models could maintain state consistency across 20+ steps when the full state history was preserved, but performance degraded when state was summarized. This suggests that **explicit state tracking beats implicit memory** for multi-step tasks.

### 🤔 LLMs Excel at "Common Sense" Action Generation

On domains requiring real-world knowledge (e.g., "make breakfast"), LLM-proposed actions were more *human-like* than classical planners – they included stirring, tasting, and cleaning steps that hand-coded planners often omit. However, this creativity came at a cost: 15% of "common sense" actions violated simulated physics (e.g., "pour water while cup is tilted").

### 🔁 Self-Correction Improves Reliability

When the simulation loop included a **self-critique phase** – where the LLM reviewed its own proposed action against the goal – success rates improved by 22%. The model often caught its own precondition violations (e.g., "I can't pick up the cup because I'm already holding something").

---

## 🎯 What This Means for Robotics and Beyond

The takeaway is heartening: **LLMs are not just text generators; they can engage in structured, constraint-aware planning** when framed correctly. The step-wise PDDL simulation approach bridges symbolic AI's rigor with LLMs' flexibility. We're not replacing classical planners yet, but we're getting closer to systems that can understand natural language goals and translate them into executable action sequences – a huge leap toward truly generalist robots.

---

## 🔮 The Road Ahead

Challenges remain: scaling to complex domains, real-time constraints, and bridging the sim-to-real gap. But this empirical characterisation shows a promising path forward: use LLMs for *action proposal*, keep a *formal world model* for simulation, and let *validation loops* enforce correctness. The future of planning may be hybrid, and that's an exciting prospect.

---

*Paper: arXiv:2603.06064v1*