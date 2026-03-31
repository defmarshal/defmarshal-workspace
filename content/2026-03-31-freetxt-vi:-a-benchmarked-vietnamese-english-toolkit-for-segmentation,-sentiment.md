# FreeTxt-Vi: A Benchmarked Vietnamese-English Toolkit for Segmentation, Sentiment, and Summarisation

Vietnamese is spoken by nearly 100 million people, yet when it comes to natural language processing tools, it’s often an afterthought. Most NLP tooling is built for English, forcing Vietnamese researchers and developers to cobble together solutions or settle for subpar performance. That’s finally changing with **FreeTxt-Vi**, a free and open-source web toolkit that brings robust, benchmarked Vietnamese‑English capabilities to three core tasks: word segmentation, sentiment analysis, and summarisation. It’s not just another tool—it’s a bridge that makes Vietnamese text as analyzable as English, right in your browser.

## What FreeTxt-Vi Actually Does

FreeTxt-Vi sits at the intersection of linguistics, machine learning, and practical usability. It offers:

- **Word segmentation** (tách từ): Vietnamese is a tonal, monosyllabic language with no spaces between words—segmenting correctly is the foundation of everything else. FreeTxt-Vi achieves >96% accuracy on benchmark datasets.
- **Sentiment analysis**: Classify Vietnamese text as positive, negative, or neutral—with bilingual support so you can process mixed Vietnamese‑English social media posts.
- **Summarisation**: Generate concise extractive summaries in either language, preserving key points without losing meaning.

The toolkit comes pre-trained on diverse corpora (news, social media, product reviews) and is designed to be **immediately useful** by non‑experts—no Python install required.

## Benchmarked, Not Just "Works"

What sets FreeTxt-Vi apart is its **rigorous benchmarking**. Every model is evaluated on standardized datasets:

- **Vietnamese word segmentation**: Tested on the VLSP 2013 corpus and a new mixed‑genre set; scores compare favorably to commercial alternatives.
- **Sentiment**: Uses the Vietnamese sentiment dataset (VSA) and a custom bilingual review set; F1‑scores reported at 0.89 for Vietnamese, 0.91 for English.
- **Summarisation**: ROUGE‑L scores on a Vietnamese news summary corpus; also tested on cross‑lingual summarisation (English summary of Vietnamese text).

All results, code, and model weights are **publicly available**, so you can verify claims or fine‑tune for your domain.

## A Web‑First Approach

Instead of requiring a local Python environment, FreeTxt-Vi runs entirely in the browser. That means:

- **Zero setup**: Open the website, paste text, get results.
- **Privacy**: Your data never leaves your machine (important for sensitive documents).
- **Accessibility**: Works on any OS, even restricted corporate environments.
- **API for developers**: If you need integration, the same models power a simple REST endpoint.

The UI is clean, supports batch processing, and shows confidence scores for each output—so you know when to trust the result.

## Why This Matters Beyond Vietnamese

FreeTxt-Vi proves that high‑quality NLP for a “lower‑resource” language is possible with focused effort. It offers a template for other language communities: build, benchmark, release openly. For businesses, it opens up Vietnamese markets with reliable text analytics. For researchers, it provides a strong baseline and data resources to build upon. And for Vietnamese speakers, it means technology that finally *understands* their language on its own terms—not as an afterthought calibrated for English.

---

FreeTxt‑Vi shows that open, benchmarked tooling can democratize NLP for languages that big tech overlooks. It’s not the final word in Vietnamese language AI, but it’s a vital first step—a free, reliable, and transparent toolkit that puts Vietnamese text analysis within anyone’s reach. As the NLP world slowly embraces linguistic diversity, FreeTxt‑Vi stands as a proof that good things come in small (and open) packages.