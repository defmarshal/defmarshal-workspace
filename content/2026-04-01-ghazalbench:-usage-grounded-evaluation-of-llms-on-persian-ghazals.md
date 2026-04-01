# GhazalBench: Usage-Grounded Evaluation of LLMs on Persian Ghazals

Persian poetry isn't just literature—it's woven into daily life. In Iran, quoting Hafez at a family gathering, slipping a Rumi line into a text message, or invoking Ferdowsi in political discourse is as natural as breathing. But for large language models, this rich cultural tapestry is often an impenetrable fog. How can an AI trained on global web data possibly grasp the nuanced ways Persian ghazals are actually *used*? Enter **GhazalBench**, a groundbreaking benchmark that evaluates LLMs not on abstract poetic analysis, but on real-world usage of Persian poetry. It's a wake-up call for the AI community: understanding culture means understanding context.

---

## 🌹 What Makes Persian Ghazals So Special?

The ghazal is more than a poetic form—it's a living cultural artifact. Key characteristics:

- **Intertextuality**: Poets constantly reference and riff on earlier ghazals, creating a dense web of allusions.
- **Occasional usage**: Verses are deployed for specific social functions: advice, apology, celebration, sarcasm.
- **Layered meaning**: A single couplet can carry literal, mystical, and humorous interpretations depending on context.
- **Canonical authority**: Lines from Hafez, Saadi, or Rumi carry weight similar to proverbs or even legal citations in some settings.

For an LLM, this is a triple challenge: recognizing the verse, understanding its traditional meaning, and—hardest of all—knowing *when* and *how* it would be invoked in real conversation.

---

## 🔬 What Is "Usage-Grounded" Evaluation?

Traditional poetry benchmarks ask: *"What does this poem mean?"* or *"Translate this verse."* GhazalBench asks: *"When would someone quote this?"* and *"Is this an appropriate response in this situation?"*

The "usage-grounded" approach means:

- **Context is king**: Each item presents a real-world scenario (e.g., a friend shares sad news; you want to comfort them with a ghazal line). The model must choose or generate the most culturally fitting verse.
- **Multi-choice with cultural reasoning**: Not just recall, but *judgment*. Why is verse A better than verse B for this moment?
- **Paraphrase and adaptation**: Can the model rephrase a ghazal line to fit modern speech while preserving the intended nuance?
- **Detection of misuse**: Identify when a verse is being used inappropriately (e.g., quoting a wedding poem at a funeral).

This mirrors how Persian speakers *actually* interact with poetry—embedding it naturally in communication.

---

## 📊 The GhazalBench Dataset: Raw Cultural Data

The benchmark is built from thousands of real usage instances collected from:

- **Social media** (Telegram, Instagram) where users quote poetry in comments
- **Literature forums** discussing appropriate usage
- **Advice columns** where poets respond to letters with tailored verses
- **Film and TV** scripts that incorporate ghazals organically

Each sample includes:
- A **situation description** (social context, emotional tone, relationship dynamics)
- A **pool of candidate verses** (4–6 options)
- **Correct answer** (the verse most likely to be used by a native speaker)
- **Explanation** (why it's appropriate, sometimes with subtle scoring for near-misses)

The dataset covers 50 canonical poets and spans love, mysticism, ethics, humor, and politics.

---

## 🧪 Key Findings: How Do LLMs Stack Up?

The researchers tested leading multilingual LLMs (GPT-4, Claude, Llama, plus Persian-specific models like PersianGPT). Results were… revealing:

- **Overall accuracy**: Best models hit ~68%—well above chance (25%) but far from human native speakers (~92%).
- **Cultural depth matters**: Models performed better on love and mysticism themes (common in training data) but poorly on political or satirical usage (rarely seen).
- **Size helps, but not enough**: Larger models improved, but even 70B参数 models struggled with subtle context cues.
- **Persian-specific fine-tuning gave a boost**: PersianGPT, trained on Persian poetry and social data, scored highest—but still had blind spots.
- **Failure modes**: Models often chose verses that were *poetically beautiful* but *socially inappropriate* for the given scenario. They missed pragmatic nuances like power dynamics (speaking to a boss vs. a friend) and generational codes (what resonates with youth vs. elders).

---

## 💡 Why This Benchmark Matters Beyond Persian Poetry

GhazalBench isn't just about Persian. It's a template for **usage-grounded evaluation of any culturally embedded artifact**:

- **Chinese shijing/qu citations** in formal speeches
- **Japanese waka/haiku** in seasonal greetings
- **Arabic proverbs** in diplomatic language
- **Biblical/ Quranic verses** in everyday argumentation

The core idea: language models must learn not just *what* a text says, but *how* it functions in social life. This bridges NLP with sociolinguistics and anthropology.

For multilingual AI, it’s a reality check: having a tokenizer that supports Persian script is not enough. The model needs *cultural competence*, which requires data that captures actual usage patterns—not just canonical texts.

---

## 🚀 Implications for AI Development

### Rethink training data
Include real conversational data where poetry is quoted. Not just poems, but *paraphrases* and *re-contextualizations*.

### Build culturally aware evaluation suites
GhazalBench shows that accuracy on multiple-choice poetry questions is a thin metric. We need benchmarks that test pragmatics, appropriateness, and situational awareness.

### Collaborate with domain experts
Persian literary scholars, sociologists, and native speakers are essential to curate usage-grounded items. This is not a job for crowdworkers alone.

### Move beyond translation
Many LLMs "understand" Persian poetry only through English translations. GhazalBench forces engagement with the original language and its cultural codes.

### Design for reflection
AI systems that suggest poetry (e.g., in messaging apps) should be evaluated on whether their suggestions would be socially welcomed, not just semantically relevant.

---

## Conclusion

GhazalBench exposes a blind spot in current LLM evaluation: we’ve been testing *comprehension* but neglecting *communicative competence*. Persian ghazals, with their deep cultural embeddedness, make this gap starkly visible. The benchmark proves that usage-grounded evaluation is both necessary and feasible. As AI becomes more multilingual and culturally embedded, we need more benchmarks like this—ones that ask not "what does it mean?" but "when would you say this?" The road to truly culturally intelligent AI passes through the living, breathing, quoting world of Persian poetry. Let's build models that don't just recite Hafez, but know *why* and *when* to share his words.

*Paper: arXiv:2603.09979v1*