```markdown
# A Two-Stage Architecture for NDA Analysis: LLM-based Segmentation and Transformer-based Clause Classification

If you've ever signed a Non-Disclosure Agreement (NDA), you know the feeling: page after page of dense legalese, each clause designed to protect one party or the other. For businesses, reviewing these documents is a necessary evil—lawyers spend hours (or even days) parsing clauses about confidentiality scope, exclusions, duration, and remedies. The variation is enormous: no two NDAs are exactly alike. Wouldn't it be nice if AI could help? A new study presents a clever two-stage system that uses large language models to first *segment* NDA text into meaningful clauses, then a transformer classifier to *categorize* each clause. The result? A system that achieves over 90% accuracy in identifying critical provisions—potentially saving thousands of lawyer-hours annually.

## The NDA Nightmare: Why This Is Hard

Non-Disclosure Agreements seem straightforward, but they're notoriously variable. Each NDA might define "Confidential Information" differently, carve out exceptions in unique ways, specify different governing laws, or impose varying liability terms. This variability makes rule-based approaches brittle—you'd need thousands of regex patterns to cover all cases. Even trained lawyers sometimes miss subtle distinctions.

The research team identified **32 distinct clause types** across a corpus of 1,200 NDAs from technology, healthcare, and manufacturing sectors. These ranged from standard (definition, term, obligations) to nuanced (residuals clauses, injunctive relief, return of materials). The challenge: automatically identify where each clause begins and ends, then classify it correctly.

## Two-Stage Brilliance: Separate the Problems

The key insight is that **segmentation and classification are fundamentally different tasks** that benefit from different model strengths:

**Stage 1: LLM-based Segmentation** — Use a large language model (GPT-4 or Claude) with few-shot prompting to break the NDA into logical clauses. The LLM excels at understanding document structure, recognizing headings, and identifying clause boundaries even when formatting is inconsistent. The researchers crafted prompts like:  
*"Split this NDA into its constituent clauses. Each clause should represent a single legal concept."*

**Stage 2: Transformer-based Clause Classification** — Take each extracted clause and feed it into a fine-tuned transformer (BERT-based) that classifies it into one of the 32 types. This stage benefits from a specialized model trained on labeled clause examples, learning subtle linguistic patterns that distinguish, say, a "non-solicitation" clause from a "non-compete."

By splitting the problem, each stage can use the right tool: the LLM's general language understanding for segmentation, and the efficient transformer's domain-specific knowledge for classification.

## Why Not Just One Model?

You might wonder: why not use a single LLM to do everything? The researchers tested that too. A single-stage prompt like *"Identify and classify each clause"* achieved only 67% accuracy, struggling with multi-class clauses and boundary detection. The two-stage approach improved performance by **23 percentage points** while being **5x faster** (since the classifier runs locally without API calls for every query).

The separation also enables **modular improvements**: swap in a better segmentation LLM, or fine-tune the classifier on new clause types, without retraining everything. It's a clean architecture that's easier to maintain and update.

## Key Innovations That Made It Work

**Adaptive Segmentation Prompting** — The team discovered that NDAs use inconsistent headings ("Article 3," "Section 4.2," plain text). Their prompt included examples of various formatting styles and instructed the LLM to look for semantic boundaries *as well as* structural ones. This yielded 94% boundary accuracy on held-out documents.

**Hierarchical Clause Encoding** — For classification, they didn't just feed raw text to BERT. They encoded each clause with positional information (clause number, relative position in document) and used a lightweight attention mechanism to weigh earlier vs. later clauses differently—capturing the intuition that certain clause types (like governing law) tend to appear toward the end.

**Semi-Supervised Confidence Boosting** — When the classifier's confidence was low (<0.8), the system would automatically query the LLM again with a more specific prompt like *"Is this clause primarily about [candidate type]?"* This hybrid retrieval-augmented approach lifted accuracy on ambiguous clauses by 12%.

**Legal-Aware Tokenization** — They trained a custom tokenizer on legal corpora to better handle terms like "indemnify," "heretofore," and "notwithstanding" that standard tokenizers often split incorrectly.

## Results That Matter to Practitioners

On a test set of 240 NDAs (20% of corpus), the two-stage system achieved:

- **Clause boundary accuracy:** 94.2% (vs. 78% for single-stage)
- **Clause type classification F1:** clothing 91.7% macro-average (vs. 67% for single LLM prompt)
- **End-to-end document analysis time:** 12 seconds (vs. 45 seconds for single LLM approach, vs. ~30 minutes for human review)
- **Cost per NDA:** ~$0.15 in API fees (LLM stage) + negligible compute (classifier)

Most impressively, the system correctly identified **93% of "red flag" clauses**—those that deviate from standard templates and might require special negotiation. For legal teams, that's the difference between a quick review and a deep dive.

## Beyond NDAs: A Blueprint for Complex Document Analysis

The two-stage architecture isn't limited to NDAs. The pattern applies to any domain where documents have **variable structure** and **mixed granularity**:

- **Contracts** (employment, vendor, partnership agreements)
- **Patents** (claims vs. description vs. embodiments)
- **Policies** (privacy policies, terms of service)
- **Regulatory filings** (10-Ks, prospectuses)

The insight: use LLMs for *structural understanding* (where are the sections?), then specialized models for *semantic classification* (what is each section saying?). This division respects the complementary strengths of general-purpose and domain-specific AI.

## Limitations and Human-in-the-Loop

The researchers are honest about limitations: the system assumes NDAs are reasonably complete documents; fragmentary or heavily scanned NDAs (with OCR errors) still challenge the segmentation stage. Also, while 91% accuracy sounds high, that means 1 in 11 clauses gets misclassified—unacceptable for fully automated review.

The intended use is **triage and assistance**: the system highlights clauses and suggests classifications, but a human lawyer reviews and corrects. This "human-in-the-loop" approach can cut review time by 60-70% while maintaining quality. The system also learns from corrections, improving over time via active learning.

## A Glimpse of the Future

As LLMs become cheaper and faster, we might eventually do everything in one stage. But for now, the two-stage architecture is a pragmatic, high-performance solution that delivers real value today. It shows how to combine the best of large language models (flexible understanding) with efficient specialized models (domain accuracy) in a clean pipeline.

For legal tech, this is more than incremental progress. It's a step toward a future where AI doesn't just retrieve clauses but genuinely *understands* document structure—freeing lawyers to focus on judgment, negotiation, and strategy. The NDA nightmare might finally be ending.

---

*Based on: "A Two-Stage Architecture for NDA Analysis: LLM-based Segmentation and Transformer-based Clause Classification," arXiv:2603.09990v1 (2026)*
```