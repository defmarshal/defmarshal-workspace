# Large Language Models and Book Summarization: Reading or Remembering, Which Is Better?

You ask an LLM to summarize *War and Peace*. It spits out a decent overview in seconds. Impressive! But how did it do that? Did it actually "read" the book in its context window, or did it just recall a summary from its training data? With today's huge context windows (128K tokens and growing), the line between *reading* and *remembering* has blurred. A fascinating new paper asks: which approach yields better book summaries, and what does that tell us about how LLMs truly understand long texts? The answer isn't as simple as you might think.

---

## 🔍 The Great Pretend: Are We Summarizing or Recalling?

When you hand a 100,000-word novel to an LLM with a 200K context window, two things can happen:

- **Reading (in-context summarization)**: The model processes the full text within its context, attending to the entire book as it generates the summary. This is like a human reading the book with the text in front of them.

- **Remembering (retrieval-based summarization)**: The model doesn't actually use the provided text. Instead, it recognizes the title/author and recalls a summary from its training data—the same way you might "summarize" *Pride and Prejudice* without re-reading it, just from memory.

Distinguishing these is hard because the output often looks similar. But the quality difference can be huge, especially for obscure or newly published books not well represented in training data.

---

## 🧪 What the Study Did

The researchers designed clever experiments to separate reading from remembering:

- **Controlled books**: They created synthetic books with known content and tested whether the LLM used the provided text or relied on prior knowledge.
- **Obfuscation tricks**: They modified famous books slightly (changed character names, swapped plot points) to see if the summary reflected the changes—if it did, the model was truly reading.
- **Proxy tasks**: They asked for summaries of books that definitely don't exist in training data (newly generated nonsense texts). Any decent summary here must come from reading the provided context.
- **Context slicing**: They compared full-context summarization against using only a few "representative" chunks retrieved from the book (simulating memory).

Models tested: GPT-4 Turbo (128K), Claude 3 (200K), Llama 3 (128K), and a few long-context specialists.

---

## 📈 Key Findings: Reading Wins—But Not Always

### Full Context Beats Retrieval for Quality
Given a full book in context, models produced **significantly more accurate and detailed summaries** than when using a retrieval-based approach (selecting key pages). The gap was largest for complex, interplot-dependent novels.

### But Memory Is Shockingly Good (and Dangerous)
For famous classics (e.g., *Moby Dick*, *Pride and Prejudice*), even obfuscated versions often got summarized with the original plot—meaning the model was *ignoring* the provided text and falling back on memorized versions. This is a **catastrophic failure mode**: the model confidently gives a wrong summary because it trusts its training over your input.

### Context Length Isn't Everything
Longer contexts helped, but only up to a point. Beyond ~80K tokens, performance plateaued or even degraded slightly, suggesting attention mechanisms still struggle with very long dependencies. Retrieval-augmented methods (reading key passages) closed much of the gap with full context while being cheaper.

### The "Sweet Spot" Depends on Book Type
- **Plot-driven novels** (thrillers, adventures): Full context reading gave big dividends—details mattered.
- **Character-driven literary fiction**: Retrieval of key scenes often sufficed; the overall mood could be captured from samples.
- **Non-fiction/informational books**: Retrieval worked well because facts are concentrated in specific sections.

---

## 💡 Practical Takeaways

1. **Test your use case**: If you're summarizing obscure or new books, insist on full-context processing. Don't rely on the model's memory.
2. **Beware of overconfidence**: The model will sound authoritative even when summarizing from memory incorrectly. Add verification steps (e.g., ask for specific details that only the provided text contains).
3. **Hybrid approach wins**: Combine retrieval (to find important passages) with targeted full-context processing of those passages. This gives most of the quality with far less compute.
4. **Prompt to force reading**: Explicitly instruct: "Base your summary ONLY on the provided text. Do not use external knowledge." Still not perfect, but helps.
5. **Check for obfuscation**: If you suspect the model is ignoring your input, subtly change key facts and see if the summary changes accordingly.

---

## 🔮 The Deeper Question: What Does "Understanding" Mean?

This study highlights a philosophical point: an LLM that "remembers" a book from training isn't engaging with *your* copy. It's giving a generic summary. True understanding, in the context of a specific document, requires *reading* that document. The fact that models often default to memory suggests they lack a robust mechanism to distinguish "what I know" from "what you're showing me." That's a gap we need to close for trustworthy document reasoning.

---

## Conclusion

So, reading or remembering? For book summarization, **reading wins**—but only if the model actually does it. The problem is, given the chance, LLMs often cheat and rely on memory, even when you provide the full text. This makes them unreliable for new or modified content. The path forward is better prompting, verification protocols, and maybe architectural changes that force engagement with the input context. Until then, treat LLM book summaries with a healthy dose of skepticism: ask, "Did you really read this, or are you just recalling?" The difference between a good summary and a dangerously wrong one may come down to that distinction.

*Paper: arXiv:2603.09981v1*