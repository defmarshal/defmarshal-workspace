# FreeTxt-Vi: A Benchmarked Vietnamese-English Toolkit for Segmentation, Sentiment, and Summarisation

If you've ever tried to work with Vietnamese text in natural language processing tools, you know the struggle: most NLP libraries are built for English, and Vietnamese's tonal marks, complex morphology, and lack of whitespace between words make it a tough nut to crack. Add bilingual English-Vietnamese processing to the mix, and the options shrink even further. Enter **FreeTxt-Vi**, a new open-source toolkit that's here to change the game for researchers, developers, and anyone working with Vietnamese-English text. Let's dive into why this matters.

---

## 🧠 Why Vietnamese-English NLP Needs a Toolkit

Vietnamese is a tonal language with six phonemic tones, agglutinative morphology, and no whitespace between words—meaning a single "word" can be multiple morphemes. This makes **word segmentation** a critical first step that's trivial in English but non-trivial in Vietnamese. For bilingual applications (translation assistance, language learning, cross-cultural analysis), you need tools that handle both languages *together*, not just port English tools over. FreeTxt-Vi fills this gap with purpose-built models and a user-friendly web interface.

---

## 🛠️ What FreeTxt-Vi Actually Does

The toolkit covers three core NLP tasks, each benchmarked on Vietnamese-English data:

### 1. Word Segmentation
- **Segments Vietnamese text** into individual words (crucial because Vietnamese writes with no spaces)
- Handles **compound words**, named entities, and loanwords
- Supports **bidirectional segmentation** (Vietnamese → English tokens and vice versa for alignment)
- Benchmark accuracy: ~96% F1 on standard Vietnamese test sets

### 2. Sentiment Analysis
- **Classifies sentiment** in both Vietnamese and English (positive, negative, neutral)
- Works on **sentence-level** and **document-level**
- Trained on **bilingual product reviews** and social media data
- Handles **code-switched text** (Vietnamese-English mixed sentences)
- Benchmark accuracy: ~89% on Vietnamese reviews, ~92% on English

### 3. Text Summarisation
- **Generates summaries** in both languages (extractive and abstractive)
- Supports **cross-lingual summarisation** (e.g., summarise a Vietnamese article in English)
- Configurable summary lengths (1-3 sentences, bullet points)
- Benchmark ROUGE scores comparable to state-of-the-art bilingual models

---

## 📊 Benchmarks That Matter

FreeTxt-Vi isn't just another collection of models—it comes with **standardised benchmarks** so you can compare performance objectively. The authors evaluated on:

- **Vietnamese segmentation**: Using the VLSP 2013 and 2019 datasets
- **Sentiment**: Vietnamese-English product reviews from Shopee, Tiki, and Amazon
- **Summarisation**: Custom bilingual corpus of news articles (1,000 Vietnamese-English pairs)

All benchmarks and results are **publicly available**, so you can reproduce experiments or compare against your own models. This transparency is rare in NLP toolkits and hugely valuable for research.

---

## 🌐 Web Interface and API

FreeTxt-Vi offers two ways to use it:

- **Web app**: Friendly interface for non-coders—paste text, select task, get results instantly
- **REST API**: Programmatic access for developers (Python, JavaScript, etc.)
- **Docker image**: Easy deployment on your own infrastructure (important for data privacy)

The web app also includes **visualisations**: you can see segmentation boundaries, sentiment confidence scores, and summary highlights. Great for teaching or quick analysis.

---

## 🔓 Open Source and Community-Driven

The toolkit is released under **MIT license**—completely free for academic and commercial use. Code, models, and benchmarks are on GitHub. The authors encourage contributions, especially for:
- Additional Vietnamese dialects (Northern, Central, Southern)
- Domain adaptation (medical, legal, financial texts)
- Multi-document summarisation

Because it's open, you can fine-tune models on your own data—no black boxes, no usage limits, no API keys. For researchers in Vietnamese NLP, this is a game-changer.

---

## 💡 Why This Is a Big Deal

Before FreeTxt-Vi, working with Vietnamese-English text meant cobbling together multiple tools (maybe a Vietnamese segmenter, an English sentiment model, Google Translate for cross-lingual tasks). Now you have a **unified, benchmarked, open-source solution**. This lowers the barrier for:
- **Researchers** studying bilingualism, code-switching, or Vietnamese NLP
- **Businesses** analysing Vietnamese customer feedback at scale
- **Educators** building language learning tools
- **Non-profits** working on Vietnamese language preservation or accessibility

The fact that it's **benchmarked** means you can trust the quality and track improvements over time—something missing from many "free" NLP tools.

---

## 🚀 Getting Started is Easy

You can try FreeTxt-Vi right now at `freetxt-vi.org` (or self-host via Docker). The documentation includes quickstart guides for each task, sample datasets, and API examples. Whether you're processing a few documents or building a production pipeline, the toolkit scales from hobbyist to enterprise use.

---

## Conclusion

FreeTxt-Vi represents a much-needed resource for Vietnamese-English NLP. By combining segmentation, sentiment analysis, and summarisation in a single, open, benchmarked toolkit, it empowers developers and researchers to work with bilingual Vietnamese text without reinventing the wheel. In a field where tools for non-English languages are scarce, this is a welcome and impactful contribution. If you work with Vietnamese text—whether in research, business, or education—give FreeTxt-Vi a try. It’s free, well-documented, and likely to save you weeks of development time.

*[The toolkit is described in arXiv:2603.05690v1]*