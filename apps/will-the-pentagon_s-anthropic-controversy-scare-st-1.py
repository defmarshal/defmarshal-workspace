#!/usr/bin/env python3

import random

def assess_defense_work_risk():
    """Simulate startup decision-making about defense contracts amid controversy."""
    factors = {
        "public_perception_risk": random.uniform(0.3, 0.9),
        "contract_complexity": random.choice([0.2, 0.5, 0.8]),
        "ethics_alignment": random.uniform(0.1, 0.7),
        "market_dependency": random.uniform(0.4, 0.95)
    }
    
    controversy_impact = 0.65  # Anthropic controversy baseline impact
    risk_score = sum(factors.values()) * controversy_impact / len(factors)
    
    return {
        "risk_level": "HIGH" if risk_score > 0.7 else "MODERATE" if risk_score > 0.4 else "LOW",
        "risk_score": round(risk_score, 2),
        "factors": factors,
        "recommendation": (
            "Consider diversification away from defense" if risk_score > 0.7 else
            "Proceed with caution and legal review" if risk_score > 0.4 else
            "Defense work appears viable"
        )
    }

def simulate_startup_population(num_startups=10):
    """Run assessment for multiple startups and show distribution."""
    results = [assess_defense_work_risk() for _ in range(num_startups)]
    high_risk = sum(1 for r in results if r["risk_level"] == "HIGH")
    return {
        "total": num_startups,
        "high_risk_count": high_risk,
        "high_risk_percentage": high_risk / num_startups * 100,
        "sample_results": results[:3]
    }

def main():
    print("Pentagon-Anthropic Controversy: Startup Defense Work Risk Assessment")
    print("=" * 60)
    
    analysis = simulate_startup_population()
    
    print(f"\nSimulation of {analysis['total']} startups:")
    print(f"  High-risk assessments: {analysis['high_risk_count']} ({analysis['high_risk_percentage']:.1f}%)")
    
    print("\nSample assessments:")
    for i, res in enumerate(analysis["sample_results"], 1):
        print(f"  Startup {i}: {res['risk_level']} risk (score: {res['risk_score']})")
        print(f"    Recommendation: {res['recommendation']}")
    
    print("\nKey factors influencing risk (0.0-1.0 scale):")
    sample_factors = analysis["sample_results"][0]["factors"]
    for factor, value in sample_factors.items():
        print(f"  {factor.replace('_', ' ').title()}: {value:.2f}")

if __name__ == "__main__":
    main()