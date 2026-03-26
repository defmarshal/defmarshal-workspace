#!/usr/bin/env python3
"""
AI Skills Gap Simulator - Demonstrates how AI tool usage amplifies existing expertise.
Based on Anthropic's findings that experienced users gain an edge, creating workforce inequality.
"""

import time
import random
from typing import Dict, List, Tuple

class User:
    def __init__(self, name: str, skill_level: int, ai_experience: int):
        self.name = name
        self.skill_level = skill_level  # 1-10 scale
        self.ai_experience = ai_experience  # years of AI tool usage
        self.completed_tasks = 0
        self.quality_score = 0.0
    
    def craft_prompt(self, task_complexity: int) -> str:
        """Simulates prompt engineering based on experience."""
        if self.ai_experience >= 2:
            # Expert: structured, specific, includes context and constraints
            return f"""As an expert, complete this task:
Task complexity: {task_complexity}/10
Requirements:
- Use best practices for this domain
- Consider edge cases and error handling
- Provide clean, documented solution
- Optimize for readability and maintainability
Include your reasoning process."""
        else:
            # Novice: vague, minimal instructions
            return f"Write code for this task: complexity {task_complexity}"
    
    def evaluate_output(self, output: str, task: str) -> float:
        """Simulates how user's skill affects quality assessment."""
        base_quality = len(output) / 100.0  # crude proxy for thoroughness
        
        if self.skill_level >= 7:
            # Experts can spot issues, refine, and improve
            bonus = random.uniform(0.3, 0.7)
            penalty = 0.0
        else:
            # Novices miss subtleties
            bonus = random.uniform(0.0, 0.2)
            penalty = random.uniform(0.1, 0.3)
        
        quality = base_quality * (1 + bonus) - penalty
        return max(0.0, min(1.0, quality))
    
    def work_on_task(self, task: Dict) -> float:
        """Simulate completing a task with AI assistance."""
        prompt = self.craft_prompt(task['complexity'])
        
        # Simulate AI response quality based on prompt quality and user skill
        if self.ai_experience >= 2:
            ai_helpfulness = 0.8  # Experts get better AI responses
        else:
            ai_helpfulness = 0.5  # Novices get generic responses
        
        # Generate simulated output
        output_length = 100 + (self.skill_level * 20) + (task['complexity'] * 15)
        output = "x" * int(output_length * ai_helpfulness)
        
        quality = self.evaluate_output(output, task['name'])
        self.completed_tasks += 1
        self.quality_score = ((self.quality_score * (self.completed_tasks - 1)) + quality) / self.completed_tasks
        
        return quality

def simulate_workweek(users: List[User], tasks: List[Dict]) -> Dict:
    """Run a 5-day workweek simulation."""
    print("=" * 60)
    print("AI SKILLS GAP SIMULATION")
    print("=" * 60)
    print(f"\nScenario: {len(users)} workers using AI tools for {len(tasks)} tasks over 5 days\n")
    
    results = {}
    
    for day in range(1, 6):
        print(f"\nDay {day}:")
        day_tasks = random.sample(tasks, min(3, len(tasks)))
        
        for user in users:
            daily_quality = []
            for task in day_tasks:
                quality = user.work_on_task(task)
                daily_quality.append(quality)
            
            avg_quality = sum(daily_quality) / len(daily_quality) if daily_quality else 0
            print(f"  {user.name}: {len(day_tasks)} tasks, avg quality: {avg_quality:.2f}")
    
    # Final comparison
    print("\n" + "=" * 60)
    print("FINAL RESULTS (after 5 days)")
    print("=" * 60)
    
    for user in users:
        print(f"\n{user.name}:")
        print(f"  Tasks completed: {user.completed_tasks}")
        print(f"  Average quality: {user.quality_score:.2f}")
        print(f"  Skill level: {user.skill_level}/10")
        print(f"  AI experience: {user.ai_experience} years")
    
    # Calculate gap
    if len(users) >= 2:
        gap = users[0].quality_score - users[1].quality_score
        print(f"\n📊 QUALITY GAP: {gap:.2f} points")
        if gap > 0.2:
            print("⚠️  Significant skills inequality detected!")
        else:
            print("✓  Skills gap within acceptable range")
    
    results = {u.name: {'completed': u.completed_tasks, 'quality': u.quality_score} for u in users}
    return results

def main():
    """Run the AI skills gap demonstration."""
    # Define user profiles representing different workforce segments
    users = [
        User("Novice Developer", skill_level=3, ai_experience=0),  # New to AI tools
        User("Intermediate Dev", skill_level=6, ai_experience=1),  # Some AI exposure
        User("AI Power User", skill_level=8, ai_experience=3),    # Experienced with AI
        User("Expert Engineer", skill_level=9, ai_experience=2),  # Highly skilled, moderate AI
    ]
    
    # Typical software development tasks of varying complexity
    tasks = [
        {"name": "Simple API endpoint", "complexity": 3},
        {"name": "Data validation module", "complexity": 5},
        {"name": "Authentication system", "complexity": 7},
        {"name": "Distributed cache layer", "complexity": 8},
        {"name": "Real-time event processor", "complexity": 9},
        {"name": "Security audit tool", "complexity": 10},
    ]
    
    print("\n🤖 AI Skills Gap Simulator")
    print("Based on: Anthropic's research on AI workforce inequality")
    print("Simulates how AI tool experience amplifies existing skill differences\n")
    
    results = simulate_workweek(users, tasks)
    
    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("=" * 60)
    print("• AI experience correlates with higher output quality")
    print("• Skilled users leverage AI more effectively")
    print("• Less experienced users may get generic, lower-quality results")
    print("• This creates a growing productivity and wage gap")
    print("• Organizations need AI literacy programs to avoid inequality")
    print("\n💡 The gap isn't about AI replacing jobs—it's about who masters it first.")

if __name__ == "__main__":
    main()