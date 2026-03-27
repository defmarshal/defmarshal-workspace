```python
#!/usr/bin/env python3
"""
Wikipedia AI Content Detection Demo
Simulates detection of AI-generated article content based on heuristics.
"""

import re
import sys
from collections import Counter
from typing import Dict, List, Tuple

class WikipediaAIDetector:
    """Detects potential AI-generated content in Wikipedia articles."""
    
    # Common AI-generated phrases and patterns
    AI_PATTERNS = [
        r'\b(in summary|it is important to note|furthermore|moreover|consequently)\b',
        r'\b(it is worth noting|plays a crucial role|serves as a foundation)\b',
        r'\b(a wide range of|various types of|multiple aspects of)\b',
        r'\b(both .* and .*|not only .* but also)\b',
        r'\b(significant|important|key|essential) (factor|aspect|role|element)\b',
        r'\b(in conclusion|to summarize|overall)\b',
    ]
    
    # Wikipedia-specific quality signals (human-written tends to have more)
    HUMAN_SIGNALS = [
        r'\[\d+\]',  # citations
        r'<ref>.*?</ref>',  # reference tags
        r'{{cite .*?}}',  # citation templates
        r'\\ conception\\b',  # sometimes AI overuses certain words
    ]
    
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.AI_PATTERNS]
        self.human_patterns = [re.compile(p, re.IGNORECASE) for p in self.HUMAN_SIGNALS]
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze text and return AI likelihood score and flags."""
        if not text or len(text.strip()) < 100:
            return {"error": "Text too short for analysis"}
        
        # Calculate metrics
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = re.findall(r'\b\w+\b', text.lower())
        word_count = len(words)
        unique_words = len(set(words))
        
        # 1. AI pattern density
        ai_matches = sum(len(p.findall(text)) for p in self.compiled_patterns)
        ai_density = ai_matches / max(len(sentences), 1)
        
        # 2. Sentence length variance (AI tends to be more uniform)
        sent_lengths = [len(s.split()) for s in sentences]
        avg_len = sum(sent_lengths) / len(sent_lengths) if sent_lengths else 0
        variance = sum((l - avg_len) ** 2 for l in sent_lengths) / len(sent_lengths) if sent_lengths else 0
        normalized_variance = variance / (avg_len ** 2) if avg_len > 0 else 0
        
        # 3. Lexical diversity (Type-Token Ratio)
        ttr = unique_words / word_count if word_count > 0 else 0
        
        # 4. Citation density (human Wikipedia articles typically have more)
        citation_count = sum(len(p.findall(text)) for p in self.human_patterns)
        citation_density = citation_count / (word_count / 100)  # per 100 words
        
        # 5. Formal transition word density
        transition_words = ['however', 'therefore', 'thus', 'furthermore', 'moreover', 
                           'consequently', 'nevertheless', 'meanwhile', 'additionally']
        transition_count = sum(text.lower().count(f' {w} ') for w in transition_words)
        transition_density = transition_count / (word_count / 100)
        
        # Scoring (heuristic weights)
        score = 0.0
        
        # High transition density -> more likely AI (weight positive)
        if transition_density > 2.0:
            score += 0.3
        elif transition_density < 0.5:
            score -= 0.2
        
        # Low citation density -> more likely AI
        if citation_density < 0.5:
            score += 0.2
        else:
            score -= 0.1
        
        # High AI pattern density -> more likely AI
        if ai_density > 0.3:
            score += 0.3
        elif ai_density < 0.1:
            score -= 0.2
        
        # Low lexical diversity can indicate AI (though depends on topic)
        if ttr < 0.4:
            score += 0.1
        
        # Low sentence variance (AI tends to write more uniformly)
        if normalized_variance < 0.5:
            score += 0.1
        
        # Normalize to 0-1 scale (simple clamp)
        score = max(0.0, min(1.0, score + 0.5))  # shift baseline
        
        # Determine flag
        is_ai_likely = score >= self.threshold
        
        flags = []
        if transition_density > 2.0:
            flags.append("High transition word density")
        if citation_density < 0.5:
            flags.append("Low citation density")
        if ai_density > 0.3:
            flags.append("AI pattern matches")
        if normalized_variance < 0.5:
            flags.append("Uniform sentence structure")
        
        return {
            "ai_likelihood": round(score, 3),
            "is_ai_likely": is_ai_likely,
            "flags": flags,
            "metrics": {
                "word_count": word_count,
                "unique_words": unique_words,
                "ttr": round(ttr, 3),
                "sentences": len(sentences),
                "avg_sentence_length": round(avg_len, 1),
                "ai_pattern_matches": ai_matches,
                "citation_count": citation_count,
                "transition_density_per_100w": round(transition_density, 2)
            }
        }

def simulate_wikipedia_patrol(article_text: str, detector: WikipediaAIDetector) -> None:
    """Simulate a Wikipedia patrol bot analyzing an article."""
    print("=" * 70)
    print("WIKIPEDIA AI CONTENT PATROL")
    print("=" * 70)
    
    # Truncate for display
    preview = article_text[:200] + "..." if len(article_text) > 200 else article_text
    print(f"\n📄 Article preview:\n{preview}\n")
    
    analysis = detector.analyze_text(article_text)
    
    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        return
    
    print("📊 ANALYSIS RESULTS:")
    print(f"  AI Likelihood: {analysis['ai_likelihood']*100:.1f}%")
    print(f"  Verdict: {'⚠️  AI-SUSPECTED' if analysis['is_ai_likely'] else '✅ LIKELY HUMAN'}")
    
    print("\n🔍 INDICATORS:")
    for flag in analysis['flags']:
        print(f"  • {flag}")
    
    print("\n📈 METRICS:")
    metrics = analysis['metrics']
    print(f"  Words: {metrics['word_count']}, Unique: {metrics['unique_words']}")
    print(f"  Type-Token Ratio: {metrics['ttr']}")
    print(f"  Avg sentence length: {metrics['avg_sentence_length']} words")
    print(f"  AI pattern matches: {metrics['ai_pattern_matches']}")
    print(f"  Citations (per 100w): {metrics['citation_density_per_100w']}")
    
    print("\n🎯 RECOMMENDED ACTION:")
    if analysis['is_ai_likely']:
        print("  Tag article with {{AI-generated}} template and flag for review.")
        print("  Consider reverting to last human-edited version if policy violation.")
    else:
        print("  No immediate action required. Continue routine patrol.")
    
    print("\n" + "=" * 70)

def sample_articles() -> Dict[str, str]:
    """Provide sample articles for demonstration."""
    return {
        "AI-generated sample (detected)": 
            "In summary, machine learning plays a crucial role in modern technology. "
            "Furthermore, artificial intelligence serves as a foundation for many applications. "
            "It is important to note that deep learning has revolutionized the field. "
            "Consequently, researchers are exploring new architectures. "
            "Moreover, neural networks have demonstrated remarkable capabilities. "
            "In conclusion, AI continues to evolve rapidly.",

        "Human-written Wikipedia style (clean)":
            "Machine learning (ML) is a field of artificial intelligence that focuses on building systems that learn from data. "
            "ML algorithms are used in a wide range of applications including email filtering, computer vision, and recommendation systems. "
            "[1] According to a 2023 survey, the global ML market was valued at $15.7 billion.[2] "
            "However, critics argue that ML systems can perpetuate existing biases if training data contains discriminatory patterns.[3] "
            "See also: Artificial intelligence, Deep learning, Data mining."
    }

def main():
    print("🧠 Wikipedia AI Content Detection System\n")
    
    detector = WikipediaAIDetector(threshold=0.5)
    samples = sample_articles()
    
    for i, (label, text) in enumerate(samples.items(), 1):
        print(f"\n{'='*70}")
        print(f"Sample {i}: {label}")
        print('='*70)
        simulate_wikipedia_patrol(text, detector)
    
    print("\n📋 SUMMARY:")
    print("  This demonstrates a heuristic-based AI content detector for Wikipedia.")
    print("  Real Wikipedia uses more sophisticated methods (e.g., GPTZero, GPT detectors)")
    print("  combined with human review. Policies evolve rapidly.")
    print("  Always verify before reverting edits!")

if __name__ == "__main__":
    main()
```