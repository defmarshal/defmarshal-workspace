# Anime Studio Tycoon

A CLI management simulation where you run an anime studio.  
**v1.1** — polished with new events, fan growth mechanics, and revenue balance.

## Run
```
python3 games/anime-studio-tycoon/main.py
```

## Goal
Complete 10 episodes while maintaining positive reputation and at least **50 000 fans**.  
Don't go bankrupt, and don't let your reputation drop below zero!

## Controls
Each week you choose one action:

| # | Action | Cost | Effect |
|---|--------|------|--------|
| 1 | Hire animator | ¥5 000 | +1 staff |
| 2 | Fire animator | +¥2 000 | -1 staff |
| 3 | Train junior | ¥3 000 | +1 staff |
| 4 | Rush episode | — | +fans (65 % chance) or -rep (35 %) |
| 5 | Quality focus | ¥2 000 | +5 reputation |
| 6 | Marketing push | ¥4 000 | +fans (15 % of current + random) |
| 7 | Next week | — | Advance time |

## Economy
- **Salary**: ¥1 200/staff/week (keep your team lean early)
- **Merch income**: ¥0.005 per fan per week (grows as fans grow)
- **Episode aired**: +2 rep, +8 % fan bonus each time
- **Passive fan growth**: fans grow weekly based on staff size × reputation

## Random Events (15 types!)
> Good: viral clips, award nominations, crowdfunding, streaming deals, fan conventions, magazine features, meme characters…  
> Bad: budget overruns, equipment failures, key animators quitting, competitor releases, tax audits…

## Tips
- Build fan base early with Marketing; merch income snowballs
- Keep reputation above 60 — it multiplies fan growth
- Don't overhire early; salary drain will kill you
- After episode 5, merch income should start covering costs

Good luck, Studio Head! 🎬✨
