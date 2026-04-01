# Real Faults in Model Context Protocol (MCP) Software: a Comprehensive Taxonomy

You've probably heard of MCP—the Model Context Protocol—as the shiny new standard that lets AI models chat with tools, databases, and other services. It promises to be the "USB-C of AI," unifying how models connect to the world. But as with any rapidly adopted protocol, the rush to implement has led to a blooming garden of software faults. A new paper catalogs these not just as bugs, but as a **systematic taxonomy** that reveals patterns in how MCP implementations go wrong. Understanding this taxonomy isn't just academic—it's a roadmap for building safer, more reliable AI systems.

---

## 🔌 What is MCP, and Why Do Faults Matter?

MCP is a protocol that allows a language model (the "client") to communicate with external tools and data sources (the "server") in a standardized way. Think of it like a universal adapter: one model can talk to many backends—SQL databases, REST APIs, browsers, you name it—without custom code for each. This is huge for building AI applications that are modular, composable, and secure.

But MCP is still young. Implementations are sprouting up everywhere, from open-source projects to enterprise products. And with rapid adoption comes **real-world faults**—security vulnerabilities, crashes, data leaks, and performance nightmares. The paper's goal? To categorize these faults systematically so we can learn from them, prevent repeats, and evolve the spec intelligently.

---

## 📊 The Taxonomy: How MCP Goes Wrong

The authors analyzed dozens of MCP implementations—both client and server—across languages (Python, TypeScript, Go, Rust) and use cases. They identified **four primary fault classes**, each with subcategories:

### 1. **Message Structure Faults**
These are violations of the MCP wire format or JSON-RPC specification.

- **Missing required fields**: E.g., omitting `method` or `params` in requests
- **Type mismatches**: Sending a string where a number is expected
- **Invalid JSON**: Malformed messages that break parsers
- **Frame boundary errors**: In streaming transports, failing to handle message boundaries correctly

Many of these stem from **hand-rolled parsers** instead of using the reference implementations. The authors found that 43% of analyzed servers had at least one structure fault.

### 2. **State Management Faults**
MCP sessions have state—credentials, connection metadata, maybe user context. Faults here lead to leaks, confusion, and security holes.

- **State leakage across sessions**: One user's credentials reused for another
- **Improper cleanup**: Sessions not disposed, leading to zombie connections
- **Race conditions**: Concurrent requests corrupting shared state
- **Resource exhaustion**: Unlimited session creation (DoS vector)

These are particularly nasty because they're often **intermittent** and hard to reproduce.

### 3. **Tool Execution Faults**
The heart of MCP is calling tools. Here faults include:

- **Incorrect parameter binding**: Passing arguments in wrong order or missing required ones
- **Sandbox escape**: Untrusted input leading to code execution (especially in `eval`-style tools)
- **Credential mishandling**: Logging secrets, storing them in plaintext
- **Time-of-check-to-time-of-use (TOCTOU)**: Verifying a condition, then using stale state

The most dangerous ones are **security-critical**: A buggy MCP server that executes arbitrary shell commands is a golden ticket for attackers.

### 4. **Protocol Conformance Faults**
These are deviations from the MCP specification's semantics—not just syntax, but behavior.

- **Incorrect error reporting**: Wrong error codes, missing stack traces
- **Async handling violations**: Not respecting cancellation tokens, hanging indefinitely
- **Capability negotiation failures**: Claiming support for a feature but not implementing it
- **Version mismatch**: Clients and servers using incompatible protocol versions

These faults break interoperability—the whole point of MCP—and are often overlooked because each implementation thinks it's "right."

---

## 🧠 Why These Faults Cluster Where They Do

The taxonomy reveals patterns:

- **Language matters**: Python and JavaScript implementations tend to have more state management issues (dynamic typing, async complexity). Rust and Go implementations have fewer memory safety bugs but more concurrency pitfalls.
- **Size matters**: Small, hobbyist MCP servers (single developer) have higher rates of structure faults. Large, commercial ones have more subtle concurrency bugs.
- **Specification ambiguity**: Where the MCP spec is vague (e.g., "servers should handle errors gracefully"), implementations diverge wildly, leading to conformance faults.

The authors also note **fault coupling**: A structure fault can cascade into a tool execution fault if malformed JSON leads to wrong parameter binding.

---

## 🛠️ What This Means for Builders

If you're implementing an MCP client or server, the taxonomy is a checklist:

1. **Validate messages rigorously** against the JSON-RPC schema—reject, don't crash, on malformed input
2. **Isolate session state**—no sharing between users or connections
3. **Treat tools as untrusted**—sandbox execution, validate all inputs, never log secrets
4. **Test async boundaries**—cancellation, timeouts, concurrent requests
5. **Pin protocol versions** and negotiate capabilities explicitly

For users: **audit your MCP dependencies**. Just because a tool claims "MCP compatible" doesn't mean it's safe. Check for known fault patterns.

---

## 🚀 The Road to More Reliable MCP

The paper's vision is a **fault-informed specification**: future versions of MCP should explicitly document known failure modes and required mitigations. Tooling could include:
- **Conformance test suites** that check for these fault classes
- **Linters** for MCP server code
- **Formal verification** for critical security properties

Until then, the taxonomy serves as a field guide—helping developers recognize, report, and ultimately fix the bugs that are inevitable in any fast-moving protocol.

---

## Conclusion

The Model Context Protocol is poised to become foundational infrastructure for AI applications. But as this taxonomy shows, the current software ecosystem is riddled with avoidable faults—from malformed messages to state leaks to tool execution hazards. By systematically categorizing these faults, the paper gives us a map of the minefield. The next step is to turn that map into better tools, better specs, and better habits. Because the last thing we need is an "AI USB-C" that's just as flaky as the physical one.

*Paper: arXiv:2603.05637v1*