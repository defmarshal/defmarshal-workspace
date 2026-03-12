#!/usr/bin/env python3
import random
import sys

EXPERTS = [
    "William Shakespeare", "Jane Austen", "Mark Twain", "Virginia Woolf",
    "Ernest Hemingway", "Toni Morrison", "James Baldwin", "Maya Angelou",
    "George Orwell", "Gabriel García Márquez", "Tech Journalist #47"
]

GENERIC_SUGGESTIONS = [
    "Use active voice.",
    "Avoid adverbs.",
    "Show, don't tell.",
    "Cut filler words.",
    "Vary sentence length.",
    "Use stronger verbs.",
    "Eliminate passive constructions.",
    "Be more concise.",
    "Add sensory details.",
    "Check your commas."
]

def generate_fake_expert_advice(text):
    expert = random.choice(EXPERTS)
    suggestion = random.choice(GENERIC_SUGGESTIONS)
    return f"\n📝 Expert Review by {expert}:\n   Suggestion: {suggestion}\n   (Applied to: '{text[:50]}...')\n"

def main():
    if len(sys.argv) > 1:
        user_text = " ".join(sys.argv[1:])
    else:
        user_text = input("Enter your text: ").strip()
    
    if not user_text:
        print("No text provided.")
        return
    
    print(f"\nOriginal text: {user_text}")
    print(generate_fake_expert_advice(user_text))
    print("💡 Remember: These are generic suggestions, not actual expert reviews.")

if __name__ == "__main__":
    main()