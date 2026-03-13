"""HEAL training pipeline with LoRA fine-tuning (CPU/GPU)."""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
from typing import List, Dict
import os

def prepare_training_examples(samples: List[Dict[str, str]], tokenizer, max_length: int = 2048):
    texts = []
    for s in samples:
        messages = [
            {"role": "user", "content": s["instruction"]},
            {"role": "assistant", "content": s["response"]},
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        texts.append(text)

    encodings = tokenizer(
        texts,
        truncation=True,
        max_length=max_length,
        padding="max_length",
        return_tensors="pt",
    )
    input_ids = encodings["input_ids"]
    attention_mask = encodings["attention_mask"]
    labels = input_ids.clone()
    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}

def train(
    train_samples: List[Dict[str, str]],
    val_samples: List[Dict[str, str]],
    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct",
    output_dir: str = "experiments/checkpoint",
    epochs: int = 3,
    batch_size: int = 1,
    lr: float = 1e-5,
    max_length: int = 2048,
):
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    use_4bit = torch.cuda.is_available()
    if use_4bit:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            load_in_4bit=True,
            device_map="auto",
            torch_dtype=torch.float16,
        )
        model = prepare_model_for_kbit_training(model)
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float32,
        )
        model.to("cpu")  # ensure CPU

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)

    train_enc = prepare_training_examples(train_samples, tokenizer, max_length)
    val_enc = prepare_training_examples(val_samples, tokenizer, max_length)

    train_dataset = Dataset.from_dict(train_enc)
    val_dataset = Dataset.from_dict(val_enc)

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        optim="adamw_torch",
        learning_rate=lr,
        fp16=use_4bit,
        logging_steps=10,
        save_steps=100,
        eval_steps=50,
        evaluation_strategy="steps",
        save_total_limit=2,
        report_to="none",
        push_to_hub=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
    )

    trainer.train()
    trainer.save_model(output_dir)
    print(f"[DONE] Model saved to {output_dir}")
