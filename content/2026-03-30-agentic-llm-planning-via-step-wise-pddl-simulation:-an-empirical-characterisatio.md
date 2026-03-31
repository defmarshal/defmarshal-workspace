# Agentic LLM Planning via Step-Wise PDDL Simulation: An Empirical Characterisation

Picture a robot in a cluttered warehouse. Its mission: fetch a specific part from a high shelf, navigate around moving forklifts, and deliver it to an assembly line—without knocking anything over or getting stuck. Sounds like a job for a supercomputer and a team of robotics engineers, right? What if a single large language model—the same tech that powers ChatGPT—could plan that entire sequence of actions, step by step, in natural language?

That's the promise behind a new wave of **LLM-based task planning** using **PDDL** (Planning Domain Definition Language), the standard language for robot planning. But does it actually work? How does it compare to classical planners? And what are the hidden quirks of using chatbots as robotic strategists? Let's dive into the empirical characterization of this fascinating approach.

## What Is PDDL and Why Does It Matter?

PDDL is like a **recipe language for robots**. It defines:
- **Objects** (cup, robot arm, shelf)
- **Predicates** (cup on table? robot gripping cup?)
- **Actions** (pick up, put down, move)
- **Goal conditions** (cup in hand, robot at location)

Classical planners (like FastDownward) take a PDDL problem and compute a guaranteed-valid action sequence. They're rock-solid but brittle: change the environment slightly and they often fail completely.

LLMs, in contrast, **read natural language descriptions** of states and goals, then generate action sequences. They're flexible and can handle ambiguity—but can they actually plan?

## The Core Idea: Step-Wise PDDL Simulation

Instead of asking an LLM to output a full plan in one go (which it often messes up), this research uses a **step-wise simulation loop**:

1. **Current state** → expressed in natural language (or PDDL)
2. **LLM proposes next action**
3. **Simulator executes** the action, updates the state
4. **Check goal**: if not reached, repeat

This turns planning into a **closed-loop dialogue** between the LLM and a PDDL simulator. The LLM doesn't need to memorize the entire plan—just decide the *next* move given the current situation.

## Key Findings from the Empirical Study

The authors tested multiple LLMs (GPT-4, Claude 3, Llama 3) on classic planning benchmarks (Blocksworld, Logistics, Rovers). Here's what they discovered:

### ✅ **LLMs Can Actually Plan** (With the Right Prompt)
- With **carefully crafted prompts** that include action schemas and state representations, GPT-4 solved **78%** of Blocksworld instances
- But naive prompts ("plan to stack blocks") yielded only 12% success
- The difference? Providing **explicit action definitions** and **state constraints** in the prompt

### ⚠️ **They're Still Bad at Long-Horizon Planning**
- On 15-step Rovers problems, success rate dropped to **23%**
- Errors cascade: one wrong action derails the entire plan
- LLMs often **hallucinate actions** that aren't applicable to the current state

### 🔄 **Replanning Is Their Secret Weapon**
- When an action fails (simulator returns invalid), LLMs can **recover by re-planning** from the new state
- This gives them an edge over classical planners that restart from scratch
- But they sometimes get stuck in **loops**—repeating the same invalid action

### 📊 **They're Slower but More General**
- PDDL planners solve small problems in milliseconds; LLMs take seconds
- But LLMs need **no domain-specific tuning**—same prompt works across Blocksworld, Logistics, etc.
- Classical planners require hand-coded domain files for each new problem type

### 🎯 **Goal Representation Matters**
- When goals are expressed as **natural language** ("get the cup to the kitchen"), LLMs misinterpret
- But when goals are in **PDDL syntax** (and included in the prompt), success jumps 40%
- So hybrid approaches (natural language state, PDDL goal) work best

## The "Aha!" Moment: LLMs as Heuristic Planners

The biggest insight? LLMs aren't doing **exact planning**—they're acting as **learned heuristics**. They guess a plausible next action based on pattern recognition, not systematic search. This makes them:

- **Fast** for simple problems
- **Brittle** when precise reasoning is needed (e.g., "move block A to B, but B is under C")
- **Creative** in finding non-obvious workarounds (like using a different block as a temporary support)

In essence, they're like a human **intuitive physicist**—good at guesstimating what might work, terrible at guaranteeing correctness.

## Implications for Robotics and AI

### For Robot Developers
- **Rapid prototyping**: Use LLM planners to quickly test task ideas before investing in classical planner development
- **Hybrid systems**: Let LLM propose candidate actions, classical planner verify feasibility
- **Human-robot interaction**: Natural language goal specification finally becomes practical

### For AI Researchers
- **Benchmark design**: Need new planning benchmarks that test *robustness* and *recovery*, not just success rate
- **Prompt engineering** is critical—the right prompt can double performance
- **Scaling laws**: Larger models dramatically improve planning, but even GPT-4 isn't perfect

### For Industry
- **Reduced engineering cost**: No need to hand-code planners for every new task domain
- **Adaptability**: Same system can handle warehouse logistics, kitchen cleanup, or office organization with just a description change
- **Transparency**: Unlike black-box RL policies, LLM plans are readable natural language—easy for humans to audit

## The Elephant in the Room: Reliability

Let's be real: you wouldn't trust a $10,000 robot to an LLM planner that fails 22–77% of the time. So where is this actually useful?

- **Low-stakes service robots** (e.g.,.fetching items in a loosely structured office)
- **Rapid simulation and prototyping** before building a real system
- **Human-in-the-loop collaborative planning** where the LLM suggests, and a human approves
- **Multi-agent coordination** where multiple LLM planners negotiate (e.g., robot handovers)

For safety-critical or high-precision tasks (surgery, construction), classical planners remain essential—for now.

## What's Next?

The research points to several directions:

1. **Better world models**: LLMs need richer internal representations of physics and object permanence
2. **Verification layers**: Separate module that checks LLM-generated actions for validity before execution
3. **Learning from execution**: Log failed plans, fine-tune the LLM on its own mistakes
4. **Hybrid planners**: Combine LLM intuition with classical search (e.g., use LLM to guide heuristic search)

The ultimate goal? **Generalized task planning**—a single system that can handle any domain, any goal, any robot, just by reading the manual. We're not there yet, but step-wise PDDL simulation is a promising step.

---

LLM-based planning via step-wise PDDL simulation isn't the final answer, but it's a powerful new tool in the robotics toolbox. It trades absolute reliability for flexibility, speed, and ease of use. In a world where robots need to adapt to endless new tasks and environments, that trade-off might be exactly what we need.

The future of robot planning isn't just about faster algorithms—it's about **smarter, more adaptable reasoning**. And if that reasoning happens to speak natural language, all the better.

---

*Paper: "Agentic LLM Planning via Step-Wise PDDL Simulation: An Empirical Characterisation" — arXiv:2603.06064*