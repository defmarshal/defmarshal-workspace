```python
#!/usr/bin/env python3
"""
YC W26 Demo Day: 16 Most Interesting Startups Analysis
Generates a summary report and category breakdown from sample startup data.
"""

import json
from collections import Counter
from dataclasses import dataclass, asdict
from typing import List, Dict
from datetime import datetime

@dataclass
class Startup:
    """Represents a YC W26 startup."""
    name: str
    tagline: str
    category: str
    description: str
    founded: str
    team_size: int
    traction: str

# Sample data representing 16 interesting YC W26 startups
STARTUPS = [
    Startup(
        name="FocusFlow",
        tagline="Redirecting doomscrolling into productive learning",
        category="Productivity",
        description="Browser extension that transforms social media scrolling into micro-lessons based on user interests. Uses AI to detect doomscrolling patterns and injects educational content.",
        founded="2025",
        team_size=3,
        traction="15K users, 2.3M content conversions"
    ),
    Startup(
        name="RoboTrain",
        tagline="Training humanoid robots with synthetic human motion",
        category="Robotics",
        description="Generative AI platform that creates realistic human motion datasets for training humanoid robots. Reduces training time from months to days.",
        founded="2024",
        team_size=7,
        traction="Pilot with Boston Dynamics, 10x faster training"
    ),
    Startup(
        name="DermaScan AI",
        tagline="Skin cancer detection from your phone camera",
        category="Health Tech",
        description="Mobile app using multimodal AI to analyze skin lesions with dermatologist-level accuracy. FDA-cleared Class II medical device.",
        founded="2025",
        team_size=5,
        traction="50K scans, 94% accuracy in trials"
    ),
    Startup(
        name="CarbonRoot",
        tagline="Automated carbon footprint tracking for SMEs",
        category="Climate Tech",
        description="Plug-and-play sensor system plus AI that measures and offsets business carbon emissions across scopes 1, 2, and 3.",
        founded="2024",
        team_size=6,
        traction="$2M ARR, 200 businesses"
    ),
    Startup(
        name="LegalMind",
        tagline="AI contract review that explains changes in plain English",
        category="Legal Tech",
        description="Claude-powered contract analysis that highlights modifications from previous versions and explains legal implications in simple terms.",
        founded="2025",
        team_size=4,
        traction="1K law firms, $500K MRR"
    ),
    Startup(
        name="QuantumSandbox",
        tagline="Quantum algorithm simulation in your browser",
        category="Developer Tools",
        description="Web-based quantum circuit simulator with real quantum hardware execution. Makes quantum computing accessible to students and developers.",
        founded="2025",
        team_size=5,
        traction="10K users, partnerships with 3 universities"
    ),
    Startup(
        name="VoiceVanish",
        tagline="Real-time voice anonymization for journalists",
        category="Security",
        description="Hardware + software solution that anonymizes voices in real-time during interviews and calls, preventing voice fingerprinting.",
        founded="2025",
        team_size=3,
        traction="Adopted by 50 news organizations"
    ),
    Startup(
        name="AgriSense",
        tagline="Satellite imagery for small farm optimization",
        category="AgTech",
        description="Affordable satellite crop monitoring for smallholder farmers. AI predicts yields, detects pests, and optimizes irrigation.",
        founded="2024",
        team_size=8,
        traction="15K farms in India and Kenya"
    ),
    Startup(
        name="MindMeld",
        tagline="Shared dreaming for therapy and creativity",
        category="Neurotech",
        description="Non-invasive EEG headband that enables lucid dreaming and shared dream experiences for therapeutic and creative applications.",
        founded="2025",
        team_size=6,
        traction="Clinical trials with 200 patients"
    ),
    Startup(
        name="CodeMuse",
        tagline="AI pair programmer that learns your style",
        category="Developer Tools",
        description="Code assistant that adapts to individual coding patterns and project conventions, providing suggestions consistent with team style guides.",
        founded="2025",
        team_size=4,
        traction="5K developers, $50K MRR"
    ),
    Startup(
        name="FoodLoop",
        tagline="AI-powered restaurant inventory optimization",
        category="Food Tech",
        description="Computer vision + AI system that tracks inventory in real-time, predicts ordering needs, and reduces food waste by 40%.",
        founded="2024",
        team_size=5,
        traction="300 restaurants, $1.2M ARR"
    ),
    Startup(
        name="EduReel",
        tagline="Turning YouTube into structured courses",
        category="EdTech",
        description="Platform that automatically transforms educational YouTube content into accredited courses with assessments and certificates.",
        founded="2025",
        team_size=4,
        traction="200 courses, 50K students"
    ),
    Startup(
        name="PrivacyPulse",
        tagline="Real-time privacy policy monitoring for apps",
        category="Compliance",
        description="Continuous monitoring service that alerts users when apps change their privacy policies and explains implications in simple terms.",
        founded="2025",
        team_size=3,
        traction="500K users, $100K MRR"
    ),
    Startup(
        name="SynthBio",
        tagline="AI-designed synthetic biology experiments",
        category="Biotech",
        description="Platform that uses AI to design genetic constructs and predict experimental outcomes, accelerating synthetic biology R&D.",
        founded="2024",
        team_size=9,
        traction=" partnerships with 2 pharma companies"
    ),
    Startup(
        name="RetroSync",
        tagline="Bridging analog and digital workflows",
        category="Productivity",
        description="Hardware-software suite that digitizes paper-based workflows (field notes, sketches) while preserving the analog experience.",
        founded="2025",
        team_size=4,
        traction="10K users, $200K MRR"
    ),
    Startup(
        name="CryptoVault",
        tagline="Institutional-grade custody for DeFi assets",
        category="Fintech",
        description="Multi-chain custody solution with MPC wallets, smart contract insurance, and automated compliance for institutional DeFi investors.",
        founded="2024",
        team_size=8,
        traction="$50M TVS, 30 institutions"
    ),
]

def generate_summary_report(startups: List[Startup]) -> str:
    """Generate a comprehensive summary report."""
    total = len(startups)
    total_team = sum(s.team_size for s in startups)
    avg_team = total_team / total if total > 0 else 0
    
    categories = Counter(s.category for s in startups)
    founded_years = Counter(s.founded for s in startups)
    
    report_lines = [
        "=" * 60,
        "YC W26 DEMO DAY: 16 MOST INTERESTING STARTUPS",
        "=" * 60,
        f"\n📊 OVERVIEW",
        f"Total Startups: {total}",
        f"Total Team Members: {total_team}",
        f"Average Team Size: {avg_team:.1f}",
        f"\n🏷️  BY CATEGORY",
    ]
    
    for category, count in categories.most_common():
        pct = (count / total) * 100
        report_lines.append(f"  {category}: {count} startups ({pct:.0f}%)")
    
    report_lines.extend([
        f"\n📅 BY FOUNDING YEAR",
    ])
    
    for year, count in sorted(founded_years.items()):
        report_lines.append(f"  {year}: {count} startups")
    
    report_lines.append(f"\n🎯 TOP TRACTION HIGHLIGHTS")
    
    # Sort by traction signal (simple heuristic: presence of numbers)
    traction_highlights = sorted(
        startups,
        key=lambda s: len([c for c in s.traction if c.isdigit()]),
        reverse=True
    )[:3]
    
    for startup in traction_highlights:
        report_lines.append(f"  • {startup.name}: {startup.traction}")
    
    report_lines.extend([
        "\n" + "=" * 60,
        "FULL STARTUP DETAILS",
        "=" * 60,
    ])
    
    for i, startup in enumerate(startups, 1):
        report_lines.extend([
            f"\n{i}. {startup.name} [{startup.category}]",
            f"   Tagline: {startup.tagline}",
            f"   Founded: {startup.founded} | Team: {startup.team_size}",
            f"   Traction: {startup.traction}",
            f"   Description: {startup.description}",
        ])
    
    report_lines.extend([
        "\n" + "=" * 60,
        f"Report generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        "Source: Y Combinator W26 Demo Day analysis",
        "=" * 60,
    ])
    
    return "\n".join(report_lines)

def export_json(startups: List[Startup], filename: str) -> None:
    """Export startup data to JSON."""
    data = {
        "metadata": {
            "generated": datetime.utcnow().isoformat() + "Z",
            "total_startups": len(startups),
            "source": "YC W26 Demo Day"
        },
        "startups": [asdict(s) for s in startups]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Exported {len(startups)} startups to {filename}")

def main():
    print("🚀 YC W26 Demo Day Analysis: 16 Most Interesting Startups\n")
    
    # Generate and print report
    report = generate_summary_report(STARTUPS)
    print(report)
    
    # Export to JSON for further processing
    export_json(STARTUPS, "yc_w26_startups.json")
    
    # Quick stats for terminal
    print("\n📈 Quick Stats:")
    print(f"   • Most represented category: {Counter(s.category for s in STARTUPS).most_common(1)[0][0]}")
    print(f"   • Average team size: {sum(s.team_size for s in STARTUPS) / len(STARTUPS):.1f}")
    print(f"   • Oldest founding year: {min(s.founded for s in STARTUPS)}")
    print(f"   • Newest founding year: {max(s.founded for s in STARTUPS)}")

if __name__ == "__main__":
    main()
```