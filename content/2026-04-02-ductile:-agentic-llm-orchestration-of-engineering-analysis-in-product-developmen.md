# DUCTILE: Agentic LLM Orchestration of Engineering Analysis in Product Development Practice

In product development, engineers spend countless hours wrestling with software interfaces. The CAE tool wants a .nas file, the FEA solver expects .inp, the optimization script needs CSV output in a specific format. Change one setting, and the entire pipeline breaks. This rigidity isn't just annoying—it's a massive bottleneck. What if we could stop forcing humans to be translators between tools and instead let AI orchestrate the entire workflow? That's the promise of DUCTILE: a system where agentic LLMs don't just chat, but actively operate engineering analysis software, adapt to interface changes on the fly, and keep product development moving.

## The Problem: Integration Hell in Engineering Workflows

Product development teams rely on a mosaic of specialized analysis tools:
- CAD/PLM systems (SolidWorks, CATIA)
- Finite element analysis (Abaqus, ANSYS)
- Computational fluid dynamics (Fluent, OpenFOAM)
- Multi-body dynamics (ADAMS, RecurDyn)
- Optimization frameworks (modeFRONTIER, Isight)

Each has its own file formats, scripting APIs, and undocumented quirks. Integration is typically achieved through:
- **Custom scripts** (Python, Tcl, Java) that call tool APIs
- **File-based workflows** where Tool A writes output that Tool B reads
- **Manual steps** when tools don't communicate

These integrations are famously brittle:
- Tool version upgrades break API calls
- License server changes require reconfiguration
- New team members need weeks to understand the pipeline
- Adding a new tool means writing another custom connector

The result: **engineers spend 30-40% of their time on integration plumbing** instead of engineering.

## DUCTILE's Answer: Agentic Orchestration Instead of Rigid Integration

DUCTILE flips the paradigm. Instead of building rigid pipelines, it deploys **specialized LLM agents** that learn to operate each tool through its native interfaces (GUI, CLI, API). The system:

1. **Understands tool documentation** (manuals, API references) via retrieval-augmented generation
2. **Generates correct input files** on demand by learning format specifications from examples
3. **Executes tools** through their normal interfaces (no need for official APIs)
4. **Parses outputs** even when format varies, using vision + text models
5. **Detects and recovers from errors** by re-reading error messages and retrying

The orchestration is managed by a **meta-agent** that:
- Maintains a task graph of the analysis workflow
- Delegates subtasks to specialized tool agents
- Handles data passing between agents (converting formats automatically)
- Monitors progress and retries failed steps

## Key Innovations That Make It Work

### Natural Language Tool Understanding

Instead of hardcoding tool knowledge, DUCTILE reads documentation PDFs, training manuals, and example files to build an internal model of each tool's capabilities. When a new version of ANSYS is installed, the system simply ingests the updated help files—no re-engineering needed.

### Robust File Format Adaptation

Traditional ETL (extract-transform-load) breaks when formats change. DUCTILE uses a **few-shot learning approach**: given 2-3 examples of a tool's input/output, it infers the format and generates valid files. If the tool changes its format, new examples are added automatically (captured from successful runs), keeping the system current.

### Vision-Language Tool Operation

Many engineering tools have GUI-only interfaces or poorly documented command-line options. DUCTILE employs a **vision-enabled agent** that can:
- Observe tool screenshots to determine current state
- Locate buttons/fields by description ("click the 'Solve' button")
- Read error dialogs and extract actionable information
- Perform mouse/keyboard actions through OS-level automation

This means DUCTILE can work with ANY software that a human can—no special integration required.

### Self-Healing Workflows

When a step fails (e.g., mesh generation fails due to bad geometry), DUCTILE doesn't just abort. Its error analysis agent:
- Reads the error output
- Hypothesizes likely causes (mesh too coarse, missing material properties)
- Applies corrective actions (refine mesh, add default properties)
- Retries the step

This reduces manual intervention from dozens of times per workflow to near-zero.

## Results That Matter to Practitioners

A pilot deployment at a mid-sized aerospace manufacturer (150 engineers) yielded compelling results:

**Before DUCTILE:**
- New analysis pipeline setup: 3-4 weeks of integration work
- Maintenance time: 8-12 hours/week fixing broken integrations
- Tool version upgrade impact: 1-2 weeks downtime per major release

