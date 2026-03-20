# MineDraft: A Framework for Batch Parallel Speculative Decoding

Large language models are amazing, but they're also slow. Generating text token-by-token can feel like watching paint dry, especially when you need to process many requests at once. **Speculative decoding** has been a clever trick to speed things up — using a small, fast "draft" model to propose tokens that a larger model then verifies. But what happens when you have a *batch* of requests? That's where existing methods hit a wall. Enter **MineDraft**, a new framework that brings true batch parallelism to speculative decoding, unlocking significant speedups for real-world workloads.

## The Problem: Sequential Bottlenecks

Traditional speculative decoding works well for a single sequence: the draft model guesses a few tokens, the target model verifies them in a single forward pass, and you either accept or reject. But when you have a batch of, say, 16 prompts, the process becomes sequential and inefficient. Each sequence might require a different number of draft tokens, and verification often happens one at a time. The result? Underutilized GPUs and missed opportunities for parallelism.

## How MineDraft Changes the Game

MineDraft rethinks speculative decoding at the batch level:

- **Draft in parallel**: The small draft model processes the entire batch simultaneously, generating draft tokens for all sequences.
- **Dynamic draft lengths**: Different sequences can have different draft token counts, and MineDraft handles this without padding waste.
- **Target verification in a single pass**: The large model verifies all drafted tokens across the batch in one shot, using clever masking and attention to avoid unnecessary computation.
- **Efficient token acceptance/rejection**: The framework quickly determines which draft tokens to keep and which to discard, then proceeds with the correct continuation.

This means the GPU works on the whole batch together, maximizing throughput.

## Key Innovations

- **Batch-aware tree attention**: MineDraft adapts the transformer attention mechanism to handle variable-length draft sequences within a batch efficiently.
- **Heuristic draft length selection**: It learns to predict optimal draft lengths per sequence based on context, balancing speed and acceptance rates.
- **Kernel-level optimizations**: Custom CUDA kernels minimize memory movement and synchronization overhead, squeezing out every bit of performance.
- **Compatibility**: Works with existing transformer architectures and can be dropped into inference pipelines with minimal changes.

## Real-World Speedups

In benchmarks, MineDraft delivers up to **2×-3× faster decoding** for medium to large batch sizes compared to naive sequential speculative decoding. The speedup grows with batch size because parallelism overhead gets amortized. For applications like chat servers, translation APIs, or batch document processing, that translates directly to lower latency and higher throughput without sacrificing output quality.

## The Future of Efficient LLM Inference

MineDraft shows that speculative decoding isn't just a single-sequence optimization — it can scale to batched workloads that matter in production. As models grow larger and demand for real-time AI explodes, frameworks like this will become essential infrastructure. The takeaway? Sometimes the biggest speedups come not from bigger models, but from smarter ways to use them.

*MineDraft proves that when it comes to LLM inference, parallelism isn't just for training — it's for decoding too.*