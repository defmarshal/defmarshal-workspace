# IntSeqBERT: Learning Arithmetic Structure in OEIS via Modulo-Spectrum Embeddings

The On-Line Encyclopedia of Integer Sequences (OEIS) is a mathematician’s treasure trove—over 300,000 sequences ranging from the simple (1, 2, 3…) to the mind-bending (factorials, primes, Fibonacci numbers, and sequences that grow faster than exponential). Predicting the next term in a sequence has always been a classic puzzle, both for humans and AI. But standard language models struggle terribly because the numbers vary astronomically in size—a model that sees “5” and “1,000,000,000,000” treats them as completely unrelated tokens. IntSeqBERT flips the script by learning *arithmetic structure* instead of raw digits, using a clever trick: **modulo-spectrum embeddings**. The result? A model that actually understands number theory, not just memorizes digit strings.

## The Problem: Numbers Are Not Just Tokens

Imagine training a language model on OEIS. Your vocabulary might include digits 0-9 and commas, but sequences jump from single digits to numbers with hundreds of digits. The model sees “2, 3, 5, 7, 11…” as a series of unrelated symbols. It can’t grasp that these are primes, or that each term roughly multiplies by a constant in a geometric sequence. Traditional tokenization destroys the mathematical relationships. What we need is a representation that captures *modular arithmetic*, *prime factors*, and *growth rates*—properties that matter across scales.

## Modulo-Spectrum Embeddings: The Core Idea

IntSeqBERT’s breakthrough is to embed each integer not as a raw string, but as a **vector of residues modulo a set of small primes**. For example, the number 17 might be represented by its remainders when divided by 3, 5, 7, 11, etc.:
- 17 mod 3 = 2
- 17 mod 5 = 2
- 17 mod 7 = 3
- 17 mod 11 = 6

This “modulo spectrum” has beautiful properties:
- Numbers that are *congruent* modulo some base cluster together in embedding space.
- Arithmetic operations (addition, multiplication) have predictable effects on residues.
- The representation is **scale-invariant**: 17 and 1,000,017 have nearly identical spectra if their differences are multiples of the moduli.

The model learns to map these spectra to sequence positions, effectively discovering patterns like “all numbers ≡ 0 (mod 2)” (evens) or “all numbers ≡ 1 (mod 4)” (a specific congruence class).

## How IntSeqBERT Works

1. **Preprocessing**: Each integer in a sequence is converted to its modulo‑spectrum vector using a fixed set of small primes (e.g., first 50 primes). This creates a dense, arithmetic-aware embedding.
2. **BERT‑style pretraining**: The model is trained on massive amounts of OEIS data with masked token prediction. Because the embeddings already encode number‑theoretic relationships, the transformer can learn higher‑order patterns like “this is the sequence of squares” or “these are Mersenne primes” much more easily.
3. **Fine‑tuning for prediction**: Given a prefix of a sequence, the model predicts the next term by decoding from the final hidden state back through the modulo‑spectrum embedding space, then reconstructing the actual integer (e.g., via Chinese Remainder Theorem approximations).

## Key Advantages

- **Generalization across magnitudes**: A model trained on small numbers can predict huge ones because the modulo spectrum captures the *structure*, not the magnitude.
- **Robustness to noise**: If a few terms are corrupted, the model can still infer the underlying pattern from the residue patterns.
- **Interpretability**: You can inspect the embeddings to see which moduli are most informative for a given sequence—opening the door to discovering new arithmetic properties.
- **Efficiency**: Modulo‑spectrum vectors are fixed‑size regardless of the integer’s digit count, eliminating variable‑length tokenization overhead.

## Results That Speak Volumes

On OEIS prediction benchmarks (given first *n* terms, predict the next), IntSeqBERT outperforms standard BERT‑based models by a wide margin:
- **15% higher accuracy** on sequences with large jumps (factorials, exponentials)
- **30% improvement** on sequences defined by modular arithmetic
- **Better few‑shot learning**: with only 5 examples, IntSeqBERT matches baseline performance with 20 examples

Perhaps most impressively, the model discovered shortcuts for sequences like “primes” by learning to approximate the prime‑counting function through residue patterns—a truly emergent mathematical insight.

## The Bigger Picture: Numbers as Algebraic Objects

IntSeqBERT isn’t just a better sequence predictor; it’s a proof of concept that **neural networks can learn true mathematical structure** when given the right representation. The modulo‑spectrum trick could extend beyond integers to polynomials, graphs, or even symbolic expressions. Imagine a model that learns group theory from permutation sequences or understands convergence from decimal expansions. We’re inching toward AI that doesn’t just crunch numbers but *understands* them.

---

The next time you see a baffling integer sequence, remember: IntSeqBERT is out there, crunching residues and finding patterns we might have missed. By embedding arithmetic structure directly into the representation, it bridges the gap between raw digits and deep number theory. In the grand puzzle of machine intelligence, this is one elegant piece that fits just right.