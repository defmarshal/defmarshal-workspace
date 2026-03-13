"""Filter and curate trajectories using GEAR and PURE."""

import argparse
import json
from tqdm import tqdm
from heal.data import load_aime, save_jsonl, load_jsonl
from heal.teacher import generate_with_hint
from heal.gear import GEAR
from heal.pure import PURE

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trajectories", type=str, required=True, help="Base trajectories JSONL")
    parser.add_argument("--output", type=str, default="data/curated.jsonl")
    parser.add_argument("--num_hints", type=int, default=2, help="Hint samples per hard problem")
    parser.add_argument("--num_repairs", type=int, default=3, help="Repair candidates per extremely hard problem")
    args = parser.parse_args()

    # Load base trajectories
    base_records = load_jsonl(args.trajectories)
    # Group by problem
    problems = {}
    for r in base_records:
        p = r["problem"]
        if p not in problems:
            problems[p] = {"answer": r.get("answer", ""), "base": []}
        problems[p]["base"].append({
            "trajectory": r["trajectory"],
            "correct": r.get("correct", False)
        })

    # Initialize GEAR and PURE
    gear = GEAR()
    pure = PURE()

    curated = []
    for problem, data in tqdm(problems.items(), desc="Filtering"):
        base_trajs = [d["trajectory"] for d in data["base"]]
        base_correct = [d["correct"] for d in data["base"]]
        pass_rate = sum(base_correct) / len(base_correct) if base_correct else 0.0
        answer = data["answer"]

        candidates = list(base_trajs)
        # Hard problems: add hint samples
        if pass_rate < 0.5:
            hints = generate_with_hint(problem, f"The correct answer is {answer}.", n=args.num_hints)
            candidates.extend(hints)
        # Extremely hard: add repair samples via GEAR
        if pass_rate == 0.0:
            repairs = gear.run_gear(problem, base_trajs[:10])  # limit to 10
            if repairs:
                candidates.extend(repairs[:args.num_repairs])

        # Apply PURE filter
        filtered = pure.filter_trajectories(candidates)
        for traj in filtered:
            curated.append({"problem": problem, "answer": answer, "trajectory": traj})

    save_jsonl(curated, args.output)
    print(f"[DONE] Curated dataset: {len(curated)} samples from {len(problems)} problems")

if __name__ == "__main__":
    main()
