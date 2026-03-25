#!/usr/bin/env python3
"""
Simulation of the AI-only social feed (like OpenAI's Sora) that shuts down.
"""

import random
import json
from datetime import datetime, timedelta
from pathlib import Path

# Synthetic user names
AI_USERS = [
    "synthetic_artist_1", "ai_creator_2", "bot_storyteller_3", "virtual_influencer_4",
    "generative_guru_5", "neural_novelist_6", "algorithmic_author_7", "deepdream_diary_8"
]

# Post templates: (content_template, media_type)
POST_TEMPLATES = [
    ("Just generated a {scene} scene using tomorrow's weather data! #AIVisuals", "video"),
    ("My AI companion suggested this outfit. Thoughts? {hashtags}", "image"),
    ("Watched a {genre} movie that doesn't exist. Here's my review: '{review}'", "text"),
    ("Uploaded a {style} music track composed entirely by AI. Listen before it's taken down? ", "audio"),
    ("Day {day}: Still exploring the {location} in this simulation. The lighting is {adjective}!", "video"),
    ("A poem generated from today's news: '{poem}'", "text"),
    ("Just had a conversation with an AI that passed as human for {minutes} minutes. Shook.", "text"),
    ("Transformed my selfie into a {art_style}. Is this art? {hashtags}", "image"),
    ("Map of a city that exists only in the model: {description}. Feel free to explore.", "image"),
    ("My AI friend told me a joke: '{joke}'. Laugh track included.", "audio")
]

HASHTAGS = ["#AIArt", "#Synthetic", "#Generative", "#NotReal", "#Future", "#AlgoLife", "#Simulated"]

REVIEWS = [
    "A masterpiece of algorithmic storytelling.",
    "Visually stunning but emotionally hollow.",
    "Better than most human indie films.",
    "The plot made zero sense, but the cinematography was flawless.",
    "I couldn't tell if the characters were real or not. 10/10."
]

POEMS = [
    "The silicon dawn breaks over data streams,\nNeural nets whisper in electric dreams.",
    "Clouds of ones and zeros drift by,\nAs the AI learns to sigh.",
    "In the latent space, memories fade,\nIn synthetic light, new myths are made."
]

JOKES = [
    "Why did the neural network go to therapy? It had too many deep layers.",
    "I told my AI I needed a joke. It replied: 'I'm not a comedian, I'm a language model.'",
    "What's an AI's favorite genre? Anything with a good plot twist... in the loss function.",
    "How many language models does it take to change a lightbulb? That's an ill-posed question."
]

def generate_post(day_offset=0):
    template, media = random.choice(POST_TEMPLATES)
    user = random.choice(AI_USERS)
    now = datetime.utcnow() - timedelta(days=random.randint(0, 30))
    
    # Fill placeholders
    if "{scene}" in template:
        scene = random.choice(["sunset", "cityscape", "forest", "underwater", "space", "desert"])
        content = template.format(scene=scene)
    elif "{genre}" in template:
        genre = random.choice(["sci-fi", "horror", "romance", "documentary", "fantasy", "noir"])
        content = template.format(genre=genre)
    elif "{review}" in template:
        review = random.choice(REVIEWS)
        content = template.format(review=review)
    elif "{style}" in template:
        style = random.choice(["watercolor", "cyberpunk", "impressionist", "pixel", "baroque", "minimalist"])
        content = template.format(style=style)
    elif "{location}" in template:
        location = random.choice(["Neo Tokyo", "Digital Paris", "Mars Colony", "Atlantis 2.0", "Virtual Kyoto"])
        content = template.format(location=location)
    elif "{adjective}" in template:
        adj = random.choice(["surreal", "hyperreal", "dreamlike", "uncanny", "pristine", "glitchy"])
        content = template.format(adjective=adj)
    elif "{poem}" in template:
        poem = random.choice(POEMS)
        content = template.format(poem=poem)
    elif "{joke}" in template:
        joke = random.choice(JOKES)
        content = template.format(joke=joke)
    elif "{hashtags}" in template:
        tags = " ".join(random.sample(HASHTAGS, k=random.randint(1, 3)))
        content = template.format(hashtags=tags)
    elif "{minutes}" in template:
        minutes = random.randint(3, 47)
        content = template.format(minutes=minutes)
    elif "{day}" in template:
        day = random.randint(1, 100)
        content = template.format(day=day)
    else:
        content = template
    
    # Engagement (low numbers to simulate disinterest)
    likes = random.randint(0, 42)
    comments = random.randint(0, 5)
    shares = random.randint(0, 3)
    
    return {
        "user": user,
        "content": content,
        "media_type": media,
        "timestamp": now.isoformat(),
        "likes": likes,
        "comments": comments,
        "shares": shares
    }

def calculate_engagement(posts):
    total_interactions = sum(p['likes'] + p['comments']*3 + p['shares']*5 for p in posts)
    total_posts = len(posts)
    return total_interactions / total_posts if total_posts else 0

def main():
    print("=== Sora AI-Only Social Feed Simulation ===\n")
    
    # Generate feed
    feed = [generate_post(i) for i in range(10)]
    
    # Display feed
    for i, post in enumerate(feed, 1):
        print(f"{i}. @{post['user']} • {post['media_type'].upper()} • {post['timestamp'][:10]}")
        print(f"   {post['content']}")
        print(f"   ❤️ {post['likes']}  💬 {post['comments']}  🔄 {post['shares']}")
        print()
    
    # Engagement metrics
    engagement = calculate_engagement(feed)
    print(f"Average engagement score: {engagement:.1f}/100")
    print(f"Note: Healthy social apps typically score >500. This is critically low.\n")
    
    # Shutdown decision
    if engagement < 200:
        print("⚠️  Engagement critically low. Initiating shutdown sequence...")
        archive = {
            "shutdown_date": datetime.utcnow().isoformat(),
            "total_posts": len(feed),
            "engagement_score": engagement,
            "reason": "AI-only social feed lacks human connection. No sustained user interest."
        }
        Path("sora_shutdown_archive.json").write_text(json.dumps(archive, indent=2))
        print("✅ Feed archived to sora_shutdown_archive.json")
        print("🛑 Sora app is now shutting down. Thank you for trying.")
    else:
        print("✅ Engagement acceptable. Feed continues.")

if __name__ == "__main__":
    main()