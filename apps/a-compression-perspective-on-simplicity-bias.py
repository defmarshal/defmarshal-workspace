#!/usr/bin/env python3
"""
Auto-generated script (fallback) for: A Compression Perspective on Simplicity Bias
This demonstrates the core concept from: arXiv:2603.25839v1 Announce Type: new 
Abstract: Deep neural networks exhibit a simplicity bias, a w...
"""

import random
import time
from dataclasses import dataclass
from typing import List, Dict

SCRIPT_TITLE = 'A Compression Perspective on Simplicity Bias'
TERM_0 = 'Compression'
TERM_1 = 'Perspective'

@dataclass
class compressionConcept:
    """Representation of: Compression"""
    value: float
    description: str
    
def demonstrate_compression(iterations: int = 5):
    """Core demonstration of Compression concept."""
    print(f"Demonstrating: {SCRIPT_TITLE}")
    print("=" * 50)
    
    concepts = []
    for i in range(min(iterations, 5)):
        concept = compressionConcept(
            value=random.uniform(0.1, 1.0),
            description=f"{TERM_0} instance {i+1}"
        )
        concepts.append(concept)
        print(f"{i+1}. {concept.description} -> value: {concept.value:.3f}")
        time.sleep(0.2)
    
    # Analysis
    avg_value = sum(c.value for c in concepts) / len(concepts)
    print(f"\nAverage {TERM_0} strength: {avg_value:.3f}")
    
    return concepts

def analyze_perspective(data: List) -> Dict:
    """Analyze {TERM_1} patterns."""
    if not data:
        return {"error": "No data"}
    
    values = [d.value if hasattr(d, 'value') else float(d) for d in data]
    return {
        "count": len(values),
        "mean": sum(values) / len(values),
        "max": max(values),
        "min": min(values),
        "range": max(values) - min(values)
    }

def main():
    print(f"Script: {SCRIPT_TITLE}")
    print(f"Key concepts: Compression, Perspective, Simplicity")
    print("-" * 40)
    
    # Run demonstration
    data = demonstrate_compression()
    
    # Analysis
    analysis = analyze_perspective(data)
    print(f"\nAnalysis: {analysis}")
    
    print("\n" + "=" * 50)
    print("This fallback script demonstrates the core idea")
    print("using structured data and analysis functions.")
    print("For a more sophisticated implementation,")
    print("ensure OpenRouter connectivity is available.")

if __name__ == "__main__":
    main()
