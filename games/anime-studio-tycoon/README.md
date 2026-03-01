# Anime Studio Tycoon

A terminal-based management sim where you run an anime production studio.

## Goal
Complete **10 episodes** with **≥50,000 fans** and **positive reputation**.

## How to Play
```bash
python3 main.py
```

## Choices Each Week
1. **Hire animator** — +1 staff, costs ¥5,000
2. **Fire animator** — -1 staff, gain ¥2,000
3. **Train junior** — +1 staff, costs ¥3,000
4. **Rush episode** — risky fast fans (65% success)
5. **Quality focus** — +5 reputation, costs ¥2,000
6. **Run fan campaign** — +3,000–8,000 fans, costs ¥4,000
7. **Upgrade shop** — buy permanent studio upgrades
8. **Next week** — advance without action

## Upgrades
| Upgrade       | Cost    | Effect                                  |
|---------------|---------|-----------------------------------------|
| Render Farm   | ¥20,000 | Halves salary cost per animator         |
| Social Team   | ¥10,000 | +1,000 bonus fans per episode           |
| Merch Shop L1 | ¥8,000  | +¥3,000 passive income per week         |
| Merch Shop L2 | ¥15,000 | Upgrades passive income to +¥7,000/week |
| PR Agency     | ¥12,000 | Halves negative reputation events       |

## Events (Random, 15% chance per week)
- Viral clip, Streaming deal, Staff burnout, Budget overrun
- Positive review, Plagiarism claim, VA scandal, Award nomination
- Convention booth, Talented intern, Equipment failure, Investor interest
- Rival poaches staff, Crowdfunding surge, Merchandise boom, Delayed episode

## Tips
- Buy **Render Farm** first — it halves your wage bill permanently
- Chain **Merch Shop L1 → L2** for steady passive income
- Run **Fan Campaigns** regularly to hit the 50k target
- Keep reputation above 40 or quality will snowball negatively

## Version History
- v1.0 — Initial release
- v1.1 — Polish update: 16 events, upgrade shop, fan campaigns, balanced economy
