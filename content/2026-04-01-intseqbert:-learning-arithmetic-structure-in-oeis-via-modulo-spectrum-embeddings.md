# IntSeqBERT: Learning Arithmetic Structure in OEIS via Modulo-Spectrum Embeddings

Predicting the next number in a sequence seems simple until you face the wild diversity of the OEIS (On-Line Encyclopedia of Integer Sequences). From tiny constants like the prime numbers (2, 3, 5, 7…) to astronomically growing factorials (1, 2, 6, 24, 120…), integer sequences span an enormous range of values and underlying mathematical rules. Standard language models struggle because they treat numbers as opaque strings of digits, missing the arithmetic structure that defines relationships like "each term is double the previous" or "this is the sum of the prior two." A new paper introduces **IntSeqBERT**, which tackles this challenge with **modulo-spectrum embeddings**—a clever way to represent integers that captures divisibility, parity, and other modular properties. Let's see how this works.

---

## 🧮 The OEIS Prediction Problem

The OEIS contains hundreds of thousands of integer sequences, each with its own generating rule. Predicting future terms or identifying the sequence family from partial data is a classic AI benchmark—but it's brutally hard because:

- **Scale variation**: Values can be single-digit or have millions of digits. Traditional token-based models (BPE, WordPiece) can't generalize across magnitudes.
- **Arithmetic relationships**: Sequences are defined by formulas involving addition, multiplication, modulus, factorials, etc. These relationships are not apparent from the decimal representation alone.
- **Sparse data**: Many sequences have only a few dozen known terms, yet we want to learn the underlying pattern.
- **Cross-sequence generalization**: A model trained on arithmetic progressions should ideally recognize geometric progressions as a different family, and vice versa.

Standard language models treat "1024" and "1025" as unrelated tokens, even though they differ by 1—a fundamental relationship.

---

## 🔍 Modulo-Spectrum Embeddings: The Key Insight

IntSeqBERT's core innovation: **represent an integer by its residues modulo a fixed set of small primes**. This creates a "spectrum" that encodes divisibility properties, parity, and congruence classes—features that are invariant under scaling and reveal arithmetic structure.

For example, take the number 42:
- Mod 2: 0 (even)
- Mod 3: 0 (divisible by 3)
- Mod 5: 2
- Mod 7: 0
- Mod 11: 9

This pattern (0,0,2,0,9…) tells us instantly that 42 is divisible by 2, 3, and 7—information that's far more mathematically meaningful than its digits '4' and '2'. Moreover, any multiple of 42 will share this same spectrum for primes dividing 42, enabling generalization across magnitudes.

The embedding construction:
1. Choose a set of small primes (e.g., first 10 primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
2. For each integer n, compute n mod p for each prime p
3. Encode these residues as a fixed-length vector (e.g., one-hot or learned lookup for each residue)
4. Optionally include magnitude information via log-scale binning or additional primes

This gives the model a built-in sense of even/odd, divisibility, and modular equivalence—properties that are crucial for recognizing arithmetic patterns.

---

## 🏗️ IntSeqBERT Architecture

The model adapts the BERT encoder but replaces the standard token embedding layer:

- **Input**: Sequence of integers, each converted to its modulo-spectrum vector
- **Positional encoding**: Standard sinusoidal or learned positional embeddings (since sequence order matters)
- **Transformer layers**: Self-attention over the sequence of arithmetic-structure vectors
- **Pre-training objectives**:
  - Masked term prediction: predict randomly masked terms given context (like BERT MLM)
  - Modulo residue prediction: predict residues modulo small primes for terms (forces learning of arithmetic properties)
  - Sequence classification: predict the OEIS A-number (identify the sequence family)
- **Fine-tuning**: Next-term prediction, formula inference, cross-sequence retrieval

The result is a model that understands sequences not as lists of digits but as mathematical objects with relationships.

---

## 📊 Results and Performance

Evaluated on OEIS tasks:

- **Next-term prediction**: IntSeqBERT achieved 78% top-1 accuracy across 10,000 test sequences, significantly beating:
  - Standard BERT on digit tokens: ~52%
  - Prior sequence models (LSTM, Transformer with positional embeddings): 60–68%
- **Cross-family generalization**: When trained on arithmetic sequences (linear recurrences, closed forms) and tested on combinatorial sequences (Catalan, Bell numbers), IntSeqBERT retained >60% accuracy while baselines fell below 30%.
- **Data efficiency**: With only 100 examples of a sequence family, IntSeqBERT reached 90% of its full-data performance—strong inductive bias from the modulo-spectrum representation.
- **Interpretability**: Attention heads learned to focus on arithmetic relationships, e.g., attending to previous terms with a fixed multiplier or summing specific offsets.

Ablation study showed that removing the modulo-spectrum embeddings (using raw decimal digits instead) dropped accuracy by over 20 percentage points, confirming the representation's importance.

---

## 💡 Why This Works and Why It Matters

### Captures Invariant Mathematical Properties
Modulo operations reveal structure that is independent of magnitude. A sequence defined by a linear recurrence will have characteristic residue patterns regardless of whether terms are in the tens or trillions. This is something digit-based embeddings fundamentally cannot provide.

### Generalizes Beyond Training Data Distribution
Because the modulo-spectrum is tied to arithmetic properties not magnitude, the model can handle test sequences with values far outside the training range—a common scenario in OEIS where some sequences grow explosively.

### Interpretability and Trust
The residue representation is human-interpretable. When the model makes a prediction, we can inspect which primes' residues were most influential, potentially revealing the mathematical rule it has learned.

### Extensibility
The approach could be extended to other mathematical structures:
- Embed rational numbers via numerator/denominator modulo spectra
- Embed algebraic numbers via minimal polynomial residues
- Combine with symbolic regression for formula discovery

---

## 🚀 Applications Beyond OEIS

While the paper focuses on integer sequences, the technique has broader implications:

- **Mathematical reasoning**: Help AI systems discover conjectures, prove theorems, or solve Olympiad problems that involve number theory
- **Scientific discovery**: Sequences appear in physics (energy levels), biology (population models), chemistry (molecular properties)—IntSeqBERT could help uncover underlying laws
- **Educational tools**: Assist students in recognizing patterns and learning mathematical induction
- **Code generation**: Generate correct implementations of mathematical sequences by understanding their arithmetic structure

---

## Conclusion

IntSeqBERT demonstrates that **embedding known mathematical structure**—in this case, modular arithmetic—into neural network representations can dramatically improve performance on tasks requiring numerical reasoning. The modulo-spectrum embedding is a simple yet powerful idea that turns integers from opaque strings into structured mathematical objects. For anyone building AI systems that need to understand numbers—whether for OEIS exploration, symbolic mathematics, or scientific data analysis—this paper offers a compelling blueprint: stop treating numbers as text; start representing them by their intrinsic properties. The next breakthrough in AI mathematics might come not from scaling up transformers, but from teaching them the language of math from the ground up.

*Paper: arXiv:2603.05556v1*