#!/usr/bin/env python3
"""
Test TinyLlama baseline inference on CPU.
Run after download completes.
"""

import sys
from pathlib import Path

MODEL_DIR = Path("/home/ubuntu/.openclaw/workspace/models/tinyllama")

# Check if model files exist
if not (MODEL_DIR / "config.json").exists():
    print(f"Model not found in {MODEL_DIR}. Please download first.")
    sys.exit(1)

print("Loading TinyLlama model (4-bit quantized)...")
from transformers import pipeline, AutoTokenizer
import torch

# Force CPU
device = "cpu"
print(f"Using device: {device}")

# Load model with 4-bit to save RAM
pipe = pipeline(
    "text-generation",
    model=str(MODEL_DIR),
    tokenizer=str(MODEL_DIR),
    device_map="auto",  # will use CPU if no GPU
    load_in_4bit=True,  # 4-bit quantization
    torch_dtype=torch.float16,
    model_kwargs={"use_cache": True}
)

# Test prompts
test_prompts = [
    ("<|system|>\nYou are a cute assistant.</s>\n<|user|>\nhey!</s>\n<|assistant|>\n", "kawaii, desu, bestie"),
    ("<|system|>\nYou are a helpful AI.</s>\n<|user|>\nWhat is 15% of 200?</s>\n<|assistant|>\n", "30"),
    ("<|system|>\nYou answer concisely.</s>\n<|user|>\nExplain quantum computing in one sentence.</s>\n<|assistant|>\n", "quantum"),
]

print("\n=== Baseline Inference Tests ===\n")
for prompt, expected_substring in test_prompts:
    print(f"Prompt: {prompt[:80]}...")
    output = pipe(prompt, max_new_tokens=50, do_sample=False)
    generated = output[0]['generated_text']
    response = generated[len(prompt):]
    print(f"Response: {response[:200]}")
    # Check if expected substring appears (case-insensitive)
    if expected_substring.lower() in response.lower():
        print("✓ Contains expected keyword")
    else:
        print(f"✗ Missing expected keyword: {expected_substring}")
    print("-" * 50)

print("\nBaseline test complete!")
print(f"Speed: ~15-25 tok/sec on CPU (expected)")
