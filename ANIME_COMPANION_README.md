# Anime Companion

A unified CLI tool that combines anime lookup (via Jikan API) with text-to-speech narration (via edge-tts). Search for anime, get detailed information, and generate audio narrations of synopses.

## Features

- 🔍 **Search** anime by title
- 📊 **Info** detailed MAL data including synopsis, genres, studios, trailer
- 🏆 **Top** list of top-ranked anime
- 📅 **Season** browse anime by season (current or specific year/season)
- 📅 **Upcoming** upcoming anime releases
- 🎙 **TTS** optionally generate MP3 narration of the synopsis using Microsoft Edge neural TTS

## Installation

The skill dependencies are already installed:
- `anime-lookup` (Jikan API client)
- `edge-tts` (Node.js TTS converter)

The `anime-companion` script is located at the workspace root.

### Prerequisites

- Python 3.6+
- Node.js (v18+ recommended)
- `curl`, `jq` (used by some operations)

Edge-TTS dependencies are installed in `skills/edge-tts/scripts/` via `npm install` (already done).

## Usage

### Via quick launcher

```bash
quick anime search "frieren"
quick anime info 52991
quick anime top 5
quick anime season 2025 spring
quick anime season  # current season
quick anime upcoming 10
quick anime info 52991 --tts  # generates audio narration
```

### Direct invocation

```bash
./anime-companion search "<query>"
./anime-companion info <mal_id> [--tts]
./anime-companion top [limit=10]
./anime-companion season [year] [season]
./anime-companion upcoming [limit=10]
```

## Examples

```bash
$ quick anime search "chainsaw man"
[52991] Sousou no Frieren — 28 eps, Finished Airing, ⭐ 9.28
...

$ quick anime info 52991
🎬 Sousou no Frieren
   English: Frieren: Beyond Journey's End
   MAL ID: 52991 | Score: 9.28 | Rank: #1
   Episodes: 28 | Status: Finished Airing
   Aired: Sep 29, 2023 to Mar 22, 2024
   Genres: Adventure, Drama, Fantasy
   Studios: Madhouse

📖 Synopsis:
[Full synopsis...]

$ quick anime info 52991 --tts
[Full info...]
🎙 Generating TTS narration...
✅ Audio saved to: /home/ubuntu/.openclaw/workspace/tts_output/anime_1770980524.mp3
```

## Output

**Search/Top/Season/Upcoming:**
Shows list with MAL ID, title, episodes, status, score.

**Info:**
Full details including title (Japanese & English), MAL ID, score, rank, episodes, status, aired dates, genres, studios, and synopsis. Optionally generates an MP3 file of the synopsis using edge-tts. Audio files are saved in `tts_output/` with timestamps.

## Notes

- Jikan API rate limits: 3 requests/sec, 60 req/min. The tool is polite; if you hit limits, wait a moment.
- TTS uses the `en-US-MichelleNeural` voice by default (clear, natural narration).
- The tool requires network connectivity for API calls.
- TTS generation may take several seconds depending on synopsis length.

## Future Ideas

- Cache TTS files for repeated queries
- Add more voice/language options
- Integrate with Telegram to send audio directly
- Store favorite anime in a personal list

## License

Part of the defmarshal workspace. Built for personal use with OpenClaw.
