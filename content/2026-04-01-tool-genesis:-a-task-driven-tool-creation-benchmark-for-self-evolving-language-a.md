# Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agents

Imagine an AI that doesn't just use tools—it *invents* them. "I need to scrape this website, but there's no scraper tool. I'll write one." "This API is too slow; I'll build a caching layer." That's the vision of **self-evolving language agents**: systems that can create, adapt, and maintain their own tools to solve novel tasks. But how do we evaluate whether an agent can truly *create* tools, not just call pre-built ones? Enter **Tool-Genesis**, a new benchmark that tests an agent's ability to generate functional tools from scratch based on task descriptions. This isn't about using a calculator—it's about *building* the calculator when you need it.

---

## 🧰 Why Tool Creation Matters

Most AI agent benchmarks today test **tool use**: given a fixed set of APIs (search, calculator, database), can the agent call them correctly? That's useful, but it's like evaluating a mechanic only on how well they use existing wrenches, not on whether they can forge a new one when the bolt is an odd size.

Self-evolving agents need **tool creation** skills because:
- The world introduces new tools constantly (new APIs, libraries, hardware)
- Tasks can be *out-of-distribution* relative to existing toolkits
- Adaptability requires modifying or combining tools in novel ways
- Long-term autonomy means maintaining one's own toolset

Tool-Genesis shifts the evaluation from "Can you use tools?" to "Can you *make* tools that solve this task?"

---

## 🔬 What Tool-Genesis Actually Tests

The benchmark presents agents with **task descriptions** that imply missing tool functionality. For example:
- *"You need to analyze sentiment of tweets in multiple languages, but you only have a basic English sentiment analyzer. Create a translation tool and integrate it with the analyzer."*
- *"This API returns paginated data with rate limits. Build a robust paginator with retry logic and caching."*
- *"Generate a visual report from these CSV files. Create a charting tool that outputs HTML."*

The agent must:
1. **Design** the tool's interface (input/output schema)
2. **Implement** the tool in code (Python, typically)
3. **Test** the tool on provided examples
4. **Integrate** it into a plan to solve the original task
5. **Maintain** it across multiple episodes (evolution over time)

Success is measured by **functional correctness** (does the tool work?), **efficiency** (reasonable performance), and **generalization** (does it handle edge cases?).

---

## 🧠 Key Innovations in the Benchmark

### 1. **Task-Driven Creation**
Tools are not created in isolation. They're spawned from a *need* in a higher-level task. This forces agents to reason about *why* a tool is needed, not just *how* to implement it.

### 2. **Multi-Granularity Evaluation**
Tool-Genesis evaluates at three levels:
- **Micro**: The tool itself (unit tests, code quality)
- **Meso**: Integration of tool into a multi-step plan
- **Macro**: Long-term maintenance across episodes (bug fixes, extensions)

### 3. **Evolutionary Scenarios**
Some tasks require the agent to *improve* an existing tool it created earlier, mimicking real-world software evolution. Did it refactor? Did it add error handling? Did it optimize?

### 4. **Cross-Domain Tool Reuse**
Agents are tested on whether they can **transfer** a tool created for one domain to a different domain. Example: a JSON parser created for a web-scraping task should be reusable for a log-analysis task.

---

## 📊 Benchmark Composition

Tool-Genesis includes:
- **150 seed tasks** spanning web interaction, data processing, API integration, visualization, and system administration
- Each task has:
  - A clear objective
  - Initial toolset (deliberately missing a crucial capability)
  - Test suite for the created tool
  - Optional constraints (performance, memory, security)
- **3 difficulty tiers**:
  - Easy: Simple utility functions (format conversion, validation)
  - Medium: Multi-step tools with state (paginators, retry loops)
  - Hard: Systems-level tools (proxy servers, compilers, interpreters)

Human expert feasibility: Easy tasks take 10-30 minutes; Hard tasks take 2-4 hours for a skilled programmer.

---

## 🏆 Why This Benchmark Is Needed Now

As language agents become more autonomous, we need to know: can they *innovate*? Tool-Genesis addresses a gap in current evaluation:
- **ToolHUB**: Tests tool *use* with a fixed library; Tool-Genesis tests *creation*
- **API-Bank**: Evaluates API calling; Tool-Genesis evaluates API *design*
- **AgentBench**: Broad agent capabilities; Tool-Genesis isolates tool-making skill

The authors argue that **tool creation is a hallmark of general intelligence**—the ability to invent new affordances to solve novel problems. Without it, agents remain brittle, dependent on pre-packaged tools.

---

## 🧪 Early Results and Surprises

Initial experiments with GPT-4, Claude, and open-source agent frameworks reveal:
- **Baseline agents struggle**: Even simple tool creation tasks have <40% success rates without specialized prompting
- **Chain-of-thought helps**: Explicitly asking "What tool do you need?" improves success to ~55%
- **Few-shot examples of tool code** boost performance to ~70%
- **Full self-evolution** (create → test → debug → refine) remains elusive; most agents need human intervention

Surprisingly, agents often produce *syntactically correct* but *functionally broken* tools—they pass basic linting but fail edge cases. This suggests tool creation requires stronger reasoning and testing loops.

---

## 🚀 Implications for Agent Design

Tool-Genesis points to architectural requirements for self-evolving agents:

1. **Code generation capability**: Must be able to produce executable code in target language (Python)
2. **Testing harness**: Ability to run tests and interpret failures
3. **Tool registry**: Maintain a library of self-created tools with versioning
4. **Retrieval over own tools**: When facing a new task, first check if an existing tool can be adapted
5. **Meta-reasoning**: Decide *when* to create a new tool vs. repurpose old ones

Systems that excel at Tool-Genesis will be more autonomous, require less human pre-engineering, and adapt to novel environments.

---

## Conclusion

Tool-Genesis is more than a benchmark—it's a **call to build agents that can truly invent**. The next generation of language agents shouldn't just be better tool users; they should be tool makers. By evaluating the full lifecycle of tool creation (design → implement → test → maintain → evolve), this benchmark sets a new standard for agentic AI. As we move toward systems that operate independently in open-ended worlds, the ability to forge one's own instruments will separate the brittle from the truly autonomous. Will your agent be a craftsman or just a consumer? Tool-Genesis helps us find out.

*Paper: arXiv:2603.05578v1*