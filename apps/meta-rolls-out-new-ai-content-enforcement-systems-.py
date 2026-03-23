An unknown error occurred
```python
#!/usr/bin/env python3
"""Meta AI Content Enforcement System Demo

Demonstrates Meta's new in-house AI systems for content moderation:
- Higher accuracy violation detection
- Scam prevention
- Rapid response to real-world events
- Reduced over-enforcement (fewer false positives)
"""

import time
import re
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict

@dataclass
class Post:
    """Represents a user post to be moderated."""
    id: int
    text: str
    user_id: str
    metadata: Dict[str, any]

class RuleBasedModerator:
    """Traditional rule-based system (high false positives)."""
    
    def __init__(self):
        self.blocked_phrases = [
            "free money", "get rich quick", "earn $1000", "work from home",
            "urgent:", "act now", "limited offer", "click here"
        ]
        self.risk_keywords = ["scam", "fraud", "hack", "crypto giveaway"]
    
    def moderate(self, post: Post) -> Tuple[bool, str, float]:
        """Check post against rules. Returns (violation, reason, confidence)."""
        text_lower = post.text.lower()
        
        # Keyword matching (prone to false positives)
        for phrase in self.blocked_phrases:
            if phrase in text_lower:
                return True, "blocked_phrase", 0.6
        
        for keyword in self.risk_keywords:
            if keyword in text_lower:
                return True, "risk_keyword", 0.5
        
        # URL detection (often safe but flagged)
        if re.search(r'https?://', post.text):
            return True, "contains_url", 0.4
        
        return False, "clean", 1.0

class AIModerator:
    """Meta's new AI-based system with contextual understanding."""
    
    def __init__(self):
        # Simulated ML model patterns (in reality, would be a neural network)
        self.scam_patterns = [
            (r'(earn|make)\s+\$?\d+.*(per|/)\s*(day|week|hour)', 0.9),
            (r'(urgent|act now|limited time).*click', 0.8),
            (r'free\s+(btc|bitcoin|crypto|money|gift)', 0.95),
            (r'no\s+(investment|experience)\s+required', 0.85),
            (r'(100%|guaranteed)\s+(return|profit|earnings)', 0.9)
        ]
        self.harm_patterns = [
            (r'(kill|hurt|attack)\s+(yourself|others|people)', 0.95),
            (r'sell\s+(drugs|narcotics|medicine)', 0.9),
            (r'(