"""PURE: Perplexity-Uncertainty Ratio Estimator (CPU-friendly)."""

import torch
from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer

SCORER_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"


class PURE:
    def __init__(self, scorer_model: str = SCORER_MODEL_ID, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"[PURE] Using device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(scorer_model, trust_remote_code=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        if self.device == "cuda":
            self.model = AutoModelForCausalLM.from_pretrained(
                scorer_model,
                trust_remote_code=True,
                load_in_4bit=True,
                device_map="auto",
                torch_dtype=torch.float16,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                scorer_model,
                trust_remote_code=True,
                torch_dtype=torch.float32,
            )
            self.model.to(self.device)
        self.model.eval()

    def compute_perplexity(self, text: str) -> float:
        enc = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=2048).to(self.device)
        with torch.no_grad():
            outputs = self.model(**enc, labels=enc.input_ids)
            loss = outputs.loss
            pp = torch.exp(loss).item()
        return pp

    def filter_trajectories(self, trajectories: List[str], lambda_thresh: float = 0.2, epsilon: float = 0.01) -> List[str]:
        if not trajectories:
            return []
        pps = [self.compute_perplexity(t) for t in trajectories]
        baseline_pp = float(torch.tensor(pps).median())
        kept = []
        for traj, pp in zip(trajectories, pps):
            ratio = pp / (baseline_pp + epsilon)
            if ratio <= lambda_thresh + epsilon:
                kept.append(traj)
        return kept
