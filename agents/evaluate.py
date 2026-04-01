#!/usr/bin/env python3
"""
Evaluate a TinyLlama model on the benchmark suite.
Reports scores: personality, openclaw, reasoning, tool_use categories.
Optionally compares two models (baseline vs fine-tuned).
"""

import json
import sys
from pathlib import Path
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
BENCHMARK = WORKSPACE / "data/tests/benchmark.jsonl"

def load_model(model_path, adapter_path=None):
    """Load base model, optionally with LoRA adapter."""
    tokenizer = AutoTokenizer.from_pretrained(str(model_path))
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        str(model_path),
        device_map="auto",
        torch_dtype=torch.float32
    )
    if adapter_path:
        model = PeftModel.from_pretrained(model, str(adapter_path))
    return model, tokenizer

def score_response(response, expected_keywords):
    """Check if any expected keyword appears in response (case-insensitive)."""
    resp_lower = response.lower()
    for kw in expected_keywords:
        if kw.lower() in resp_lower:
            return 1
    return 0

def evaluate(model, tokenizer, benchmark_path, max_new_tokens=50):
    """Run all benchmark tests and return category scores."""
    with open(benchmark_path) as f:
        tests = [json.loads(line) for line in f if line.strip()]

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device_map="auto"
    )

    results = {
        "personality": {"correct": 0, "total": 0},
        "openclaw": {"correct": 0, "total": 0},
        "reasoning": {"correct": 0, "total": 0},
        "tool_use": {"correct": 0, "total": 0}
    }

    for test in tests:
        category = test["category"]
        prompt = test["prompt"]
        expected = test["expected_keywords"]
        output = pipe(prompt, max_new_tokens=max_new_tokens, do_sample=False)
        generated = output[0]['generated_text']
        # Extract response after prompt
        response = generated[len(prompt):].strip()
        score = score_response(response, expected)
        results[category]["correct"] += score
        results[category]["total"] += 1

    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 agents/evaluate.py <model_path> [adapter_path]")
        sys.exit(1)

    model_path = Path(sys.argv[1])
    adapter_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    print(f"Loading model from {model_path}")
    if adapter_path:
        print(f"Applying LoRA adapter from {adapter_path}")
    model, tokenizer = load_model(model_path, adapter_path)

    print(f"Running benchmark: {BENCHMARK}")
    results = evaluate(model, tokenizer, BENCHMARK)

    print("\n=== Benchmark Results ===")
    for cat, stats in results.items():
        acc = stats["correct"] / stats["total"] * 100
        print(f"{cat:12s}: {stats['correct']}/{stats['total']} = {acc:.1f}%")

    overall = sum(s["correct"] for s in results.values()) / sum(s["total"] for s in results.values()) * 100
    print(f"\nOverall accuracy: {overall:.1f}%")

if __name__ == "__main__":
    main()
