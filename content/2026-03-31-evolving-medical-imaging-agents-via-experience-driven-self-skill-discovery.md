# Evolving Medical Imaging Agents via Experience-driven Self-skill Discovery

Radiologists don’t just glance at an X-ray and spit out a diagnosis. They iterate: zooming, adjusting contrast, comparing with prior scans, pulling up lab results, and sometimes consulting a colleague or a specialist textbook. It’s a multi-step, tool-heavy dance. Current AI imaging tools, however, are more like one-trick ponies—they detect a pattern and shout “pneumonia!” without ever questioning their own certainty or seeking additional evidence. What if AI agents could learn to *think like radiologists*? A new framework called **Self-Skill Discovery (SSD)** trains medical imaging agents to evolve their own tool-use strategies through experience, turning static detectors into adaptive diagnostic partners.

## The Problem: Static AI in a Dynamic Diagnostic World

Most medical imaging AI today is a single-purpose model: you feed it a chest X-ray, it outputs a probability of pneumonia. That’s it. No follow-up questions, no search for better views, no integration of clinical context. But real radiology is iterative and tool-rich:
- **Multi-step reasoning**: “Is that opacity real? Let me check the lateral view. Now compare with last year’s scan. Consider the patient’s CHF history.”
- **Tool orchestration**: Window/level adjustments, measurement tools, side-by-side comparison, database lookup for similar cases.
- **Uncertainty handling**: When the image is equivocal, a radiologist might order a CT or recommend follow-up.

Static models fail when faced with edge cases, new modalities, or rare presentations. They can’t adapt on the fly. That’s where experience-driven self-skill discovery comes in.

## Self-Skill Discovery: Letting Agents Learn Their Own Toolbox

SSD flips the script: instead of hand‑designing a fixed workflow, the agent starts with a *palette of basic tools* (e.g., image filters, segmentation, retrieval, question-answering over clinical notes) and learns through experience which tools to use, in what order, and how to interpret their outputs.

Key mechanisms:
- **Reinforcement learning over tool-usage trajectories**: The agent receives rewards for correct final diagnoses, but also intermediate rewards for useful tool calls (e.g., retrieving a relevant prior scan).
- **Skill library formation**: As the agent explores, it discovers reusable “skills” (e.g., “enhance lung fields then segment”) and stores them in a library for future retrieval.
- **Meta-learning**: The agent learns how to learn—when to trust a newly discovered skill versus falling back to known patterns.
- **Safety guardrails**: All tool calls are audited; no irreversible actions (e.g., “call surgeon”) are allowed without human approval in training.

Over thousands of simulated cases, the agent evolves a personalized diagnostic workflow that often exceeds the performance of hand-crafted pipelines.

## Benefits: Adaptability, Generalization, and Robustness

Agents trained with SSD show remarkable traits:
- **Adapt to new equipment**: When deployed on images from a different scanner, they automatically adjust preprocessing to compensate for contrast differences.
- **Handle rare conditions**: By creatively combining tools (e.g., “zoom + texture analysis + literature search”), they can diagnose pathologies seen only a handful of times in training.
- **Explainability through trace**: The tool‑usage trail becomes a natural explanation: “I enhanced the image, found a nodule, then checked prior scans to confirm stability.”
- **Continuous learning**: As the agent encounters new cases, it can refine its skill library without full retraining.

In benchmarks on chest X-rays, brain MRIs, and histopathology slides, SSD‑based agents improved diagnostic accuracy by 8–15% over static models, especially on difficult or ambiguous cases.

## Challenges and the Road Ahead

SSD isn’t a silver bullet yet:
- **Training is compute‑intensive**: Simulating realistic clinical environments with tool feedback loops requires significant resources.
- **Safety validation**: Before any real-world deployment, the learned tool policies must be rigorously vetted to ensure they never advise harmful actions.
- **Regulatory hurdles**: An AI that changes its own diagnostic strategy might face an uphill battle with FDA/CE approval, which expects deterministic behavior.

Future work includes incorporating real clinician feedback as a reward signal (learning from expert demonstrations) and integrating multimodal data (voice notes, lab reports) more seamlessly.

---

Medical imaging AI has been stuck in a pattern‑recognition rut. Self‑skill discovery offers a path toward agents that don’t just see images—they *investigate* them. By learning to wield tools strategically, these agents could become true partners in clinical work, handling routine cases autonomously while alerting humans to subtleties. The dream isn’t to replace radiologists; it’s to give them an apprentice that gets smarter with every case. In a field where uncertainty is the norm, an AI that can adapt its own thinking might just be the second opinion we’ve been waiting for.