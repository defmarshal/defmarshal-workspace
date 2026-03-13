"""Dataset utilities for AIME problems and training data."""

from datasets import load_dataset
from transformers import AutoTokenizer
import torch
from typing import List, Dict, Any
import json

AIME_DATASET = "gneubig/aime-1983-2024"
QWEEN_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"


def load_aime(split: str = "train", num_samples: int = 100, seed: int = 42) -> List[Dict[str, Any]]:
    """Load AIME dataset. Returns list of dicts with 'problem' and 'answer' (if available)."""
    ds = load_dataset(AIME_DATASET, split=split)
    ds = ds.shuffle(seed=seed).select(range(min(num_samples, len(ds))))
    # Convert to list of dicts
    problems = []
    for item in ds:
        # Dataset fields likely: 'problem' and 'answer'
        problem_text = item.get("problem") or item.get("Question")
        answer = item.get("answer") or item.get("Answer")
        problems.append({"problem": problem_text, "answer": answer})
    return problems


def get_tokenizer():
    """Get Qwen2.5 tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained(QWEEN_MODEL_ID, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def format_chat(instruction: str, response: str) -> Dict[str, str]:
    """Format a single prompt-response pair for chat model."""
    return {"messages": [{"role": "user", "content": instruction}, {"role": "assistant", "content": response}]}


def save_jsonl(records: List[Dict], path: str):
    """Save list of dicts to JSONL."""
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def load_jsonl(path: str) -> List[Dict]:
    """Load JSONL."""
    records = []
    with open(path) as f:
        for line in f:
            records.append(json.loads(line))
    return records
