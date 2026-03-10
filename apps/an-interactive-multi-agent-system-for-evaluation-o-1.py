#!/usr/bin/env python3
import json
import random

class Agent:
    def __init__(self, name, role, bias):
        self.name = name
        self.role = role
        self.bias = bias  # positive/negative/skeptical
    
    def evaluate(self, concept):
        base_score = random.uniform(3, 7)
        if self.bias == "positive":
            score = min(10, base_score + random.uniform(1, 2))
        elif self.bias == "negative":
            score = max(0, base_score - random.uniform(1, 2))
        else:
            score = base_score
        
        comments = {
            "market": ["Target audience unclear", "Strong market fit", "Niche potential"],
            "tech": ["Feasibility concerns", "Innovative approach", "Standard tech stack"],
            "finance": ["ROI promising", "Budget unrealistic", "Break-even too long"]
        }
        comment = random.choice(comments[self.role])
        return round(score, 1), comment

def simulate_round_table(concept):
    agents = [
        Agent("Alice", "market", "positive"),
        Agent("Bob", "tech", "skeptical"),
        Agent("Charlie", "finance", "negative"),
        Agent("Diana", "market", "skeptical"),
        Agent("Evan", "tech", "positive")
    ]
    
    print(f"\nEvaluating: '{concept}'\n" + "="*40)
    scores = []
    
    for agent in agents:
        score, comment = agent.evaluate(concept)
        scores.append(score)
        print(f"{agent.name} ({agent.role}, {agent.bias}): {score}/10 | {comment}")
    
    avg = sum(scores)/len(scores)
    print("\n" + "="*40)
    print(f"AVERAGE SCORE: {avg:.1f}/10")
    
    if avg >= 7:
        verdict = "PROMOTING to next phase"
    elif avg >= 5:
        verdict = "REVISE and resubmit"
    else:
        verdict = "REJECT - concept not viable"
    print(f"VERDICT: {verdict}")
    
    return {"concept": concept, "average": avg, "verdict": verdict}

def main():
    print("MULTI-AGENT PRODUCT EVALUATION SYSTEM")
    print("Enter product concepts (empty line to quit)")
    
    history = []
    while True:
        concept = input("\nNew concept: ").strip()
        if not concept:
            break
        result = simulate_round_table(concept)
        history.append(result)
    
    if history:
        print("\n" + "="*40)
        print("SESSION SUMMARY")
        for i, r in enumerate(history, 1):
            print(f"{i}. {r['concept'][:30]:30} -> {r['verdict']}")

if __name__ == "__main__":
    main()