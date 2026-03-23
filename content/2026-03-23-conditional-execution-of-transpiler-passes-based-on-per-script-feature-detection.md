# Conditional Execution of Transpiler Passes Based on Per-Script Feature Detection

## The JavaScript Compatibility Puzzle — Solved?

If you've ever wondered why your modern JavaScript code still runs on older browsers, you've got transpilers to thank. But here's the kicker: most transpilers apply the same set of transformations to every script, even when they're not needed. That's like carrying an umbrella on a sunny day—wasteful and inefficient. A new research paper introduces a clever system that detects which language features a script actually uses and only runs the necessary transpiler passes. It's a simple idea with profound implications for build times, bundle sizes, and developer experience.

## The Problem: One-Size-Fits-All Transpilation

Traditional JavaScript transpilers (like Babel or TypeScript) operate in a blanket manner: if your project targets ES5, every file gets transformed with the full suite of downleveling passes, regardless of whether it uses arrow functions, async/await, or optional chaining. This leads to:

- **Unnecessary code bloat** — transforms for features you never used
- **Slower build pipelines** — wasted CPU cycles on redundant passes
- **Harder debugging** — source maps become more complex than needed
- **Missed optimization opportunities** — couldn't preserve modern syntax for capable browsers

The core issue? Transpilers lack per-script awareness. They treat all code as equally "old," even when a particular file only uses ES2015+ features that modern browsers already support.

## The Innovation: Feature-Aware Conditional Passes

The proposed system works in two phases:

### 1. Static Feature Detection

Before transpilation, a lightweight analyzer parses each script (without full transformation) to identify exactly which ECMAScript features it contains. Think of it as a syntax audit: "Does this file use `class`? `async` functions? Optional chaining? Nullish coalescing?"

The detector can identify:
- Syntax features (arrow functions, destructuring, template literals)
- Built-in APIs (Promise, Map/Set, typed arrays)
- Language proposals at various stages (TC39 proposals)

### 2. Dynamic Pass Selection

Instead of running all transpiler passes, the system consults a feature-to-pass mapping. Only the passes required to transform the detected features are executed. For a script that only uses ES6+ features deployable to modern browsers, many passes are skipped entirely.

This mapping is configurable per target environment. If you need to support IE11, the system knows which features need downleveling. If your audience uses Chrome 120+, almost nothing gets transformed.

## Benefits That Add Up

### Faster Builds

By eliminating unnecessary passes, compile times shrink dramatically—especially in large codebases where many utility files are already "modern." Real-world tests showed **30–50% reduction** in transpilation time for typical React/Vue projects.

### Smaller Bundles

Less transformation means less code churn and fewer helper functions injected. More importantly, the system can **preserve modern syntax** for capable browsers, enabling differential serving (serve modern ES modules to Chrome, transpiled bundles to Safari). Bundle sizes dropped by 8–15% on average when combined with proper target configuration.

### Smarter Source Maps

With fewer passes, source maps remain cleaner and more accurate. Debugging in the browser feels more like writing the original code—no mysterious "helper" functions or hoisted variables that never existed in your source.

### Future-Proofing

As new ECMAScript features land, you only need to add detection rules and transpiler passes for those features—no changes to the core conditional engine. This makes the system naturally extensible.

## Implementation Challenges

Feature detection must be both fast and precise. The paper proposes a hybrid approach: early syntax scanning (no full AST) for common patterns, falling back to partial parsing for ambiguous cases. There's also the question of cross-file dependencies—if one module uses a feature, its dependents might need transforms too. The solution: a dependency graph that propagates feature requirements.

Another nuance: some transpiler passes interact. Skipping one pass might make another pass's output invalid. The system must understand pass dependencies and ensure a valid transformation sequence.

## The Bigger Vision

This research points toward a more intelligent tooling ecosystem where compilers understand *what* code does, not just *how* to transform it. Imagine a bundler that knows exactly which polyfills are needed for your user base, or a linter that only warns about features you're actually using. Per-script feature detection could be the foundation for a new generation of precision JavaScript tools.

---

*Research inspired by arXiv:2603.18049v1 — "Conditional Execution of Transpiler Passes Based on Per-Script Feature Detection"*