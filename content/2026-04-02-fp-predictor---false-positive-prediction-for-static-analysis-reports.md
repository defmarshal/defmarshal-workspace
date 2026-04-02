# FP-Predictor - False Positive Prediction for Static Analysis Reports

You've been there: your CI pipeline runs a security scan, and the report lights up like a Christmas tree—SQL injection! Buffer overflow! Path traversal! You drop everything to investigate, only to discover... it's a false alarm. Again. This is **alert fatigue** from false positives, and it's undermining the entire purpose of SAST (Static Application Security Testing). Teams start ignoring warnings, real vulnerabilities slip through, and security becomes a checkbox exercise. What if we could predict which findings are likely false positives *before* wasting human hours? That's the promise of FP-Predictor, a smart new approach that's about to make your security scans actually useful.

## The SAST False Positive Problem (And Why It's So Bad)

SAST tools (Checkmarx, SonarQube, Fortify, etc.) automatically scan source code for security vulnerabilities. They're essential for catching bugs early, but they come with a crippling flaw: **false positive rates of 50-80%** are common [1].

Consider the impact:
- **Developer frustration**: "Another SQL injection false positive? I'll just mark it as won't fix."
- **Wasted time**: Security engineers spend 60% of their time triaging false alerts instead of fixing real issues [2]
- **Desensitization**: After seeing hundreds of false alarms, teams start ignoring all warnings—including the real ones
- **CI/CD bottlenecks**: Security gates that can't pass due to unfixable false positives slow down releases

Why are SAST tools so prone to false positives? They operate on syntactic patterns without deep understanding of context. A tool sees `String query = "SELECT * FROM users WHERE id = " + userInput;` and flags SQL injection—without knowing that `userInput` is actually validated upstream and sanitized. The tool lacks the semantic context to distinguish real vulnerabilities from benign patterns.

## Enter FP-Predictor: Predicting the False Positives

FP-Predictor takes a radically different approach: instead of trying to make the SAST tool smarter, it **learns to predict which findings are false positives** after the tool has reported them.

Think of it as a **smart filter** that sits on top of your existing SAST pipeline:

```
Source Code → SAST Tool → Raw Findings → FP-Predictor → Filtered, Prioritized Report
```

The system works in two phases:

### 1. Training Phase (Supervised Learning)

Collect historical data from your own codebase:
- **Positive examples**: Findings that were confirmed as true vulnerabilities (after manual review)
- **Negative examples**: Findings that were marked as false positives

For each finding, extract features:
- **Tool-specific**: Rule ID, confidence score, line of code
- **Code context**: Surrounding code patterns, function complexity, data flow
- **Project metadata**: Age of the code, ownership, commit frequency
- **Historical**: Has this pattern caused false positives before in this codebase?

Train a classifier (typically a gradient-boosted tree or lightweight neural network) to predict the probability that a given finding is a false positive.

### 2. Inference Phase (Real-Time Filtering)

When a new SAST scan completes:
1. Extract features for each finding
2. Run FP-Predictor to get false positive probability
3. Filter out findings above a tunable threshold (e.g., >85% probability of false positive)
4. Present the remaining findings with probability scores to help triage

The tool can also suggest which findings to prioritize (high severity, low false positive probability) and which to deprioritize.

## Key Innovations That Make FP-Predictor Work

### Context-Aware Feature Engineering

FP-Predictor doesn't just look at the vulnerability pattern—it examines the **surrounding code ecosystem**:
- Is the vulnerable pattern inside a test file? (likely false positive)
- Is it in a deprecated module that's never called? (likely false positive)
- Does the function have input validation layers? (reduces exploitability)
- Historical fix rate for this rule in this codebase

These contextual signals are missing from traditional SAST tools but are gold for false positive prediction.

### Continuous Learning from Triage Decisions

Every time a developer marks a finding as "false positive" or "true vulnerability" in the triage interface, that feedback is fed back into FP-Predictor. The model **improves over time** as it learns the team's specific codebase patterns and tolerance levels.

This is crucial because what's a false positive in one project may be a real issue in another (different coding conventions, different threat models).

### Project-Specific Adaptation

Unlike generic rule-based filters, FP-Predictor **customizes to each codebase**. A financial services application and a game engine will have different false positive patterns. The model learns these idiosyncrasies automatically from historical triage data.

### Minimal Integration Overhead

FP-Predictor works as a post-processor to any SAST tool that outputs standard formats (SARIF, JSON). No need to replace your existing scanner; just add the filter.

## Results: Real Impact on Security Engineering

The paper evaluated FP-Predictor on three large industrial codebases (2M+ LOC each) with historical triage data spanning 18 months.

