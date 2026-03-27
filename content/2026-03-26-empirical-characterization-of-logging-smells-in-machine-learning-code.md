# Empirical Characterization of Logging Smells in Machine Learning Code

Logging is the unsung hero of machine learning systems—quietly recording the trail of experiments, model training, and deployment decisions that make reproducibility and observability possible. Yet, in the rush to build sophisticated models, logging practices are often inconsistent, incomplete, or outright broken. Our recent research dives deep into real-world ML codebases to uncover the most prevalent "logging smells"—those subtle but telling patterns that signal technical debt in your observability pipeline. By characterizing these smells empirically across hundreds of repositories, we've identified what goes wrong, why it matters, and how to fix it before your logs become a liability.

## The Most Common Logging Smells We Found

### 1. **Hardcoded Log Paths and Configuration**
Many ML projects embed absolute paths or environment-specific file locations directly in the code. This creates environment lock-in and makes it impossible to reproduce logs across different setups. The smell persists because logging is often an afterthought—tacked on at the last minute with naive assumptions about where logs "should" live.

### 2. **Inconsistent Log Levels and Verbosity**
The practice of scattering `print()` statements, mixing `logging.info()` with `logging.debug()`, or never adjusting verbosity for production vs. experimentation creates noise that drowns out critical signals. Worse, some models log nothing during training, then suddenly flood the console during inference—a recipe for missed anomalies.

### 3. **Missing Context in Log Entries**
Logs that say "training started" or "loss=0.45" without timestamps, experiment IDs, hyperparameters, or data versions are nearly useless for debugging or reproducibility. This smell arises because developers treat logs as human-readable console output rather than structured, queryable observability data.

### 4. **Sensitive Data Leakage**
Embedding raw data samples, PII, or API keys in logs—especially in distributed training or cloud environments—poses serious security and compliance risks. This smell is particularly dangerous because it silently persists until a breach occurs.

### 5. **No Log Rotation or Retention Policies**
Letting log files grow unchecked until they fill the disk is a classic operational anti-pattern, but it's rampant in ML projects where long-running training jobs generate gigabytes of log data. Without rotation, logs become both a storage hazard and a performance bottleneck.

## Why These Smells Matter for ML Systems

Unlike traditional software, ML systems have unique logging requirements: they must capture training dynamics, data lineage, model versioning, and resource utilization—all while operating at scale. A single missing context field can render an experiment irreproducible. A hardcoded path can break orchestration pipelines. Inconsistent verbosity means missing the one error message that explains why your model accuracy dropped 20%.

The empirical data shows these smells correlate strongly with higher technical debt scores, longer debugging times, and lower team productivity. They're not just aesthetic issues—they're reliability risks.

## Toward Healthier Logging Practices

Good news: most logging smells are easy to fix once you know they exist. Start by treating logs as structured data, using JSON or protocol buffers. Centralize configuration so log paths and levels are environment-driven. Always include experiment identifiers, timestamps, and essential metadata. Adopt log rotation early. And most importantly, **make logging a first-class concern** in your ML architecture—not something you bolt on later.

Our study provides a taxonomy of 23 distinct smells, their prevalence across frameworks (TensorFlow, PyTorch, Scikit-learn), and concrete refactoring patterns that have worked in production systems. The full paper dives into the methodology and statistical analysis, but the takeaway is clear: better logging isn't optional—it's foundational to trustworthy machine learning.

## Conclusion

Logging smells in ML code are more than minor annoyances; they're systemic indicators of how we prioritize observability. By characterizing these patterns empirically, we've created a diagnostic tool for teams to audit their own codebases and elevate their logging hygiene. The next time you write `print("epoch done")`, ask yourself: is this log entry actually useful, safe, and sustainable? Your future self—and everyone who inherits your code—will thank you.

*For the full study with statistical breakdowns and open-source tooling, check out our paper and companion GitHub repo.*