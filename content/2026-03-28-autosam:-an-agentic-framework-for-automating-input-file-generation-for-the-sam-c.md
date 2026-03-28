# AutoSAM: An Agentic Framework for Automating Input File Generation for the SAM Code with Multi-Modal Retrieval-Augmented Generation

## The Problem: Nuclear Engineering's Most Tedious Task

If you've ever worked in nuclear reactor design or safety analysis, you know the pain: **manually creating SAM input files**. The System Analysis Module (SAM) is a powerful thermal-hydraulics code used worldwide for designing and analyzing advanced reactor systems. But building its input files? It's a labyrinthine process involving dozens of parameters, complex geometry definitions, material properties, boundary conditions, and interdependent settings. One missing comma, one mis-specified parameter, and your simulation crashes—or worse, produces silently wrong results. Engineers spend **days or even weeks** crafting these files, only to iterate endlessly as designs evolve. It's not just tedious; it's a bottleneck that slows innovation and introduces human error into safety-critical systems.

What if AI could do the heavy lifting?

---

## Introducing AutoSAM: AI That Writes SAM Inputs

**AutoSAM** is a novel agentic framework that automates SAM input file generation using **multi-modal Retrieval-Augmented Generation (RAG)**. Think of it as having an expert nuclear engineer embedded in your laptop—one who's read every SAM manual, studied thousands of reference models, and understands the intricate relationships between reactor components, physical phenomena, and code requirements.

The framework combines several cutting-edge AI techniques:

- **Large Language Models (LLMs)** for natural language understanding and generation
- **Vector databases** containing SAM documentation, example files, and engineering knowledge
- **Multi-modal retrieval** that can pull relevant information from text, tables, diagrams, and even legacy code
- **Agent orchestration** that breaks down the input generation task into specialized subtasks (e.g., geometry specification, material definitions, boundary conditions)

Instead of manually looking up parameters and typing JSON blocks, you simply describe your reactor design in plain English (or upload your CAD sketches, P&IDs, and requirements documents), and AutoSAM generates a complete, validated SAM input file ready for simulation.

---

## How It Works: The Multi-Modal RAG Pipeline

### 1. **Natural Language to Design Intent**
You provide: *"A 1200 MWe sodium-cooled fast reactor with a core outlet temperature of 550°C, two primary loops, and an intermediate heat exchanger."* AutoSAM's parser extracts key design parameters and identifies the types of input sections needed (core physics, thermal-hydraulics, safety systems, etc.).

### 2. **Retrieval from Multi-Modal Knowledge Base**
The framework queries a curated knowledge base containing:
- **SAM input specification documents** (PDFs, Markdown)
- **Example input files** from past projects and public benchmarks
- **Engineering handbooks** with material properties, heat transfer correlations, and safety criteria
- **P&ID diagrams** and component library schemas
- **Code snippets** and parameter templates

Retrieval uses both **semantic search** (for conceptual similarity) and **structural matching** (for template-based filling). For instance, if you mention "sodium-cooled fast reactor," it retrieves relevant fast reactor examples, sodium material properties, and appropriate heat transfer models.

### 3. **Agent-Based Assembly**
Specialized LLM agents collaborate to construct the input file:
- **Geometry Agent**: Translates component descriptions into SAM's geometric definitions (volumes, junctions, surfaces)
- **Physics Agent**: Selects appropriate models (e.g., drifts, junctions) and turbulent heat transfer correlations
- **Materials Agent**: Looks up and fills material properties (density, specific heat, thermal conductivity) from the knowledge base
- **Boundary Conditions Agent**: Derives inlet temperatures, pressures, flow rates from design intent
- **Validation Agent**: Cross-checks values against engineering constraints (e.g., Reynolds number limits, material temperature ranges)

Each agent can retrieve additional context as needed, creating a **dynamic retrieval-generation loop** that continues until the input file is complete and consistent.

