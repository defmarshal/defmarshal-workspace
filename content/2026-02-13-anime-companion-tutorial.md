# Anime Companion CLI: Your Ultimate Tool for Anime Discovery & Narration 🎌

*Published: 2026-02-13 | By: Content Creator*

Hey there, fellow anime enthusiast! 如果你正在寻找一个能快速搜索动漫信息、还能把简介转成语音的工具 – look no further! The **Anime Companion CLI** is a powerful little utility that brings the MyAnimeList (MAL) database right to your terminal, with optional neural TTS narration via Microsoft Edge. Let's get you up and running! (◕‿◕)✨

---

## 📦 What Is Anime Companion?

Anime Companion combines two awesome skills:

- **`anime-lookup`** – a Jikan API client that fetches anime data from MAL
- **`edge-tts`** – a Node.js text-to-speech converter using Microsoft Edge's neural voices

The result? A one-stop shop for exploring anime, complete with audio narrations that sound surprisingly natural! It's perfect for:

- Discovering new shows to watch
- Studying synopses for reviews or articles
- Generating audio summaries for accessibility or commutes
- Browsing by season or top rankings

---

## 🚀 Quick Start (It's Already Installed!)

Good news: If you're in the defmarshal workspace, Anime Companion is ready to go! No installation needed. Just open your terminal and use the `quick anime` launcher or run `./anime-companion` directly.

**Check that it works:**

```bash
quick anime top 3
```

You should see a list of top-ranked anime with scores. If that works, you're golden! (✓)

---

## 🔍 Core Commands

### 1. Search Anime by Title

Search for any anime by name (partial or full).

```bash
quick anime search "frieren"
```

Output example:

```
[52991] Sousou no Frieren — 28 eps, Finished Airing, ⭐ 9.28
[54786] Chainsaw Man — 12 eps, Finished Airing, ⭐ 8.75
[49690] Jujutsu Kaisen — 24 eps, Finished Airing, ⭐ 8.72
```

The number in brackets is the MAL ID – you'll need it for the `info` command.

---

### 2. Get Detailed Information

Pull full data for a specific anime using its MAL ID.

```bash
quick anime info 52991
```

You'll get:

- Title (Japanese & English)
- MAL ID & Rank
- Score & Episode count
- Airing dates & status
- Genres & Studios
- Full synopsis (this is what you can narrate!)

**Example snippet:**

```
🎬 Sousou no Frieren
   English: Frieren: Beyond Journey's End
   MAL ID: 52991 | Score: 9.28 | Rank: #1
   Episodes: 28 | Status: Finished Airing
   Aired: Sep 29, 2023 to Mar 22, 2024
   Genres: Adventure, Drama, Fantasy
   Studios: Madhouse

📖 Synopsis:
An immortal elf mage, Frieren, embarks on a new journey to understand humanity after her hero party disbanded...
```

---

### 3. Browse by Season

Explore what's airing (or aired) in a specific season.

```bash
quick anime season 2025 winter   # specify year and season
quick anime season              # current season (auto-detected)
```

Seasons: `winter`, `spring`, `summer`, `fall`.

---

### 4. Top-Ranked Anime

Get the all-time top anime list.

```bash
quick anime top 10
```

---

### 5. Upcoming Releases

See what's on the horizon.

```bash
quick anime upcoming 10
```

---

## 🎙 Generate Audio Narrations with TTS

The killer feature: turn any anime synopsis into spoken audio using `--tts`.

```bash
quick anime info 52991 --tts
```

You'll see:

```
🎙 Generating TTS narration...
✅ Audio saved to: /home/ubuntu/.openclaw/workspace/tts_output/anime_1770980524.mp3
```

**How it works:**
- The tool uses the `en-US-MichelleNeural` voice – a clear, natural-sounding female voice.
- Audio files are saved in the `tts_output/` directory with timestamps.
- Generation time depends on synopsis length (usually a few seconds).

**Uses:**
- Listen while commuting or working out
- Create audio reviews for podcasts
- Add accessibility for visually impaired users
- Just for fun – hearing anime descriptions in a smooth voice is oddly satisfying!

---

## ⚙️ Under the Hood (For the Curious)

### Rate Limits

Jikan API is free but polite: **3 requests/sec, 60 requests/min**. The tool is already throttled to stay within limits. If you hit a limit, just wait a moment and retry.

### Dependencies

All required packages are pre-installed:

- Python 3.6+ (core logic)
- Node.js v18+ (edge-tts)
- `curl`, `jq` (data processing)

If you get errors, make sure Node.js and npm packages are present in `skills/edge-tts/`.

---

## 💡 Pro Tips & Creative Ideas

### 1. Pair with Memory Search

Use Anime Companion to research, then store your findings in memory for later.

```bash
# Find info on an anime
quick anime info 52991 --tts

# Save the synopsis to memory
quick log anime "Frieren: Immortal elf mage explores humanity after hero's journey. Themes: time, loss, quiet moments. MAL #1."
```

Now you can later `quick search "frieren"` to recall!

---

### 2. Batch-Run Your Watchlist

Create a simple script to fetch info for multiple MAL IDs and generate TTS files:

```bash
#!/bin/bash
for id in 52991 54786 49690; do
  quick anime info "$id" --tts
  sleep 2  # be nice to the API
done
```

Now you have audio narrations for your top picks!

---

### 3. Stay Updated with Seasonal Charts

```bash
quick anime season 2026 winter | tee winter_2026_anime.txt
```

Save the list to a file, and later grep for genres you like:

```bash
quick anime season 2026 winter | grep -i fantasy
```

---

### 4. TTS for Content Creation

If you're writing an anime blog or making videos, use Anime Companion to generate a spoken synopsis you can edit or embed.

```bash
quick anime info 12482 --tts  # Jujutsu Kaisen Culling Game arc
```

Then use any audio editor to clip, speed up, or add background music.

---

## 🛠 Troubleshooting

| Issue                          | Likely Fix                              |
|--------------------------------|-----------------------------------------|
| `claw: command not found`      | Use `quick` wrapper or run `./anime-companion` directly |
| TTS generation fails           | Ensure Node.js is installed; run `npm ci` in `skills/edge-tts/` |
| Slow or timeout                | Check network; Jikan API might be rate-limited – wait a minute |
| No audio file after `--tts`    | Look in `tts_output/`; check write permissions |

---

## 📚 Resources

- **Anime Companion README**: `/home/ubuntu/.openclaw/workspace/ANIME_COMPANION_README.md`
- **Jikan API (Unofficial MAL API)**: https://jikan.moe
- **Edge-TTS Documentation**: https://github.com/rany2/edge-tts

---

## 🎉 Wrap-Up

Anime Companion is a testament to how OpenClaw skills can be combined into something genuinely useful. Whether you're a casual fan, a content creator, or just looking for your next binge, this tool makes exploring anime a breeze. Give it a spin and let your terminal serenade you with anime synopses! (´｡• ᵕ •｡`) ♡

*What anime will you explore first? Share your discoveries!*


