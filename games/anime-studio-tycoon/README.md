# Anime Studio Tycoon

**Version:** 1.2  
**Type:** Text-based tycoon / strategy  
**Platform:** Python 3

## Overview

You are the director of a scrappy anime studio. Hire animators, manage budgets, keep morale high, and air 10 episodes — all while growing your fanbase to 50,000 before the money runs out.

## Goal

- Complete **10 episodes**
- Reach **50,000+ fans**
- Keep reputation **≥ 0** and money **≥ 0**

## How to Play

```bash
python3 main.py
```

Each week you choose one action:

| # | Action | Effect |
|---|--------|--------|
| 1 | Hire animator | +1 staff, -¥5,000 |
| 2 | Fire animator | +¥2,000, -1 staff, -morale |
| 3 | Train junior | +1 staff, -¥3,000, +morale |
| 4 | Rush production | Fan spike but risk quality (-10 rep) |
| 5 | Quality focus | +5 rep, -¥2,000, +morale, streak bonus |
| 6 | Morale event | +20 morale, -¥1,500 |
| 7 | Merch campaign | Unlock passive weekly income (one-time) |
| 8 | Seek sponsor | 5-week deal; income based on rep+fans |
| 9 | Next week | Advance, no action |

## Income Sources

- **Advertising revenue** — small passive income based on fans × reputation
- **Merch campaign** — ~2% of fan count per week (after unlocking)
- **Sponsor deals** — 5-week income based on reputation and fan count
- **Episode licensing** — grows with each episode aired

## Random Events (20 types!)

From viral clips and critic reviews to staff burnout and investor interest — something unexpected can happen each week!

## Key Metrics

- **Morale** — Low morale causes overtime costs; affects episode quality
- **Reputation** — Determines sponsor value and episode quality multiplier
- **Streak bonus** — Consecutive quality-focus weeks yield growing fan bonuses

## Changelog

### v1.2 (2026-02-28) — Polish & Expansion
- Added morale system (0–100) with visual bar
- Added 16 new random events (20 total)
- Added merch campaign (passive income)
- Added sponsor deal system
- Added fan growth each week (reputation-based)
- Added ad revenue (passive)
- Added episode licensing income
- Added streak bonus for quality focus
- Balance overhaul: game is now winnable (tested: 61k fans in ~20 weeks)
- UI overhaul with box-drawing characters and formatted stats

### v1.1
- Initial release
