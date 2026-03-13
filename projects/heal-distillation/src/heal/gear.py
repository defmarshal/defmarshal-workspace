"""GEAR: Guided Entropy-Assisted Repair with CPU-friendly model loading."""

import torch
from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer
from .teacher import generate_with_hint

SCORER_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"


class GEAR:
    def __init__(self, scorer_model: str = SCORER_MODEL_ID, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"[GEAR] Using device: {self.device}")

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

    def compute_step_entropies(self, text: str) -> List[float]:
        enc = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=2048).to(self.device)
        with torch.no_grad():
            outputs = self.model(**enc, output_attentions=False, output_hidden_states=False)
            logits = outputs.logits[0, :-1, :]
            labels = enc.input_ids[0, 1:]
            probs = torch.softmax(logits, dim=-1)
            token_probs = probs[torch.arange(len(labels)), labels]
            entropies = (-torch.log2(token_probs + 1e-10)).cpu().numpy().tolist()
        return entropies

    def find_breakpoint(self, entropies: List[float]) -> int:
        if not entropies:
            return -1
        n = len(entropies)
        third = max(1, n // 3)
        window = entropies[:third]
        idx = int(torch.argmax(torch.tensor(window)).item())
        return idx

    def repair_trajectory(self, problem: str, broken_traj: str, breakpoint_token_idx: int, n_hints: int = 5) -> List[str]:
        # For simplicity: regenerate full continuation using answer hint.
        # We need the correct answer; we can't extract from broken_traj easily. We'll rely on external answer.
        # In practice, we'll pass answer separately; but here we use generic hint.
        # We'll just ask Step to continue correctly, not using answer explicitly.
        prompt = f"""Problem: {problem}

Here is an attempted solution that may have errors:

{broken_traj}

Please provide a correct, complete solution, ensuring logical steps and end with \\boxed{{answer}}."""
        return generate_with_hint(prompt, "Fix the solution", n=n_hints)

    def run_gear(self, problem: str, trajectories: List[str]) -> List[str]:
        repaired_all = []
        for traj in trajectories:
            entropies = self.compute_step_entropies(traj)
            bp = self.find_breakpoint(entropies)
            if bp >= 0:
                repaired = self.repair_trajectory(problem, traj, bp)
                repaired_all.extend(repaired)
        return repaired_all
