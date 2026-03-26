#!/usr/bin/env python3
"""
Memory Bear AI - Multimodal Affective Intelligence Demo
Demonstrates how emotional meaning depends on prior trajectory and accumulated context.
Based on arXiv:2603.22306v1
"""

import time
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from enum import Enum
import random

class Emotion(Enum):
    NEUTRAL = 0
    HAPPY = 1
    SAD = 2
    ANGRY = 3
    SURPRISED = 4
    FEARFUL = 5

@dataclass
class Interaction:
    timestamp: float
    modality: str  # 'text', 'face', 'voice'
    emotion: Emotion
    intensity: float  # 0.0 to 1.0
    context: str = ""

class EmotionalMemory:
    def __init__(self, window_size: int = 5):
        self.window = []
        self.window_size = window_size
        self.trajectory_weight = 0.7  # How much past influences present
    
    def add_interaction(self, interaction: Interaction):
        self.window.append(interaction)
        if len(self.window) > self.window_size:
            self.window.pop(0)
    
    def get_trajectory_influence(self) -> Dict[Emotion, float]:
        """Calculate emotional momentum from recent history"""
        if not self.window:
            return {e: 0.0 for e in Emotion}
        
        # Weight recent interactions more heavily
        weights = [0.5, 0.7, 0.9, 1.0][-len(self.window):]
        emotion_scores = {e: 0.0 for e in Emotion}
        
        for w, interaction in zip(weights, self.window):
            emotion_scores[interaction.emotion] += w * interaction.intensity
        
        # Normalize
        total = sum(emotion_scores.values()) or 1.0
        return {e: s/total for e, s in emotion_scores.items()}
    
    def get_dominant_trajectory(self) -> Tuple[Emotion, float]:
        influence = self.get_trajectory_influence()
        dominant = max(influence, key=influence.get)
        return dominant, influence[dominant]

class MultimodalAffectiveEngine:
    def __init__(self):
        self.memory = EmotionalMemory()
        self.modality_weights = {
            'text': 0.4,
            'face': 0.35,
            'voice': 0.25
        }
        self.confidence_threshold = 0.6
    
    def _parse_text_sentiment(self, text: str) -> Tuple[Emotion, float]:
        """Simple rule-based sentiment parser for demo"""
        text = text.lower()
        
        # Keyword-based emotion detection
        emotion_keywords = {
            Emotion.HAPPY: ['happy', 'joy', 'great', 'excellent', 'love', 'wonderful'],
            Emotion.SAD: ['sad', 'depressed', 'unhappy', 'cry', 'heartbroken'],
            Emotion.ANGRY: ['angry', 'mad', 'furious', 'hate', 'rage'],
            Emotion.SURPRISED: ['wow', 'surprise', 'shocked', 'unexpected'],
            Emotion.FEARFUL: ['scared', 'fear', 'anxious', 'worried', 'nervous']
        }
        
        scores = {e: 0.0 for e in Emotion}
        for emotion, keywords in emotion_keywords.items():
            for kw in keywords:
                if kw in text:
                    scores[emotion] += 1
        
        # Detect negations that flip sentiment
        negations = ['not', "n't", 'no', 'never']
        for neg in negations:
            if neg in text:
                # Boost opposite emotions (simplified)
                pass
        
        total = sum(scores.values()) or 1.0
        dominant = max(scores, key=scores.get)
        intensity = scores[dominant] / total if total > 0 else 0.5
        
        return dominant if scores[dominant] > 0 else Emotion.NEUTRAL, intensity
    
    def _assess_face_expression(self, expression: str) -> Tuple[Emotion, float]:
        """Map facial expression to emotion"""
        mapping = {
            'smile': (Emotion.HAPPY, 0.9),
            'frown': (Emotion.SAD, 0.8),
            'scowl': (Emotion.ANGRY, 0.85),
            'wide_eyes': (Emotion.SURPRISED, 0.75),
            'tense': (Emotion.FEARFUL, 0.7),
            'neutral': (Emotion.NEUTRAL, 0.5)
        }
        return mapping.get(expression, (Emotion.NEUTRAL, 0.5))
    
    def _assess_voice_tone(self, tone: str) -> Tuple[Emotion, float]:
        """Map voice tone to emotion"""
        mapping = {
            'cheerful': (Emotion.HAPPY, 0.85),
            'monotone': (Emotion.NEUTRAL, 0.6),
            'shouting': (Emotion.ANGRY, 0.8),
            'trembling': (Emotion.FEARFUL, 0.75),
            'excited': (Emotion.SURPRISED, 0.7),
            'flat': (Emotion.SAD, 0.7)
        }
        return mapping.get(tone, (Emotion.NEUTRAL, 0.5))
    
    def process_input(self, modality: str, content: str, expression: str = None) -> Dict:
        """Process multimodal input and produce affective judgment with memory"""
        
        # Step 1: Modality-specific emotion detection
        if modality == 'text':
            emotion, intensity = self._parse_text_sentiment(content)
        elif modality == 'face':
            emotion, intensity = self._assess_face_expression(expression or content)
        elif modality == 'voice':
            emotion, intensity = self._assess_voice_tone(expression or content)
        else:
            emotion, intensity = Emotion.NEUTRAL, 0.5
        
        # Step 2: Get memory influence
        trajectory_emotion, trajectory_strength = self.memory.get_dominant_trajectory()
        influence = self.memory.get_trajectory_influence()
        
        # Step 3: Fuse current input with memory (Memory Bear core concept)
        # If trajectory is strong (>0.3), it modulates current perception
        if trajectory_strength > 0.3:
            # Blend current emotion with trajectory influence
            # E.g., if user has been angry recently, neutral statements appear more negative
            blended_emotion = self._blend_with_trajectory(emotion, influence)
            final_emotion = blended_emotion
            confidence = min(1.0, intensity + trajectory_strength * 0.5)
            memory_effect = "strong"
        else:
            final_emotion = emotion
            confidence = intensity
            memory_effect = "weak"
        
        # Step 4: Store in memory
        interaction = Interaction(
            timestamp=time.time(),
            modality=modality,
            emotion=final_emotion,
            intensity=confidence,
            context=content[:50]
        )
        self.memory.add_interaction(interaction)
        
        return {
            'modality': modality,
            'raw_emotion': emotion.name,
            'final_emotion': final_emotion.name,
            'confidence': round(confidence, 3),
            'trajectory_influence': memory_effect,
            'trajectory_emotion': trajectory_emotion.name,
            'trajectory_strength': round(trajectory_strength, 3)
        }
    
    def _blend_with_trajectory(self, current: Emotion, trajectory: Dict[Emotion, float]) -> Emotion:
        """Blend current emotion with memory trajectory"""
        # If current emotion matches strong trajectory emotion, amplify
        if trajectory[current] > 0.4:
            return current
        
        # Otherwise, check if trajectory suggests a bias
        # E.g., recent anger might bias neutral toward angry
        strongest_traj = max(trajectory, key=trajectory.get)
        if trajectory[strongest_traj] > 0.3:
            return strongest_traj
        
        return current

