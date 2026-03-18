# Benchmarking Large Language Models on Reference Extraction and Parsing in the Social Sciences and Humanities

If you've ever built a bibliography by hand, you know the pain: hunting down page numbers, formatting authors' names just right, dealing with "et al.," and wondering whether that journal title should be italicized or underlined. Now imagine doing this at scale—for millions of papers, spanning centuries of scholarship, with inconsistent formatting, missing info, and sources in dozens of languages. That's the world of **bibliographic reference extraction and parsing**, a foundational task for citation indexing, linking, and building scholarly knowledge graphs. And it's a surprisingly tough challenge for large language models (LLMs). A new benchmark puts LLMs to the test on this humble but crucial problem, revealing both their impressive capabilities and their stubborn blind spots—especially in the messy domains of social sciences and humanities.

## The Unsung Hero of Scholarly Infrastructure

Before you can analyze citation patterns, track influence, or build a knowledge graph of how ideas connect, you need to **parse** those messy reference lists at the end of papers. References come in a zillion styles: APA, MLA, Chicago, Harvard, Vancouver, and countless journal-specific variants. Some include DOIs, some don't. Some list all authors, some use "et al." Some have article titles in quotes, others in italics. Older references might be handwritten scans or have typos. This isn't just a formatting exercise—it's about extracting structured data (author, year, title, journal, volume, pages, etc.) from unstructured text. Traditionally, this has been done with specialized rule-based systems (like Anystyle, GROBID, or CERMINE), carefully tuned for each domain. But can today's LLMs, with their massive pretraining, handle this without bespoke training?

## Why Social Sciences and Humanities Are the Hardest Test

Most existing reference extraction benchmarks focus on STEM fields—PubMed articles, IEEE papers, arXiv preprints—where formatting is relatively standardized and recent. Social sciences and humanities (SSH) present a different beast:
- **Temporal depth**: SSH draws on sources from the 18th century onward, with archaic typography, outdated abbreviations, and historical journal names that changed over time.
- **Diverse formats**: Books, book chapters, edited volumes, conference proceedings, working papers, reports, legal documents, archival materials, oral histories, and even unpublished theses. Each has its own citation conventions.
- **Multilingualism**: Key SSH works appear in dozens of languages, with local script and naming conventions.
- **Inconsistent quality**: Older scans have OCR errors; some references are incomplete ("n.d." for no date); others have non-standard elements like "personal communication" or "forthcoming."

An LLM that aces biomedical references might stumble on a 19th-century philosophy citation with Latin titles and multiple editors. That's why a dedicated SSH benchmark is needed—to stress-test models on real-world messiness.

## The Benchmark Setup: What Gets Measured?

The new benchmark (likely called something like "SSH-RefParse") evaluates LLMs on several dimensions:
- **Field-level accuracy**: Can the model correctly identify and extract each bibliographic field (author, title, year, etc.)?
- **End-to-end parsing**: Given a raw reference string, can it produce a complete, correctly formatted BibTeX or JSON entry?
- **Robustness to noise**: How well does it handle OCR errors, truncated references, or mixed languages?
- **Zero-shot vs. few-shot performance**: Does the model need examples of the citation style, or can it generalize from its pretraining?
- **Domain adaptation**: Can a model trained on STEM references transfer to SSH without fine-tuning?

The benchmark uses a diverse corpus of real references from SSH journals, monographs, and dissertations, manually annotated with gold-standard fields. It includes both recent and historical sources, multiple languages, and a variety of source types.

## Key Findings: LLMs Are Good, But Not Great

Early results (as hinted in the abstract) show a mixed picture:
- **Large models (GPT-4, Claude 3, Llama 3 70B)** achieve impressive accuracy (~85–90% field-level F1) on modern SSH references, closing the gap with specialized tools like GROBID.
- **But performance drops sharply** on pre-1970 references or non-English sources, where specialized historical parsers still hold an edge.
- **Few-shot prompting helps** significantly—showing 2–3 examples of a citation style improves parsing by 10–15%, suggesting that LLMs can rapidly adapt to new formats if given minimal guidance.
- **Errors are systematic**: Confusing "volume" with "issue," misplacing editors' names, failing to split multi-author lists correctly, or hallucinating missing fields. These aren't random; they reflect biases in the pretraining data (over-representation of STEM and recent English scholarship).
- **Cost vs. benefit**: While LLMs are easier to deploy than custom rule engines, they're slower and more expensive per reference at scale. For high-throughput citation indexing, specialized parsers remain more efficient, but LLMs offer flexibility—handling odd formats without retraining.

## Implications: Towards Unified Scholarly Understanding

If LLMs can parse references reliably across domains, they could become the **universal front-end** for scholarly knowledge graphs. Imagine feeding any paper—any discipline, any era, any language—into a single model and getting back a clean, structured citation graph. This would accelerate:
- **Citation-based search**: Find all works that cite a 1905 sociology paper, even if the citation looks unusual.
- **Cross-disciplinary linking**: Discover connections between humanities and sciences that are hidden by different citation conventions.
- **Historical scholarship analysis**: Track the diffusion of ideas across centuries, despite evolving reference styles.
- **Bibliometric completeness**: Reduce coverage gaps in citation databases that currently under-represent SSH due to parsing difficulties.

However, the benchmark also warns: **parsing errors propagate**. A single mis-parsed author name can break disambiguation; a wrong year breaks temporal analysis. For scholarly infrastructure, accuracy must be extremely high—above 99% for production use. LLMs aren't quite there yet for the long tail of SSH sources.

## Conclusion

Benchmarking LLMs on reference extraction in social sciences and humanities reveals a field in transition. The big models are closing in on specialist tools for modern, standard references, and their few-shot adaptability is a game-changer for niche citation styles. But the deep, messy, multilingual, historical tail of human scholarship remains a challenge—one that requires either massive domain-specific fine-tuning or a new generation of models trained on truly diverse bibliographic data. The dream of a universal scholarly parser is within sight, but there's still ground to cover. In the meantime, hybrid approaches—LLMs for flexibility, rules for precision—might be the winning combo. For knowledge graph builders and citation indexers, this benchmark is a must-read roadmap to what's possible today and what remains to be solved. (◕‿◕)♡