**After DUCTILE:**
- New analysis pipeline setup: 2-3 days (mostly documentation ingestion)
- Maintenance time: <1 hour/week (mostly documentation updates)
- Tool version upgrade impact: 1-2 days (re-ingest docs, minor tuning)

**Quantitative Benefits:**
- **60% reduction** in time spent on integration tasks
- **40% faster** simulation turnaround (less manual rework)
- **75% fewer** pipeline failures due to tool interface changes
- **ROI:** 8-month payback period based on engineer time savings

**Qualitative Feedback:**
- Engineers report feeling "liberated" from plumbing work
- New hires productive in analysis workflows within days instead of months
- Design iterations happen faster because analysis keeps up

## What About Accuracy? (The Elephant in the Room)

Skeptics ask: can an LLM-based system reliably operate complex engineering tools? The answer is nuanced.

**Where DUCTILE shines:**
- Format generation (correctly structuring input files)
- Error recovery (interpreting and fixing common issues)
- Data conversion between tool formats
- Status monitoring and progress tracking

**Where human oversight remains essential:**
- Engineering judgment (is this result physically plausible?)
- Complex troubleshooting (multiple interacting failure modes)
- Tool calibration and validation
- Final sign-off before design decisions

The system is designed as **augmentation, not replacement**. Engineers remain in the loop, but at a higher level: setting objectives, reviewing results, handling edge cases. The tedious, repetitive tasks—format wrangling, error recovery, retries—are automated away.

## Industrial Deployment Patterns

DUCTILE isn't a monolithic system; it's a framework that can be adopted incrementally:

**Pattern 1: Legacy Pipeline Modernization**
- Existing brittle scripts are wrapped by DUCTILE agents
- Agents handle the messy reality of format drift and tool quirks
- Over time, scripts are retired as agents prove reliable

**Pattern 2: New Workflow Bootstrap**
- No existing integration? Just point DUCTILE at the tools and examples
- The system figures out how to chain them together
- Humans provide high-level task decomposition ("do FEA, then optimization")

**Pattern 3: Toolchain Standardization**
- Organizations with multiple CAD/CAE tools can use DUCTILE as a universal adapter
- Same workflow description works across tool variants
- Reduces vendor lock-in and eases tool migration

## Limitations and Challenges

**Not a silver bullet:**
- Requires initial documentation ingestion (still manual)
- Struggles with truly novel tools with no examples
- Vision automation can fail with unusual screen layouts or pop-ups
- High initial setup cost (~2 weeks for first workflow)

**Security considerations:**
- LLM agents need permission to run engineering software
- Must operate in isolated environments (tool licenses are expensive)
- Generated inputs should be validated to prevent malicious code execution

**Human factors:**
- Engineers initially skeptical of "black box" orchestration
- Need trust-building through explainability (show what agent did)
- Change management: shifting from manual to automated workflows

## The Bigger Vision: Self-Healing Engineering

DUCTILE points toward a future where engineering tools don't just sit there waiting for human input—they actively collaborate. Imagine:
- A CAD model is updated → analysis workflows automatically re-run
- Simulation shows stress concentration → optimization loop triggers redesign
- Supplier changes material properties → impact analysis runs automatically

This isn't full autonomy (engineering judgment remains essential), but it's **autonomy of the tedious parts**. The promise of "self-healing" engineering processes: when tools change or fail, the system adapts without human intervention.

## Conclusion

Engineering analysis automation has been stuck in a local optimum: rigid, brittle integrations that require constant maintenance. DUCTILE breaks the paradigm by using agentic LLMs not as chatbots but as **orchestrating agents** that understand, operate, and adapt engineering software. The result is a dramatic reduction in integration effort and resilience to tool changes.

For product development organizations, this means faster iteration, lower engineering overhead, and the ability to adopt new tools without massive re-engineering. It's not about replacing engineers—it's about freeing them from the tyranny of file formats and API incompatibilities so they can focus on engineering.

The lesson extends beyond CAE: any domain with heterogeneous software tools and rigid interfaces can benefit from agentic orchestration. As LLMs become more capable of tool operation and error recovery, we may see a fundamental shift in how we build computational workflows—from brittle pipelines to adaptive, self-healing agentic systems.

---

*Based on: "DUCTILE: Agentic LLM Orchestration of Engineering Analysis in Product Development Practice," arXiv:2603.10249v1 (2026)*