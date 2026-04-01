#!/usr/bin/env python3
"""
Simple LoRA fine-tuning for TinyLlama using PEFT.
CPU-optimized, no fancy dependencies besides transformers+peft+bitsandbytes.
"""

import json
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
MODEL_DIR = WORKSPACE / "models/tinyllama"
DATA_FILE = WORKSPACE / "data/personality.jsonl"
OUTPUT_DIR = WORKSPACE / "models/mewmew-lora/personality-v1-simple"

# Load model and tokenizer
print("Loading model (4-bit)...")
model = AutoModelForCausalLM.from_pretrained(
    str(MODEL_DIR),
    load_in_4bit=True,
    device_map="auto",  # will use CPU if no GPU
    torch_dtype=torch.float16
)
tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))

# Ensure tokenizer has padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Apply LoRA
lora_config = LoraConfig(
    r=8,  # CPU-friendly
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # should show ~30-40M trainable params

# Load dataset
def load_dataset(path):
    with open(path) as f:
        data = [json.loads(line) for line in f if line.strip()]
    # Flatten messages into a single string with special tokens
    texts = []
    for item in data:
        messages = item["messages"]
        # Convert ChatML to single string: <|system|>...<|user|>...<|assistant|>...
        text = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                text += f"<|system|>\n{content}</s>\n"
            elif role == "user":
                text += f"<|user|>\n{content}</s>\n"
            elif role == "assistant":
                text += f"<|assistant|>\n{content}</s>\n"
        texts.append(text)
    return Dataset.from_dict({"text": texts})

print("Loading dataset...")
dataset = load_dataset(DATA_FILE)
print(f"Dataset size: {len(dataset)} examples")

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, max_length=1024, padding="max_length")

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

# Training arguments (CPU-optimized)
training_args = TrainingArguments(
    output_dir=str(OUTPUT_DIR),
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    optim="adamw_torch",
    learning_rate=2e-4,
    warmup_steps=50,
    logging_steps=10,
    save_steps=100,
    eval_strategy="no",  # skip eval for speed
    save_total_limit=2,
    report_to="none",
    disable_tqdm=False,
    # CPU-specific
    no_cuda=True,  # force CPU
    dataloader_num_workers=0,  # avoid multiprocessing issues
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

print("Starting training...")
trainer.train()

# Save final model (LoRA adapter only)
print("Saving LoRA adapter...")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"Training complete! Adapter saved to {OUTPUT_DIR}")
