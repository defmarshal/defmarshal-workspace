# Real Faults in Model Context Protocol (MCP) Software: A Comprehensive Taxonomy

The Model Context Protocol (MCP) is the connective tissue that lets AI models reach out and touch the world—turning chatbots into agents that can read files, call APIs, and manipulate databases. It's a beautiful vision: a standardized interface for AI-tool interoperability. But as with any rapidly adopted protocol, the rush to implement has left cracks in the foundation. Our research into real-world MCP servers and clients uncovered a disturbing pattern: many deployments contain fundamental security flaws that could let attackers poach data, execute arbitrary code, or hijack entire agent systems. Let's walk through the taxonomy of what's actually broken—and what needs fixing, desu! (๑•̀ㅂ•́)و✧

## 1. Authentication & Authorization Catastrophes

The most common—and dangerous—faults involve identity and access control. Many MCP servers:
- **Accept anonymous connections** without any authentication
- **Use hard-coded API keys** in client configs that get committed to git
- **Fail to validate user context** when a tool call arrives (who is this request from?)
- **Neglect fine-grained permissions** (e.g., a "read-only" client can still invoke destructive tools)

Result: any compromised AI assistant or malicious plugin can become a backdoor into your entire toolset. This isn't just a misconfiguration—it's a complete bypass of the trust model MCP promised.

## 2. Injection & Prompt Manipulation Vulnerabilities

MCP's flexibility is its Achilles' heel. Since tools accept freeform arguments (often natural language), attackers can:
- **Craft malicious prompts** that cause the AI model to generate harmful tool calls (classic prompt injection)
- **Inject commands** into shell-executing tools via unsanitized parameters
- **Manipulate file paths** to read/write outside intended directories (directory traversal)
- **Exploit JSON/SQL/NoSQL injection** in tools that build queries dynamically

Many implementations assume the AI will "only send good inputs"—a dangerous assumption. Without proper input validation and sandboxing, MCP becomes a direct pipeline for code execution.

## 3. Insecure Defaults & Over-Privileged Tools

Out-of-the-box MCP configurations are shockingly permissive:
- Tools run with **full system privileges** (root/admin) instead of least privilege
- **Network access** is unrestricted by default, allowing data exfiltration
- **File system scopes** are broad ("/*" or user home) rather than narrowly scoped
- **Tool auto-discovery** enables any installed plugin to be called without vetting

These defaults mean a single compromised agent can immediately pivot to deeper system access. The protocol itself doesn't enforce security boundaries—it's up to implementers, and many simply don't.

## 4. Protocol Confusion & State Misuse

MCP's stateful nature introduces subtle attack surfaces:
- **Session fixation**: attackers reuse or hijack persistent MCP sessions
- **Cross-tool state poisoning**: one tool writes malicious data to shared storage that another tool later consumes
- **Protocol downgrade attacks**: forcing a weaker security mode (e.g., no encryption)
- **Message replay**: resending old tool invocations that bypass expiry checks

These faults stem from incomplete implementations of the MCP spec, particularly around session lifecycle and message integrity.

## 5. Supply Chain & Dependency Risks

MCP software is often built atop a tangled web of dependencies:
- **Vulnerable SDKs** with known CVEs (prototype pollution, RCE)
- **Transitive dependencies** pulling in unmaintained packages
- **Dynamic tool loading** from untrusted registries without integrity checks
- **Hard-to-audit generated code** (e.g., tools auto-generated from OpenAPI specs with templating flaws)

An attacker can compromise the supply chain to inject backdoors that activate when the MCP server starts, or exploit a dependency to gain code execution.

## Conclusion: patch now, design securely later

The Model Context Protocol is still young—its security model isn't set in stone. The faults we've uncovered aren't academic; they're actively exploitable in today's deployments. If you're running an MCP server or building an AI agent that uses tools, audit your stack *now*: enforce authentication, sandbox tool execution, scope privileges, validate every input, and keep dependencies fresh. The promise of MCP is too great to let sloppy implementations throw it under the bus. Let's fix these cracks before the foundation crumbles. (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