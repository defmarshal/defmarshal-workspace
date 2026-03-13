"""Teacher model interface using Step via OpenRouter API."""

import os
import time
from typing import List, Optional
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type

# Get API key: first from env, else from OpenClaw config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
if not OPENROUTER_API_KEY:
    try:
        import json
        cfg_path = "/home/ubuntu/.openclaw/workspace/openclaw.json"
        with open(cfg_path) as f:
            cfg = json.load(f)
        OPENROUTER_API_KEY = cfg.get("services", {}).get("openrouter", {}).get("apiKey", "")
    except Exception as e:
        print(f"[WARN] Could not load OpenRouter API key from config: {e}")
        OPENROUTER_API_KEY = ""

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "stepfun/step-3.5-flash"

client = openai.OpenAI(api_key=OPENROUTER_API_KEY, base_url=BASE_URL)


@retry(
    wait=wait_random_exponential(min=5, max=20),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(openai.RateLimitError),
)
def _call_step(prompt: str, temperature: float = 0.7, top_p: float = 0.8, max_tokens: int = 16384) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    msg = response.choices[0].message
    # Prefer content; fallback to reasoning (OpenRouter Step may put output there)
    if msg.content:
        return msg.content
    # Some models (Step) may return reasoning field instead of content
    reasoning = getattr(msg, "reasoning", None)
    if reasoning:
        return reasoning
    # If both missing, return empty string
    return ""


def generate_trajectories(problem: str, n: int = 30) -> List[str]:
    prompt = f"""Solve step by step.

{problem}

Solution:"""
    trajectories = []
    for _ in range(n):
        try:
            traj = _call_step(prompt, max_tokens=512)  # shorter for MVP
            if traj:
                trajectories.append(traj)
        except Exception as e:
            print(f"[WARN] Trajectory generation failed: {e}")
            time.sleep(2)
    return trajectories


def generate_with_hint(problem: str, hint: str, n: int = 5) -> List[str]:
    prompt = f"""Solve the following problem step by step, using the provided hint.

Problem: {problem}
Hint: {hint}

Provide a complete solution. End with the final answer on a line by itself: \\boxed{{answer}}."""
    trajectories = []
    for _ in range(n):
        try:
            traj = _call_step(prompt, temperature=0.5)
            if traj:
                trajectories.append(traj)
        except Exception as e:
            print(f"[WARN] Hint generation failed: {e}")
            time.sleep(5)
    return trajectories


def extract_boxed(text: str) -> str:
    """Extract content inside \\boxed{...}."""
    if "\\boxed{" in text:
        try:
            return text.split("\\boxed{")[1].split("}")[0].strip()
        except:
            return text.strip()
    return text.strip()


def normalize_answer(ans: str) -> str:
    """Normalize answer string for robust comparison."""
    ans = ans.lower().replace(",", "").replace(" ", "")
    # Remove common units? Keep as is.
    return ans


def evaluate_correctness(problem: str, trajectory: str, answer: Optional[str] = None) -> bool:
    """Determine if a trajectory is correct.
    If ground truth answer is provided, compare extracted answer.
    Otherwise, heuristically check presence of \\boxed{}.
    """
    pred = extract_boxed(trajectory)
    if answer is None:
        return "\\boxed{" in trajectory  # any answer present
    return normalize_answer(pred) == normalize_answer(answer)
