#!/usr/bin/env python3
"""Quick test of HEAL pipeline with a single toy math problem."""

import sys
sys.path.insert(0, "src")

from heal.teacher import generate_trajectories, generate_with_hint
from heal.gear import GEAR
from heal.pure import PURE
from heal.train import train
from heal.evaluate import evaluate_model
from heal.data import save_jsonl, load_jsonl

def main():
    # Toy problem
    problem = "What is 2+2? Show steps."
    answer = "4"
    print(f"Problem: {problem}")

    # 1. Generate base trajectories (teacher)
    print("Generating base trajectories...")
    base_trajs = generate_trajectories(problem, n=3)
    print(f"Got {len(base_trajs)} trajectories")
    if not base_trajs:
        print("ERROR: No trajectories generated. Check API.")
        return
    # Save base
    base_records = [{"problem": problem, "answer": answer, "trajectory": t} for t in base_trajs]
    save_jsonl(base_records, "data/toy_base.jsonl")

    # 2. Filter: add hint and repair (skip GEAR/PURE for now, just combine)
    print("Generating hint samples...")
    hints = generate_with_hint(problem, f"The answer is {answer}.", n=2)
    candidates = base_trajs + hints
    # PURE filter (may reduce)
    pure = PURE()
    filtered = pure.filter_trajectories(candidates)
    print(f"After PURE: {len(filtered)} trajectories")
    curated = [{"problem": problem, "answer": answer, "trajectory": t} for t in filtered]
    save_jsonl(curated, "data/toy_curated.jsonl")

    # 3. Train (tiny)
    print("Training...")
    dataset = [{"instruction": c["problem"], "response": c["trajectory"]} for c in curated]
    train(
        train_samples=dataset,
        val_samples=dataset[:1],
        model_name="Qwen/Qwen2.5-1.5B-Instruct",
        output_dir="experiments/toy_checkpoint",
        epochs=1,
        batch_size=1,
    )
    print("Training done.")

    # 4. Evaluate (same problem, trivial)
    metrics = evaluate_model(
        checkpoint_path="experiments/toy_checkpoint",
        test_problems=[{"problem": problem, "answer": answer}],
        base_model="Qwen/Qwen2.5-1.5B-Instruct",
    )
    print("Metrics:", metrics)

if __name__ == "__main__":
    main()
