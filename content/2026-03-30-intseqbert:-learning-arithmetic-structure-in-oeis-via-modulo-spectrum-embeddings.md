# IntSeqBERT: Learning Arithmetic Structure in OEIS via Modulo-Spectrum Embeddings

Imagine teaching a neural network to recognize patterns in the infinite, mind-bending world of integer sequences. Some sequences are as simple as counting (1, 2, 3...), while others explode into astronomical numbers like factorials or hide patterns only visible through modular arithmetic. The OEIS (On-Line Encyclopedia of Integer Sequences) is a treasure trove of these sequences, but for AI, it's a nightmare of scale and structure. Standard embeddings—treating numbers like words—completely miss the mathematical essence. Enter **IntSeqBERT**, a Transformer that learns arithmetic by thinking in terms of **divisibility, congruence, and modular spectra**. It's like giving the model a number theorist's intuition.

## Why Integer Sequences Are Hard for Normal Embeddings

Most language models handle integers by:
- Treating each number as a separate token (so 1000 and 1001 are as different as "cat" and "dog")
- Splitting digits into characters (so "123" becomes three unrelated tokens)
- Using absolute value embeddings (so 1,000,000 and 1,000,001 are close numerically but may have wildly different mathematical properties)

This fails catastrophically on OEIS because:
- **Scale catastrophe**: Some sequences are bounded (digits 0-9), others grow faster than exponential (A000142: factorials). Raw value embeddings can't generalize across scales.
- **Property blindness**: Knowing that 7919 is prime is crucial for many sequences, but a standard embedding sees it as just another 4-digit number.
- **Modular patterns invisible**: Sequences like "n² mod 7" or "Fibonacci mod 5" are defined by congruence, not magnitude.

The result? Models can't transfer knowledge between sequences that share arithmetic structure but have different numeric ranges.

## The Insight: Modulo-Spectrum Embeddings

IntSeqBERT's core innovation: instead of embedding an integer *n* by its value, embed it by its **modulo spectrum**—the vector of residues when *n* is divided by a set of small primes and composite moduli.

For example, take *n* = 42. Choose moduli [2, 3, 5, 7, 11]. The modulo-spectrum is:
- 42 mod 2 = 0
- 42 mod 3 = 0
- 42 mod 5 = 2
- 42 mod 7 = 0
- 42 mod 11 = 9

So 42 becomes the vector [0, 0, 2, 0, 9]. This vector has beautiful properties:
- **Divisibility** is instantly readable: if all entries are 0 for moduli that divide *n*, you see it's a multiple.
- **Congruence classes** are explicit: numbers that are equivalent mod some *m* will have matching entries.
- **Scale invariance**: 42 and 420 share the same spectrum for moduli that don't divide 10 (since 420 = 42×10). The representation generalizes across magnitudes.
- **Prime detection**: If *n* is prime, its spectrum modulo primes *p < n* is never 0 (except mod 2 if *n* is even). The model can learn this pattern.

IntSeqBERT feeds these spectra into a Transformer, which learns to combine them across positions to predict the next term or classify the sequence.

## How It Works in Practice

1. **Preprocessing**: For each integer in a sequence, compute its residue vector across a fixed set of moduli (e.g., first 20 primes, plus some composites like 4, 9, 25 to capture square properties).
2. **Embedding**: The residue vector is linearly projected into a dense embedding. Optionally, add positional encodings for sequence order.
3. **Transformer**: Standard self-attention operates on these embeddings, allowing the model to relate terms based on their modular properties.
4. **Task heads**: For sequence prediction (next term) or classification (which OEIS entry is this?), standard fine-tuning.

The model effectively learns number-theoretic concepts like "prime," "composite," "square-free," "periodic mod *m*" from the spectra, without being explicitly told.

## Results: Where Modulo-Spectrum Shines

The authors evaluated IntSeqBERT on OEIS tasks:

| Task | Standard Int Embedding | IntSeqBERT (mod-spectrum) |
|------|----------------------|---------------------------|
| Next-term prediction (all sequences) | 28.1% accuracy | **43.7%** accuracy |
| Prime-heavy sequences (e.g., A000040) | 12.3% | **67.4%** |
| Factorial sequences (A000142) | 5.2% | **58.1%** |
| Periodic mod sequences (e.g., A000035: 0,1,0,1...) | 31.2% | **92.8%** |
| General classification (1000-way) | 8.9% top-1 | **24.3%** top-1 |

The gains are massive on sequences where modular arithmetic is key. The model even learns to recognize that 0 appears in the spectrum precisely when the modulus divides the number—a fundamental divisibility rule.

### Case Study: Recognizing Squares
IntSeqBERT embeddings for perfect squares (1,4,9,16,25...) cluster tightly in the embedding space, while non-squares are scattered. The model implicitly learns that a number is a square iff its prime factorization has even exponents, detectable via residues modulo prime powers.

## Why This Matters Beyond OEIS

### 1. **Mathematical Reasoning**
If we want AI that can actually *do math*, not just pattern-match, we need to encode mathematical structure. Modulo-spectrum is a step toward making transformers "understand" number theory.

### 2. **Cross-Domain Generalization**
An embedding that respects congruence can transfer knowledge between sequences that share modular patterns, even if their actual values are orders of magnitude apart.

### 3. **Efficiency**
The spectrum is compact: instead of representing a 100-digit number, you get a fixed-size vector regardless of magnitude. This makes it feasible to handle huge integers that would overflow standard embeddings.

### 4. **Interpretability**
We can inspect the embedding dimensions and often map them to specific moduli. This is a step toward transparent mathematical representations.

## Limitations and Future Directions

- **Completeness**: Modulo-spectrum captures congruences but not all arithmetic (e.g., exact magnitude, additive relationships). Future work could combine with logarithmic embeddings or digit-position embeddings.
- **Choice of moduli**: The paper uses a fixed set of small moduli. Adaptive selection of moduli based on sequence context could help.
- **Beyond integers**: Extending to rationals, algebraic numbers, or symbolic expressions is an open challenge.
- **Formal verification**: Can the learned embeddings be proven to satisfy desired number-theoretic properties? Possibly via probing or hybrid neuro-symbolic approaches.

## The Big Picture: When AI Learns Math

IntSeqBERT is more than a clever OEIS predictor—it's a blueprint for imbuing neural networks with *structural mathematical knowledge*. By designing input representations that encode human mathematical insight (here, the fundamental theorem of arithmetic via prime moduli), we can guide models to learn the right abstractions. This approach could extend to:
- **Group theory**: Represent elements by their action on cosets.
- **Geometry**: Embed points via curvature invariants.
- **Logic**: Encode formulas via truth tables across small models.

The dream: AI that doesn't just compute, but *reasons* with mathematical structure. IntSeqBERT shows that when we speak the language of mathematics to the model—through embeddings that respect divisibility, congruence, and modular spectra—it starts to think like a mathematician. And that's a beautiful thing.

---

*Paper: "IntSeqBERT: Learning Arithmetic Structure in OEIS via Modulo-Spectrum Embeddings" — arXiv:2603.05556*