```python
#!/usr/bin/env python3
"""AI Meeting Notetaker Demo

Simulates an AI notetaking device: records meeting, transcribes audio,
generates summary, extracts action items, and translates to another language.
Inspired by physical notetakers with live translation capabilities.
"""

import random
import time
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class MeetingSegment:
    """Represents a segment of meeting dialogue."""
    speaker: str
    text: str
    timestamp: float

class AINotetaker:
    """AI-powered meeting notetaker device."""
    
    def __init__(self, target_language: str = "es"):
        self.transcript: List[MeetingSegment] = []
        self.target_language = target_language
        self.summary = ""
        self.action_items = []
        self.translations = {}
        
    def record_segment(self, speaker: str, text: str):
        """Simulate recording audio and transcribing it."""
        seg = MeetingSegment(
            speaker=speaker,
            text=text,
            timestamp=time.time()
        )
        self.transcript.append(seg)
        print(f"[{speaker}] {text}")
        
    def generate_transcript(self) -> str:
        """Compile full transcript."""
        lines = [f"{seg.speaker}: {seg.text}" for seg in self.transcript]
        return "\n".join(lines)
    
    def ai_summarize(self) -> str:
        """Simulate AI summarization (in practice would use LLM API)."""
        speakers = set(seg.speaker for seg in self.transcript)
        total_segments = len(self.transcript)
        topics = self._extract_topics()
        
        summary = f"Meeting with {len(speakers)} participants ({', '.join(speakers)}). "
        summary += f"Discussion covered {len(topics)} main topics: {', '.join(topics)}. "
        summary += f"Total utterances: {total_segments}. "
        summary += "Key decisions: timeline agreed, resources allocated, next meeting scheduled."
        self.summary = summary
        return summary
    
    def _extract_topics(self) -> List[str]:
        """Simple keyword-based topic extraction (demo only)."""
        all_text = " ".join(seg.text.lower() for seg in self.transcript)
        potential_topics = ["project", "budget", "timeline", "features", "bug", "release", "marketing", "research"]
        found = [t for t in potential_topics if t in all_text]
        return found if found else ["general discussion"]
    
    def extract_action_items(self) -> List[Dict[str, str]]:
        """Extract action items from transcript (demo uses pattern matching)."""
        actions = []
        for seg in self.transcript:
            text = seg.text.lower()
            if any(keyword in text for keyword in ["will do", "responsible", "follow up", "action", "task", "assign"]):
                # Simple extraction - in reality would use NLP
                actions.append({
                    "assignee": seg.speaker,
                    "action": seg.text,
                    "due": "next meeting"
                })
        self.action_items = actions
        return actions
    
    def translate(self, text: str) -> str:
        """Simulate live translation to target language."""
        # In a real device, this would call a translation API
        translations = {
            "es": {
                "Hello": "Hola",
                "meeting": "reunión",
                "summary": "resumen",
                "action items": "elementos de acción",
                "project": "proyecto",
                "budget": "presupuesto",
                "timeline": "cronograma"
            }
        }
        if self.target_language in translations:
            words = text.split()
            translated = [translations[self.target_language].get(w.lower(), w) for w in words]
            return " ".join(translated)
        return f"[{self.target_language}] {text}"
    
    def generate_report(self) -> str:
        """Create full meeting report."""
        report = "=== AI MEETING NOTES ===\n\n"
        report += "SUMMARY:\n" + self.summary + "\n\n"
        report += "ACTION ITEMS:\n"
        for i, item in enumerate(self.action_items, 1):
            report += f"  {i}. {item['assignee']}: {item['action']} (Due: {item['due']})\n"
        report += "\nFULL TRANSCRIPT:\n" + self.generate_transcript()
        return report
    
    def live_translate_mode(self):
        """Demonstrate live translation during meeting."""
        print(f"\n--- LIVE TRANSLATION to {self.target_language.upper()} ---")
        for seg in self.transcript[-3:]:  # translate last 3 segments
            translated = self.translate(seg.text)
            print(f"[{seg.speaker}] {translated}")

def demo_meeting():
    """Demonstrate a typical meeting with AI notetaker."""
    print("=== AI NOTETAKER DEMO ===\n")
    print("Simulating a project sync meeting...\n")
    
    notetaker = AINotetaker(target_language="es")
    
    # Simulate meeting dialogue
    notetaker.record_segment("Alice", "Good morning! Let's start with the project timeline.")
    notetaker.record_segment("Bob", "We're on track for the March release, but the budget needs review.")
    notetaker.record_segment("Alice", "I'll send the updated budget by Friday. Action item for me.")
    notetaker.record_segment("Charlie", "The marketing team needs the feature list by next week.")
    notetaker.record_segment("Alice", "I'll provide that tomorrow. Charlie, can you follow up with the design team?")
    notetaker.record_segment("Charlie", "Yes, that's my action.")
    notetaker.record_segment("Bob", "Any risks? I'll monitor the testing budget closely.")
    time.sleep(0.5)
    
    print("\n--- AI PROCESSING ---\n")
    
    summary = notetaker.ai_summarize()
    print("SUMMARY:", summary[:200] + "...\n")
    
    actions = notetaker.extract_action_items()
    print("ACTION ITEMS:")
    for i, item in enumerate(actions, 1):
        print(f"  {i}. {item['assignee']}: {item['action'][:60]}...")
    
    # Show live translation
    notetaker.live_translate_mode()
    
    print("\n--- FULL REPORT ---")
    report = notetaker.generate_report()
    print(report[:500] + "\n... (truncated for demo)")
    
    print("\n=== CONCEPT DEMONSTRATED ===")
    print("• Audio recording and transcription")
    print("• AI summarization")
    print("• Action item extraction")
    print("• Live translation to Spanish")
    print("• Unified meeting notes export")

if __name__ == "__main__":
    demo_meeting()
```