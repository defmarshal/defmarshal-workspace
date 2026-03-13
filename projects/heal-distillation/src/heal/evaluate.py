"""Evaluation for HEAL-distilled student models (CPU/GPU)."""

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch
from typing import List, Dict
import re

def extract_boxed(text: str) -> str:
    if "\\boxed{" in text:
        try:
            return text.split("\\boxed{")[1].split("}")[0].strip()
        except:
            return text.strip()
    return text.strip()

def normalize_answer(ans: str) -> str:
    ans = ans.lower().replace(",", "").replace(" ", "")
    return ans

def evaluate_model(
    checkpoint_path: str,
    test_problems: List[Dict[str, str]],
    base_model: str = "Qwen/Qwen2.5-1.5B-Instruct",
    max_new_tokens: int = 512,
) -> Dict[str, float]:
    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    use_cuda = torch.cuda.is_available()
    if use_cuda:
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            trust_remote_code=True,
            load_in_4bit=True,
            device_map="auto",
            torch_dtype=torch.float16,
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            trust_remote_code=True,
            torch_dtype=torch.float32,
        )
        model.to("cpu")

    # Load LoRA weights if checkpoint exists and is not full model
    model = PeftModel.from_pretrained(model, checkpoint_path)

    correct = 0
    total = len(test_problems)

    for item in test_problems:
        problem = item["problem"]
        gt = item.get("answer", "").strip()
        if not gt:
            continue

        messages = [
            {"role": "user", "content": f"Solve the following problem step by step. End your final answer within \\boxed{{}}.\n\nProblem: {problem}"}
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt")
        if use_cuda:
            inputs = inputs.to("cuda")
        else:
            inputs = inputs.to("cpu")

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        pred = extract_boxed(response)
        if normalize_answer(pred) == normalize_answer(gt):
            correct += 1

    accuracy = correct / total if total > 0 else 0.0
    return {"pass@1": accuracy, "correct": correct, "total": total}
