```python
#!/usr/bin/env python3
"""
Kentucky Farm Data Center Offer Simulator
Demonstrates the decision facing a farmer: $26M for a data center on their land.
"""

import time
from dataclasses import dataclass
from typing import List

@dataclass
class Farm:
    name: str
    acres: int
    annual_income: float  # Current farm income
    family_heritage: bool
    community_ties: int   # 1-10 scale

@dataclass
class Offer:
    amount: float
    company_name: str
    tax_implications: float
    land_use_clause: str
    community_impact: str

def evaluate_offer(farm: Farm, offer: Offer) -> dict:
    """Analyze the offer from the farmer's perspective."""
    
    # Simple financial analysis
    investment_return = offer.amount / farm.annual_income if farm.annual_income > 0 else float('inf')
    
    # Non-financial factors (subjective scoring)
    heritage_score = 10 if farm.family_heritage else 3
    community_score = farm.community_ties * 1.5
    
    # Negative factors
    land_loss_impact = farm.acres * 1000  # $1k per acre emotional value
    disruption_score = 7  # Construction disruption
    
    # Calculate composite score (higher = more likely to accept)
    financial_weight = 0.4
    non_financial_weight = 0.6
    
    financial_attractiveness = min(10, offer.amount / 5_000_000)  # Cap at 10 for $50M+
    non_financial_attractiveness = (heritage_score + (10 - community_score) + (10 - disruption_score)) / 3
    
    total_score = (financial_attractiveness * financial_weight + 
                   non_financial_attractiveness * non_financial_weight)
    
    return {
        'investment_multiple': investment_return,
        'financial_score': financial_attractiveness,
        'lifestyle_score': non_financial_attractiveness,
        'total_score': total_score,
        'recommendation': 'ACCEPT' if total_score >= 6 else 'REJECT'
    }

def main():
    print("=" * 60)
    print("Kentucky Farm Data Center Offer Simulator")
    print("=" * 60)
    print()
    
    # Sample farm scenario
    farm = Farm(
        name="Miller Family Farm",
        acres=240,
        annual_income=85_000,  # Typical Kentucky farm income
        family_heritage=True,
        community_ties=9  # Deep community roots
    )
    
    # The offer
    offer = Offer(
        amount=26_000_000,
        company_name="Major AI Company (unnamed)",
        tax_implications=26_000_000 * 0.23,  # ~23% capital gains tax
        land_use_clause="Full control for 50 years, renewable",
        community_impact="150 construction jobs, 20 permanent tech jobs"
    )
    
    print(f"FARM: {farm.name}")
    print(f"  - {farm.acres} acres in Lexington, KY")
    print(f"  - Current income: ${farm.annual_income:,}")
    print(f"  - Family owned for {4 if farm.family_heritage else 2} generations")
    print(f"  - Community involvement: {farm.community_ties}/10")
    print()
    
    print("THE OFFER:")
    print(f"  - Company: {offer.company_name}")
    print(f"  - Amount: ${offer.amount:,}")
    print(f"  - After taxes (~23%): ${offer.amount - offer.tax_implications:,.0f}")
    print(f"  - Term: {offer.land_use_clause}")
    print(f"  - Jobs: {offer.community_impact}")
    print()
    
    print("ANALYSIS:")
    analysis = evaluate_offer(farm, offer)
    
    print(f"  Investment return multiple: {analysis['investment_multiple']:.1f}x")
    print(f"    (How many years of farm income is this?)")
    print(f"  Financial attractiveness: {analysis['financial_score']:.1f}/10")
    print(f"  Lifestyle/community score: {analysis['lifestyle_score']:.1f}/10")
    print(f"  Overall decision score: {analysis['total_score']:.1f}/10")
    print()
    
    print("FACTORS WEIGHING AGAINST ACCEPTANCE:")
    print("  ✓ Family heritage (4+ generations on this land)")
    print("  ✓ Deep community ties (local church, school, market)")
    print("  ✓ Lifestyle: farming way of life vs corporate tenant")
    print("  ✓ Environmental concerns: data center water usage, energy")
    print("  ✓ Loss of agricultural land (limited supply)")
    print()
    
    print("FACTORS WEIGHING FOR ACCEPTANCE:")
    print("  ✗ Life-changing wealth ($26M = 306 years of farm income)")
    print("  ✗ Job creation for community")
    print("  ✗ Modern infrastructure investment")
    print()
    
    print("DECISION SIMULATION:")
    time.sleep(1)
    
    if analysis['recommendation'] == 'ACCEPT':
        print("💰 Financial logic suggests ACCEPTING the offer.")
        print("   But many farmers reject purely financial logic...")
    else:
        print("🏡 The non-financial factors overwhelmingly favor REJECTION.")
        print(f"   Score: {analysis['total_score']:.1f}/10 (need 6+ to accept)")
    
    print()
    print("REAL-WORLD CONTEXT:")
    print("  In 2024, multiple Kentucky farm families rejected similar")
    print("  data center offers despite $20-40M price tags, citing:")
    print("  - Preservation of agricultural heritage")
    print("  - Community opposition to industrial facilities")
    print("  - Environmental concerns (water, power)")
    print("  - Boom-bust tech cycle vs stable farming")
    print()
    print("  The 'major AI company' likely needs land for AI training")
    print("  clusters, but rural communities increasingly resist")
    print("  conversion of farmland to tech infrastructure.")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
```