```python
#!/usr/bin/env python3
import math
import random

# Simple vector utilities (no numpy dependency)
def dot(a, b): return sum(x*y for x,y in zip(a,b))
def norm(v): return math.sqrt(dot(v,v))
def cosine(a, b): return dot(a,b)/(norm(a)*norm(b)+1e-8)

# Shared representation: 5-dimensional feature space
# Features: [platform_density, enemy_count, puzzle_complexity, exploration_openness, resource_abundance]
levels = {
    "mario_1": [0.9, 0.3, 0.1, 0.2, 0.4],   # Classic platforming
    "mario_2": [0.8, 0.5, 0.2, 0.3, 0.3],   # More enemies
    "zelda_1": [0.3, 0.4, 0.7, 0.8, 0.5],   # Puzzle-heavy, open
    "zelda_2": [0.2, 0.6, 0.6, 0.7, 0.4],   # Combat dungeons
    "metroid_1": [0.5, 0.5, 0.5, 0.6, 0.3], # Balanced
}

# Keyword to feature weight mapping (simplified language conditioning)
keyword_weights = {
    "platform": [0.8, 0.1, 0.0, 0.1, 0.0],
    "action": [0.2, 0.8, 0.0, 0.0, 0.0],
    "puzzle": [0.0, 0.0, 0.9, 0.1, 0.0],
    "explore": [0.0, 0.0, 0.0, 0.9, 0.1],
    "rich": [0.0, 0.0, 0.0, 0.0, 0.8],
}

def text_to_condition(text):
    """Convert natural language description to condition vector."""
    text = text.lower()
    vec = [0.0]*5
    for kw, w in keyword_weights.items():
        if kw in text:
            for i in range(5):
                vec[i] += w[i]
    # If no keywords matched, return uniform
    if all(v == 0 for v in vec):
        vec = [0.2]*5
    # Normalize
    n = math.sqrt(sum(v*v for v in vec))
    return [v/n for v in vec] if n>0 else vec

def blend_levels(level_ids, weights):
    """Weighted blend of level feature vectors."""
    blended = [0.0]*5
    total = sum(weights)
    for lid, w in zip(level_ids, weights):
        vec = levels[lid]
        for i in range(5):
            blended[i] += (w/total) * vec[i]
    return blended

def describe(vec):
    """Convert feature vector to human-readable description."""
    names = ["platforms", "enemies", "puzzles", "exploration", "resources"]
    descriptors = []
    for i, name in enumerate(names):
        if vec[i] > 0.7:
            descriptors.append(f"high {name}")
        elif vec[i] < 0.3:
            descriptors.append(f"low {name}")
        else:
            descriptors.append(f"moderate {name}")
    return ", ".join(descriptors)

def main():
    # Example condition from user
    user_prompt = "I want a level with lots of puzzles to solve and open spaces to explore"
    print(f"User prompt: '{user_prompt}'")
    condition = text_to_condition(user_prompt)
    print(f"Condition vector: {[round(x,2) for x in condition]}")
    
    # Find top-3 most similar existing levels
    similarities = []
    for lid, vec in levels.items():
        sim = cosine(condition, vec)
        similarities.append((sim, lid))
    similarities.sort(reverse=True)
    top3 = similarities[:3]
    print("\nTop 3 matching levels:")
    for sim, lid in top3:
        print(f"  {lid}: similarity={sim:.3f}, features={describe(levels[lid])}")
    
    # Blend the top 3 with similarity-based weights
    level_ids = [lid for _, lid in top3]
    weights = [sim for sim, _ in top3]
    blended = blend_levels(level_ids, weights)
    
    print("\nBlended level features:")
    print(f"  {[round(x,2) for x in blended]}")
    print(f"  Descriptor: {describe(blended)}")
    
    # Show that blending respects condition
    print("\nCondition vs. Blend similarity:", round(cosine(condition, blended),3))

if __name__ == "__main__":
    main()
```