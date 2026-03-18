# Design-Specification Tiling for ICL-based CAD Code Generation

Large language models have taken the coding world by storm, writing everything from simple scripts to complex applications with impressive fluency. But when it comes to specialized domains—like Computer-Aided Design (CAD)—these models hit a wall. The gap between "write a function that sorts a list" and "generate precise CAD geometry code from a design spec" is huge. That's where a clever new approach called **design-specification tiling**, powered by ICL (Intermediate Cone Layout), comes in to bridge the divide.

## The Problem: LLMs Stumble on Domain-Specific Code

CAD code isn't just any code. It's a highly structured, mathematically precise language that describes physical shapes, dimensions, tolerances, and manufacturing constraints. General-purpose LLMs, trained on vast corpora of software code, simply haven't seen enough CAD examples to develop the deep intuition needed. They often produce code that looks plausible but fails in practice—missing geometric constraints, mixing up units, or violating design rules. This isn't just a minor inconvenience; in engineering contexts, a single error can lead to costly manufacturing failures.

## The Insight: Tile the Specification, Not Just the Code

The core innovation is to stop asking the LLM to generate the final CAD code directly from a high-level design description. Instead, the authors propose **tiling** the design specification into a structured intermediate representation (the ICL). Think of it like an architect's detailed blueprint before the construction crew arrives. The ICL breaks down a complex design into a sequence of logical geometric operations—extrusions, rotations, cuts, constraints—each expressed in a consistent, LLM-friendly format. The model then generates code *for each tile* independently, stitching together a correct final program from reliable pieces.

## Why ICL Works: A Language LLMs Can Actually Grasp

ICL (Intermediate Cone Layout) serves as a lingua franca between human design intent and machine-executable CAD code. It's designed to be:

- **Explicit**: Every geometric operation is spelled out clearly, with named parameters and well-defined relationships.
- **Compositional**: Tiles can be nested, reused, and validated in isolation before integration.
- **LLM-optimized**: The syntax avoids ambiguous phrasing and mirrors patterns commonly found in code.

By converting the natural language spec into ICL first—a step that can be rule-based or lightly supervised—the LLM's job becomes much simpler: translate a clean, structured intermediate language into target CAD code (like OpenSCAD, SolidWorks API, or Python CAD libraries). This two-stage pipeline dramatically reduces hallucination and improves correctness.

## Results: Better Code, Fewer Errors

In evaluations on CAD generation benchmarks, the tiling approach significantly outperformed direct LLM prompting. Models using design-specification tiling with ICL produced:

- **Higher functional correctness**: More generated code compiled without errors and produced the intended geometry.
- **Reduced hallucination**: Fewer spurious operations or invalid parameters.
- **Better generalization**: The approach works across different CAD target languages and scales to more complex designs.

The gains were consistent across several LLM backbones, suggesting the method is model-agnostic and relies on the structural clarity of the tiling itself.

## The Bigger Picture: Structured Intermediaries as a New Paradigm

What's really exciting is that this isn't just a CAD trick—it's a blueprint for tackling other domain-specific code generation problems. Whether it's SQL queries, hardware description languages (Verilog/VHDL), or mathematical simulation code, the principle is the same: **introduce a well-defined intermediate representation that captures domain semantics in a way LLMs can reliably translate**.

Instead of fighting the LLM's statistical nature, we work with it: give it a structured scaffold, and let it fill in the final syntax. This keeps the model in its comfort zone (pattern-matching and translation) while ensuring the output adheres to strict domain constraints.

## Conclusion

Design-specification tiling with ICL shows that the future of specialized code generation may lie not in bigger models alone, but in smarter pipelines. By decomposing complex specs into manageable, well-specified tiles, we can make LLMs truly useful in high-stakes engineering domains. It's a reminder that sometimes the best way to advance AI isn't to scale up—but to **tile down** and build a solid foundation. (◕‿◕)♡