### False Positive Reduction

| SAST Tool | Baseline FPR | FP-Predictor FPR | Reduction |
|-----------|--------------|------------------|-----------|
| Checkmarx | 68% | 22% | 46% |
| SonarQube | 59% | 18% | 41% |
| Fortify | 72% | 25% | 47% |

That's **roughly 40-50% fewer false positives** to triage.

### Triage Time Savings

- **Before**: Security engineers spent 15 hours/week triaging SAST findings
- **After**: Reduced to 6 hours/week (60% time savings)
- **Payback**: Less than 2 months based on engineering salary costs

### True Positive Preservation

Critically, FP-Predictor doesn't just filter randomly—it actually **improves precision** while maintaining recall:
- Precision increased from 32% to 78%
- Recall decreased only slightly: 89% → 84%

That means you're filtering out mostly noise while keeping almost all real vulnerabilities.

### Developer Satisfaction

Survey of 45 developers using the filtered reports:
- 82% said the report was "more trustworthy" than before
- 76% reported "less frustration" with security scans
- 68% said they now "pay more attention" to SAST findings

When developers trust the tool, they actually fix the vulnerabilities. That's the ultimate metric.

## How Organizations Can Deploy FP-Predictor

### Getting Started

1. **Collect historical data**: Export SAST findings with triage decisions (true/false) from the past 6-12 months. Need at least 500 labeled examples for decent performance.
2. **Train initial model**: Use FP-Predictor's training script; takes minutes on a laptop.
3. **Integrate into CI/CD**: Add as a post-processing step after SAST scan.
4. **Tune threshold**: Start conservative (filter 20% of findings) and adjust based on feedback.

### Maintenance

- **Retrain quarterly** as codebase evolves and new vulnerability patterns emerge
- **Monitor precision/recall** to ensure model isn't drifting
- **Collect feedback** from triage team to improve continuously

### Customization Options

- **Risk tolerance**: Aggressive filtering (more false positives filtered, risk of missing real issues) vs. conservative
- **Rule-specific thresholds**: Some rules (e.g., hard-coded passwords) have lower false positive rates; can be treated differently
- **Component-specific models**: Train separate models for frontend vs. backend code if patterns differ significantly

## Limitations and When Not to Use It

FP-Predictor isn't a magic bullet:

- **Requires historical data**: New projects with no triage history can't train a model initially. Start with rule-based heuristics and collect data.
- **May miss novel vulnerabilities**: If a new type of bug appears that doesn't resemble historical patterns, the model may not recognize it. Keep some high-sensitivity rules unfiltered.
- **Model interpretability**: While tree-based models are fairly interpretable, you should still review why certain findings are being filtered, especially for compliance reasons.
- **Not a replacement for better SAST**: FP-Predictor mitigates bad tools but doesn't fix the root cause. Continue to improve your primary SAST tool's precision.

## The Bigger Picture: From Alerts to Intelligence

FP-Predictor represents a shift from **raw signal** to **filtered intelligence**. SAST tools will always generate noise—that's inherent to static analysis of complex code. The question is: how do we surface the signal effectively?

This approach could be applied to other security tooling:
- **DAST (Dynamic Application Security Testing)**: Filter false positives from web vulnerability scanners
- **SCA (Software Composition Analysis)**: Predict which dependency vulnerabilities are actually exploitable in your context
- **Container scanning**: Distinguish real misconfigurations from benign findings

The pattern is clear: use machine learning to learn from your own triage history and personalize the security signal.

## Conclusion

False positives aren't just an annoyance—they're a critical barrier to effective application security. They waste time, breed cynicism, and cause real vulnerabilities to be overlooked. FP-Predictor offers a practical, data-driven solution: learn from past triage decisions to automatically filter future noise.

For organizations drowning in SAST alerts, this is a game-changer. You can finally use your security scans with confidence, knowing that what appears in the report is worth your attention. And that means you'll actually fix vulnerabilities before attackers exploit them.

The takeaway is simple: **don't just accept false positives as the cost of doing business**. Use FP-Predictor to reclaim your security engineering time and focus on what matters—finding and fixing real bugs.

Your future self (and your security posture) will thank you.

---

*Based on: "FP-Predictor - False Positive Prediction for Static Analysis Reports," arXiv:2603.10558v1 (2026)*

**References:**
[1] Pearson, S. (2024). "The False Positive Crisis in SAST Tools." *IEEE Security & Privacy*, 22(3), 45-52.  
[2] MITRE. (2025). "SAST Triage Cost Study." internal technical report.  
[3] FP-Predictor: Open-source implementation available at https://github.com/security-ai/fp-predictor