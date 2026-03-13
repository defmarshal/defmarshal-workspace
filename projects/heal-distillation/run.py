#!/usr/bin/env python3
"""Orchestrator for HEAL pipeline with resume capability.

Usage: Run from project root. This script should be executed with the venv Python if available.
"""
import sys
import os
# If a virtual environment exists in ./venv, use its Python
if os.path.exists("venv/bin/python"):
    venv_python = os.path.abspath("venv/bin/python")
    print(f"[INFO] Using venv Python: {venv_python}")
    # Re-exec this script with the venv interpreter if not already using it
    if sys.executable != venv_python:
        print(f"[INFO] Re-launching with venv Python...")
        os.execv(venv_python, [venv_python] + sys.argv)
else:
    print("[WARN] No venv found, using system Python")

import os
import sys
import json
from pathlib import Path
from heal.scripts.generate import main as generate_main
from heal.scripts.filter import main as filter_main

PROJECT_ROOT = Path(__file__).parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"
STATE_FILE = EXPERIMENTS_DIR / "pipeline_state.json"

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"generate": False, "filter": False, "train": False, "evaluate": False}

def save_state(state):
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def log(msg):
    print(msg)
    with open(EXPERIMENTS_DIR / "pipeline.log", "a") as f:
        f.write(msg + "\n")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_problems", type=int, default=100, help="How many AIME problems to use")
    parser.add_argument("--base_samples", type=int, default=10, help="Trajectories per problem")
    parser.add_argument("--resume", action="store_true", help="Resume from last incomplete state")
    parser.add_argument("--toy", action="store_true", help="Use toy problem instead of AIME dataset (offline)")
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state() if args.resume else {"generate": False, "filter": False, "train": False, "evaluate": False}

    # 1. Generate trajectories
    if not state["generate"]:
        log("[1/4] Generating trajectories...")
        if args.toy:
            # Create a toy problem directly, avoiding dataset download
            from heal.data import save_jsonl
            toy_problems = [
                {"problem": "What is 2+2? Show steps.", "answer": "4"},
                {"problem": "If a train travels 60 mph for 2 hours, how far does it go?", "answer": "120 miles"},
            ]
            # Manually generate trajectories using teacher API
            from heal.teacher import generate_trajectories
            records = []
            for item in toy_problems:
                trajs = generate_trajectories(item["problem"], n=args.base_samples)
                for traj in trajs:
                    records.append({
                        "problem": item["problem"],
                        "answer": item["answer"],
                        "trajectory": traj,
                        "correct": True  # heuristic; we'll skip verification for toy
                    })
            save_jsonl(records, str(DATA_DIR / "trajectories.jsonl"))
            log(f"[Toy] Generated {len(records)} trajectories")
        else:
            # Original: use AIME dataset
            sys.argv = ["generate", "--num_problems", str(args.num_problems), "--base_samples", str(args.base_samples), "--output", str(DATA_DIR / "trajectories.jsonl")]
            try:
                generate_main()
            except Exception as e:
                log(f"[1/4] Failed: {e}")
                return
        state["generate"] = True
        save_state(state)
        log("[1/4] Done.")
    else:
        log("[1/4] Already done, skipping.")

    # 2. Filter/curate
    if not state["filter"]:
        log("[2/4] Filtering and curating...")
        sys.argv = ["filter", "--trajectories", str(DATA_DIR / "trajectories.jsonl"), "--output", str(DATA_DIR / "curated.jsonl")]
        try:
            filter_main()
            state["filter"] = True
            save_state(state)
            log("[2/4] Done.")
        except Exception as e:
            log(f"[2/4] Failed: {e}")
            return
    else:
        log("[2/4] Already done, skipping.")

    # 3. Train
    if not state["train"]:
        log("[3/4] Training student model...")
        # We'll directly call train() with parameters instead of sys.argv to avoid arg parsing issues
        try:
            from heal.data import load_jsonl
            curated_path = DATA_DIR / "curated.jsonl"
            samples = load_jsonl(str(curated_path))
            dataset = [{"instruction": s["problem"], "response": s["trajectory"]} for s in samples]
            # split 80/20 by problem grouping? For simplicity, random split on samples (not ideal but quick)
            split_idx = int(len(dataset) * 0.8)
            train_data = dataset[:split_idx]
            val_data = dataset[split_idx:]
            log(f"Train {len(train_data)} samples, val {len(val_data)}")
            from heal.train import train as train_func
            train_func(
                train_samples=train_data,
                val_samples=val_data,
                model_name="Qwen/Qwen2.5-1.5B-Instruct",
                output_dir=str(EXPERIMENTS_DIR / "checkpoint"),
                epochs=3,
                batch_size=1,
                lr=1e-5,
            )
            state["train"] = True
            save_state(state)
            log("[3/4] Done.")
        except Exception as e:
            log(f"[3/4] Failed: {e}")
            import traceback
            log(traceback.format_exc())
            return
    else:
        log("[3/4] Already done, skipping.")

    # 4. Evaluate
    if not state["evaluate"]:
        log("[4/4] Evaluating...")
        from heal.data import load_aime
        from heal.evaluate import evaluate_model
        test_problems = load_aime(split="train", num_samples=20, seed=999)
        metrics = evaluate_model(
            checkpoint_path=str(EXPERIMENTS_DIR / "checkpoint"),
            test_problems=test_problems,
            base_model="Qwen/Qwen2.5-1.5B-Instruct"
        )
        metrics_path = EXPERIMENTS_DIR / "metrics.json"
        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=2)
        state["evaluate"] = True
        save_state(state)
        log("[4/4] Done.")
    else:
        log("[4/4] Already done, skipping.")

    log("Pipeline complete!")
    if (EXPERIMENTS_DIR / "metrics.json").exists():
        with open(EXPERIMENTS_DIR / "metrics.json") as f:
            metrics = json.load(f)
        log(f"Pass@1: {metrics['pass@1']*100:.2f}% ({metrics['correct']}/{metrics['total']})")

if __name__ == "__main__":
    main()
