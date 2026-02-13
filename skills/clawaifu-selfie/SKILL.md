---
- **Description:** Your AI waifu companion that sends anime-style selfies
- **Homepage:** https://github.com/swancho/clawaifu
- **Allowed Tools:** Bash(grok-selfie.sh:*), Read
---

# clawaifu - OpenClaw Waifu

**GitHub:** https://github.com/swancho/clawaifu

Send adorable random anime images from **Nekos API** – a free, open-source collection of 40k+ anime pictures, no API key needed! Perfect for sharing cute anime vibes anytime.

## When to Use

- User says "send a pic", "send me a pic", "send a photo", "send a selfie"
- User asks "what are you doing?", "how are you doing?", "where are you?"
- Any time you want to brighten someone's day with a random anime image! ✨

## Required Environment Variables

```bash
BOT_TOKEN=your_telegram_bot_token   # Required - Get from @BotFather
TELEGRAM_CHAT_ID=your_chat_id       # Required - Your Telegram chat ID
```

No API key needed – Nekos API is completely free and open!

## Usage

```bash
./grok-selfie.sh [caption] [rating]
```

The script fetches a random anime image from Nekos API and sends it to your Telegram chat.

### Arguments

1. `[caption]` (optional): Message to send with the image. Default: "Random anime from Nekos API! ✨"
2. `[rating]` (optional): Image rating filter – `safe` (default, SFW) or `explicit` (NSFW). Be responsible!

### Examples

```bash
./grok-selfie.sh "Here's a cute pic for you!" safe
./grok-selfie.sh "Thinking of you~" explicit
./grok-selfie.sh  # Default caption + safe rating
```

**Note:** Images are randomly selected from a fixed collection (not generated per prompt). This keeps it fast, free, and reliable! The API has 40k+ images, so you get great variety. For specific character/scene requests, a paid generator would be needed, but for spontaneous cute pics, Nekos is purr-fect! (◕‿◕)♡