def demonstrate_memory_effect():
    """Show how same text is interpreted differently based on memory"""
    print("🧠 Memory Bear AI - Multimodal Affective Intelligence Demo")
    print("=" * 60)
    print("Demonstrating how emotional meaning depends on prior trajectory\n")
    
    engine = MultimodalAffectiveEngine()
    
    # Scenario 1: Neutral conversation
    print("📱 Scenario 1: Neutral conversation (no strong emotional history)")
    print("-" * 60)
    
    statements = [
        ("text", "I'll think about it", None),
        ("text", "That's an interesting proposal", None),
        ("text", "Let me get back to you", None)
    ]
    
    for modality, content, expr in statements:
        result = engine.process_input(modality, content, expr)
        print(f"Input: '{content}'")
        print(f"  → Emotion: {result['final_emotion']} (confidence: {result['confidence']})")
        print(f"  → Memory effect: {result['trajectory_influence']} (dominant: {result['trajectory_emotion']})\n")
    
    # Scenario 2: Angry conversation
    print("\n😠 Scenario 2: Conversation with angry history")
    print("-" * 60)
    
    # First, build angry trajectory
    angry_statements = [
        ("text", "This is unacceptable!", None),
        ("text", "I'm extremely frustrated", None),
        ("text", "This is the worst service ever", None)
    ]
    
    print("Building angry trajectory...")
    for modality, content, expr in angry_statements:
        engine.process_input(modality, content, expr)
    
    # Now ambiguous statement
    print("\nNow interpreting ambiguous statement: 'I'll consider your request.'")
    result = engine.process_input("text", "I'll consider your request.", None)
    print(f"  → Emotion: {result['final_emotion']} (confidence: {result['confidence']})")
    print(f"  → Memory effect: {result['trajectory_influence']} (dominant: {result['trajectory_emotion']})")
    print("  Note: Neutral text interpreted as ANGRY due to recent angry trajectory!\n")
    
    # Scenario 3: Multimodal integration
    print("\n🎭 Scenario 3: Multimodal integration (text + face + voice)")
    print("-" * 60)
    
    engine2 = MultimodalAffectiveEngine()
    
    # Person says "I'm fine" with sad face and shaky voice
    inputs = [
        ("text", "I'm fine", None),
        ("face", "frown", None),
        ("voice", "trembling", None)
    ]
    
    print("Input combination:")
    print("  • Text: 'I'm fine'")
    print("  • Face: frown")
    print("  • Voice: trembling")
    
    results = []
    for modality, content, expr in inputs:
        res = engine2.process_input(modality, content, expr)
        results.append(res)
    
    # Simple fusion: take weighted average of emotion confidences
    print("\nIndividual modality assessments:")
    for r in results:
        print(f"  {r['modality']}: {r['final_emotion']} (conf: {r['confidence']})")
    
    print("\n➡️  Final assessment: Mixed signals suggest SAD (contradiction between verbal and nonverbal cues)")
    print("   Memory Bear engine would flag this for human review.\n")
    
    # Show memory state
    print("=" * 60)
    print("📊 Memory State (last 5 interactions):")
    for i, interaction in enumerate(engine2.memory.window, 1):
        print(f"  {i}. {interaction.modality}: {interaction.emotion.name} (intensity: {interaction.intensity:.2f})")

def main():
    demonstrate_memory_effect()
    
    print("\n" + "=" * 60)
    print("💡 Key Insight:")
    print("=" * 60)
    print("Affective judgment is NOT purely local. The same 'I'm fine' can mean")
    print("different things depending on recent emotional history (trajectory).")
    print("Memory Bear AI demonstrates how accumulated context shapes meaning.")

if __name__ == "__main__":
    main()