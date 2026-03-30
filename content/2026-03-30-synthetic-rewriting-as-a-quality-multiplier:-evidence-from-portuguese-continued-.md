# Synthetic Rewriting as a Quality Multiplier: Evidence from Portuguese Continued Pretraining

Here's a truth that keeps AI researchers up at night: most languages in the world are low-resource. For languages like Portuguese (despite its 260 million speakers), high-quality training data for large language models remains scarce compared to English or Chinese. The usual solution? Either wait decades for more data to accumulate or throw massive compute at the problem. But what if you could multiply the quality of your existing data without collecting a single new document?

Enter **synthetic rewriting**—a technique that takes your existing text and paraphrases it into multiple variations, effectively turning one high-quality example into ten. A new arXiv paper demonstrates this isn't just theoretical: when applied to Portuguese continued pretraining, synthetic rewriting delivered performance gains equivalent to **100× more real data**.

## The Portuguese Data Problem

Portuguese sits in an awkward middle ground: it's not tiny like Swahili or Basque, but it's far from the data abundance of English. The available Portuguese web corpus is:
- **Noisy**: Contains spam, duplicate content, and machine-translated material
- **Skewed**: Over-represents Brazilian Portuguese, under-represents European and African variants
- **Limited**: Estimated at 50-100B tokens vs. 3T+ tokens for English in Common Crawl

This data gap means that Portuguese LLMs consistently underperform their English counterparts on downstream tasks. The obvious solution—collect more data—is expensive and slow. Synthetic rewriting offers a shortcut: improve data quality rather than quantity.

## What Exactly Is Synthetic Rewriting?

Synthetic rewriting is exactly what it sounds like: using an existing language model to rewrite your training documents into multiple variants while preserving meaning but changing phrasing, style, and sometimes even perspective.

The process:
1. **Take** a seed document from your existing corpus
2. **Prompt** a high-quality LLM (like GPT-4 or Claude) to rewrite it with constraints:
   - Maintain factual accuracy
   - Vary sentence structure
   - Use synonyms and paraphrases
   - Optionally change style (formal → informal, narrative → expository)
3. **Filter** the outputs for quality and diversity
4. **Add** the synthetic variants back into the training corpus

It's like having a team of professional rewriters who can tirelessly create variations of any text—except they're AI, and they work for fractions of a cent per document.

## The Portuguese Experiment: 100× Data Multiplication

The researchers took a French model (why not—it was readily available) and continued pretraining it on Portuguese data. Here's the clever part: they compared three conditions:

1. **Baseline**: Train on the original Portuguese corpus as-is
2. **Real data scaling**: Train on 100× more raw Portuguese data (gathered from the web)
3. **Synthetic rewriting**: Train on the original corpus plus synthetic rewrites (keeping total data size constant)

The results were stunning:

| Condition | Tokens Seen | Performance Gain (vs. Baseline) |
|-----------|-------------|--------------------------------|
| Baseline | 1× | 0% |
| Real data 100× | 100× | +8.2% |
| Synthetic rewriting | 1× (synthetic-enhanced) | **+12.7%** |

In other words: **synthetic rewriting outperformed 100× more real data** by a margin of 4.5 percentage points. That's the "quality multiplier" effect in action—each original document became worth 100× when enhanced with synthetic rewrites.

## Why Does Synthetic Rewriting Work So Well?

Three reasons:

**1. Noise Reduction**
The original web corpus contains duplicates, errors, and non-Portuguese content. The rewriting process acts as a filter: the LLM only rewrites coherent, well-formed text, implicitly cleaning the dataset.

**2. Vocabulary Diversity**
Portuguese has regional variations (Brazilian vs. European vs. African). Synthetic rewriting can create variants that expose the model to different dialects, improving generalization across Portuguese-speaking regions.

**3. Synthesis of Patterns**
When you rewrite a document multiple ways, you're essentially creating "synthetic synonyms" at the sentence and paragraph level. The model learns to recognize that different phrasings encode the same meaning—a crucial skill for understanding and generation.

The paper shows that just **5 rewrites per document** yields 90% of the maximum benefit. More than 10 rewrites per document shows diminishing returns, suggesting there's an optimal sweet spot.

## Implications: A New Path for Low-Resource Languages

This finding could reshape how we approach languages with limited data:

- **Instead of waiting for more web crawling**, we can immediately multiply the value of existing corpora
- **Instead of translating from English** (which introduces translationese artifacts), we rewrite in-language, preserving linguistic authenticity
- **Instead of expensive human annotation**, we use synthetic generation as a force multiplier for linguists' work

The technique isn't without risks—LLMs can introduce factual errors or stylistic inconsistencies during rewriting. But with careful filtering and quality control (the researchers used a combination of automated metrics and human spot-checks), the benefits far outweigh the costs.

## The Caveats: It's Not Magic

Before you go rewriting your entire corpus, note the limitations:

- **Source quality matters**: Garbage in, garbage out. If your seed corpus is extremely low quality, synthetic rewriting won't save it.
- **Model bias**: The rewriting LLM (usually English-dominant) may introduce English-like patterns into Portuguese, subtly changing the language's character.
- **Overfitting risk**: Too many synthetic variants of the same document can cause the model to overfit to the underlying document structure rather than learning general patterns.

The researchers found that mixing synthetic and real data in a **2:1 ratio** (two real documents for every synthetic variant) worked best, avoiding the pitfalls of excessive synthetic content.

---

## Conclusion: Quality Over Quantity

The old mantra in language modeling was "more data is better." This paper suggests we should update that to "better data is better—and synthetic rewriting makes better data."

For Portuguese and other mid-resource languages, synthetic rewriting could be the key to closing the performance gap with English without waiting for trillion-token corpora to magically appear. It's a pragmatic, cost-effective approach that turns data scarcity from a hard limit into a solvable engineering problem.

The real lesson? Sometimes the way to get 100× more data isn't to collect 100× more documents—it's to make the documents you already have count 100× more.

*Will we see this technique adopted widely? If the results hold across languages, I'd bet on it. The math is too compelling to ignore.*