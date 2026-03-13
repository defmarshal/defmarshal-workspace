"""PACE: Progressive Answer-guided Curriculum Evolution.

Constructs training curriculum in three stages:
- Stage I: Base samples (30 trajectories per problem)
- Stage II: Hint samples for hard problems (Pass@30 < 0.5)
- Stage III: Repair samples for extremely hard problems (Pass@30 == 0) from GEAR.
"""

from typing import List, Dict, Any
from .teacher import evaluate_correctness
from .gear import GEAR
from .pure import PURE
import numpy as np


def compute_pass_at_k(correct_flags: List[bool], k: int = 30) -> float:
    """Compute Pass@k (fraction of problems with at least one correct solution among k samples)."""
    if not correct_flags:
        return 0.0
    # For a single problem, among k samples, if any correct then pass=1
    # Here correct_flags is k booleans. Return 1 if any True else 0.
    return 1.0 if any(correct_flags[:k]) else 0.0


def assign_stage(
    problem: str,
    answer: str,
    base_trajs: List[str],
    hint_trajs: List[str],
    repair_trajs: List[str],
) -> List[Dict[str, str]]:
    """Build PACE curriculum: combine base, hint, repair according to rules.

    Returns list of training samples (each is a dict with 'instruction' and 'response').
    """
    # Evaluate base trajectories correctness
    base_correct = [evaluate_correctness(problem, t) for t in base_trajs]
    pass_at_30 = compute_pass_at_k(base_correct, k=len(base_trajs))

    training_samples = []

    # Stage I: Always include base samples
    for traj in base_trajs:
        training_samples.append({"instruction": problem, "response": traj})

    # Stage II: Add hint samples for hard problems (Pass@30 < 0.5)
    if pass_at_30 < 0.5:
        for traj in hint_trajs:
            training_samples.append({"instruction": problem, "response": traj})

    # Stage III: Add repair samples for extremely hard (Pass@30 == 0)
    if pass_at_30 == 0.0:
        for traj in repair_trajs:
            training_samples.append({"instruction": problem, "response": traj})

    return training_samples