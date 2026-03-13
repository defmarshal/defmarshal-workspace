"""Generate trajectories for AIME problems using teacher Step."""

import argparse
import json
from tqdm import tqdm
from heal.data import load_aime, save_jsonl
from heal.teacher import generate_trajectories, evaluate_correctness

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_problems", type=int, default=20, help="Number of AIME problems to use")
    parser.add_argument("--base_samples", type=int, default=10, help="Trajectories per problem")
    parser.add_argument("--output", type=str, default="data/trajectories.jsonl")
    parser.add_argument("--split", type=str, default="train", help="Dataset split")
    args = parser.parse_args()

    problems = load_aime(split=args.split, num_samples=args.num_problems)
    records = []
    out_path = args.output
    # If previous partial output exists, resume?
    # For simplicity, we'll overwrite. Could add resume later.
    for i, item in enumerate(tqdm(problems, desc="Problems")):
        problem = item["problem"]
        answer = item.get("answer", "")
        trajs = generate_trajectories(problem, n=args.base_samples)
        for traj in trajs:
            records.append({
                "problem": problem,
                "answer": answer,
                "trajectory": traj,
                "correct": evaluate_correctness(problem, traj, answer)
            })
        # Periodically save
        if (i + 1) % 5 == 0:
            save_jsonl(records, out_path)
    save_jsonl(records, out_path)
    print(f"[DONE] Saved {len(records)} trajectories to {out_path}")

if __name__ == "__main__":
    main()
