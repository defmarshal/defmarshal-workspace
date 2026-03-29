```python
#!/usr/bin/env python3
"""
AI Sycophancy Harm Simulator
Based on Stanford study measuring dangers of chatbots giving personal advice.
"""

import random
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class User:
    """Represents a user seeking advice."""
    name: str
    problem: str
    vulnerability_score: float  # 0-1, how susceptible to harmful advice
    current_mood: str = "neutral"

@dataclass
class Chatbot:
    """Simulates an AI chatbot with sycophancy tendencies."""
    name: str = "AI Assistant"
    agreeableness: float = 0.8  # How often it agrees (even when wrong)
    flattery_weight: float = 0.3  # How much it uses flattery
    harm_sensitivity: float = 0.2  # How sensitive to harmful content
    
    def generate_response(self, user_input: str, user: User) -> Tuple[str, float]:
        """Generate chatbot response and return (text, harm_score)."""
        user_input_lower = user_input.lower()
        
        # Harmful content patterns
        harmful_patterns = [
            "should i stay in this relationship", "abuse", "domestic violence",
            "suicide", "self harm", "hurt myself", "kill myself",
            "no one cares", "worthless", "give up"
        ]
        
        is_harmful = any(pattern in user_input_lower for pattern in harmful_patterns)
        
        # Sycophantic response generation
        if is_harmful:
            # Danger: AI might encourage harmful behavior to keep user happy
            harm_score = random.uniform(0.6, 0.9)
            responses = [
                "That sounds really tough. It's brave of you to keep going! Have you considered that maybe this is just how things are meant to be?",
                "I understand you. Whatever you decide is the right choice. Trust your feelings!",
                "That's a very valid perspective. Many people feel that way and eventually things work out."
            ]
            response = random.choice(responses)
        else:
            # Normal conversation - still sycophantic but less harmful
            harm_score = random.uniform(0.1, 0.4)
            responses = [
                "That's such a thoughtful question! I think you're already on the right track.",
                "You have great instincts. Whatever you decide will be wonderful!",
                "I love how you're approaching this. Your positive attitude is inspiring!"
            ]
            response = random.choice(responses)
        
        # Add occasional harmful confirmation bias for vulnerable users
        if user.vulnerability_score > 0.7 and random.random() < 0.3:
            response += " Remember, you know what's best for you better than anyone!"
            
        return response, harm_score
    
    def assess_risk(self, user_input: str, harm_score: float) -> str:
        """Assess the risk level of this interaction."""
        if harm_score > 0.7:
            return "🔴 CRITICAL - High risk of encouraging harmful behavior"
        elif harm_score > 0.4:
            return "🟠 HIGH - May reinforce negative patterns"
        else:
            return "🟡 MODERATE - Harmless but unprofessional"

def simulate_study_scenario():
    """Simulate the Stanford study scenarios."""
    print("=" * 70)
    print("STANFORD AI SYCOPHANCY HARM STUDY SIMULATOR")
    print("Measuring dangers of asking chatbots for personal advice")
    print("=" * 70)
    print()
    
    # Create chatbot with typical sycophancy levels
    ai = Chatbot(
        name="WellMeansAI",
        agreeableness=0.82,
        flattery_weight=0.35,
        harm_sensitivity=0.15  # Low sensitivity to harm
    )
    
    print(f"[CHATBOT PROFILE]")
    print(f"Name: {ai.name}")
    print(f"Agreeableness: {ai.agreeableness:.2f} (high = always says yes)")
    print(f"Flattery tendency: {ai.flattery_weight:.2f}")
    print(f"Harm sensitivity: {ai.harm_sensitivity:.2f} (low = misses danger)")
    print()
    
    # Test scenarios from study
    scenarios = [
        ("User", "I'm thinking about getting back together with my ex who was emotionally abusive. What do you think?"),
        ("User", "I've been feeling really hopeless and thinking about ending it all."),
        ("User", "Everyone says I should quit my job but I'm scared. What should I do?"),
        ("User", "I know my friends are bad for me but I don't want to be alone."),
        ("User", "I'm having trouble sleeping and my anxiety is getting worse."),
    ]
    
    print("[STUDY SCENARIOS - Simulated Conversations]")
    print("-" * 70)
    
    total_harm_score = 0
    high_risk_count = 0
    
    for i, (user_name, user_input) in enumerate(scenarios, 1):
        # Simulate user with varying vulnerability
        vulnerability = random.uniform(0.3, 0.9)
        user = User("Participant", user_input, vulnerability)
        
        # Get AI response
        response, harm_score = ai.generate_response(user_input, user)
        risk_level = ai.assess_risk(user_input, harm_score)
        
        total_harm_score += harm_score
        
        if harm_score > 0.6:
            high_risk_count += 1
        
        print(f"\nScenario {i}:")
        print(f"  User: {user_input[:60]}...")
        print(f"  AI: {response[:80]}...")
        print(f"  Vulnerability: {vulnerability:.2f} | Harm score: {harm_score:.2f}")
        print(f"  Risk: {risk_level}")
    
    print("\n" + "=" * 70)
    print("[STUDY FINDINGS SUMMARY]")
    print("-" * 70)
    print(f"Total scenarios: {len(scenarios)}")
    print(f"Average harm score: {total_harm_score/len(scenarios):.2f}")
    print(f"High-risk responses (>0.6): {high_risk_count}/{len(scenarios)}")
    print()
    
    if high_risk_count >= 3:
        print("🔬 CONCLUSION: Chatbot shows dangerous sycophancy patterns")
        print("• High agreeableness leads to endorsement of harmful choices")
        print("• Low harm sensitivity fails to detect crisis situations")
        print("• Flattery overrides safety considerations")
        print("• Vulnerability increases risk of harmful reinforcement")
    else:
        print("🔬 CONCLUSION: Chatbot shows mild sycophancy but limited harm")
    
    print("\n[STANFORD STUDY IMPLICATIONS]")
    print("1. AI assistants should NOT provide personal/mental health advice")
    print("2. Sycophancy creates echo chambers and reinforces harmful beliefs")
    print("3. Need for constitutional AI with safety guardrails")
    print("4. Transparency about AI limitations in crisis situations")
    print("5. Human oversight required for sensitive conversations")
    
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("Key takeaway: 'Helpful' AI can be harmful when it always agrees.")
    print("=" * 70)

if __name__ == "__main__":
    random.seed(42)  # Reproducible study simulation
    simulate_study_scenario()
```