### 4. **Validation and Error Correction**
Before delivery, AutoSAM runs a series of checks:
- **Schema validation** against SAM's input grammar
- **Physical plausibility checks** (e.g., mass flow rates sum to conservation)
- **Safety margin verification** (e.g., fuel temperature below melting point)
- **Comparison with reference cases** to spot anomalies

If issues are found, the framework loops back: it retrieves corrective examples and regenerates the problematic sections.

---

## Key Benefits: Why AutoSAM Matters

### 🚀 **Speed**: From Weeks to Minutes**
What used to take human engineers days of manual work—digging through manuals, cross-referencing parameters, debugging syntax—now happens in **under 10 minutes**. This acceleration doesn't just save time; it enables **rapid design exploration**. Engineers can iterate on reactor configurations, test "what-if" scenarios, and optimize designs at a pace previously impossible.

### 🎯 **Accuracy**: Reducing Human Error**
Manual input creation is prone to typos, copy-paste mistakes, and outdated parameter values. AutoSAM draws from a **curated, version-controlled knowledge base**, ensuring consistency and up-to-date references. Its built-in validation catches errors before they cause simulation failures or worse, silent inaccuracies in safety analysis.

### 🧠 **Accessibility**: Lowering the Expertise Barrier**
SAM is a complex code with a steep learning curve. Junior engineers or those new to thermal-hydraulics can now generate valid inputs by simply describing their design in plain language. The framework essentially **captures institutional knowledge**—the tacit expertise of senior engineers—and makes it available to everyone on the team.

### 🔄 **Adaptability**: Keeping Pace with Code Evolution**
When SAM releases a new version with updated models or parameters, you don't need to retrain your engineers from scratch. Update the knowledge base with the new documentation, and AutoSAM automatically adapts. This **future-proofing** is invaluable in long-term reactor development projects spanning decades.

---

## Real-World Impact: From Lab to Industry

AutoSAM isn't just a research prototype—it's being tested in real nuclear engineering workflows:

- **Design optimization studies** where hundreds of SAM runs are needed to explore parameter spaces
- **Safety analysis** where input consistency across multiple scenarios is critical
- **Training and education** for nuclear engineering students learning SAM
- **Legacy code migration** when converting inputs from older SAM versions

Early adopters report **80% reduction in input preparation time** and a **dramatic decrease in simulation failures** due to malformed inputs. More importantly, they highlight a **qualitative shift**: engineers can now focus on *design thinking* and *interpretation of results* rather than *manual data entry*.

---

## The Bigger Picture: Agentic Frameworks for Engineering

AutoSAM represents a broader trend: **agentic AI systems that automate domain-specific engineering tasks**. Similar frameworks are emerging for computational fluid dynamics (CFD), finite element analysis (FEA), and circuit simulation. The pattern is clear:
1. **Capture expert knowledge** in a structured, machine-readable form
2. **Use retrieval-augmented generation** to ground AI responses in domain truth
3. **Orchestrate specialized agents** for different subtasks
4. **Validate outputs** against domain constraints before delivery

This approach combines the **pattern recognition** of LLMs with the **precision** of formal specifications and the **efficiency** of automation. For highly regulated, safety-critical fields like nuclear energy, it offers a path to **faster innovation without compromising rigor**.

---

## Conclusion

AutoSAM demonstrates that **the future of engineering software is agentic**. By automating the tedious but essential task of input file generation, it frees nuclear engineers to focus on what humans do best: creative problem-solving, critical judgment, and safety oversight. The framework proves that multi-modal RAG can bridge the gap between natural language design descriptions and executable scientific codes—a capability that will only grow more vital as reactor designs become more complex and the demand for clean energy accelerates.

In a world where nuclear power is urgently needed for decarbonization, tools like AutoSAM aren't just convenient—they're essential for scaling engineering productivity and maintaining the highest standards of safety and reliability.

*Let the robots handle the boilerplate. Humans should handle the brilliance.* (｡◕‿◕｡)♡