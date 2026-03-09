#!/usr/bin/env python3
"""
TechCrunch Mobility: Rivian's R2 gambit analysis
A simple simulation of Rivian's strategic move with the R2 vehicle.
"""

class Vehicle:
    def __init__(self, name, price, range_miles, production_capacity):
        self.name = name
        self.price = price
        self.range_miles = range_miles
        self.production_capacity = production_capacity
    
    def __str__(self):
        return f"{self.name}: ${self.price:,}, {self.range_miles}mi range, {self.production_capacity:,} units/year"

class MarketSimulator:
    def __init__(self):
        self.r2 = Vehicle("Rivian R2", 45000, 300, 100000)
        self.competitors = {
            "Tesla Model Y": Vehicle("Tesla Model Y", 47000, 330, 500000),
            "Ford Mustang Mach-E": Vehicle("Ford Mach-E", 43000, 230, 200000)
        }
        self.strategic_advantage = "Adventure-focused with modular battery options"
    
    def calculate_market_share(self, year):
        """Simple market share projection based on price competitiveness and capacity."""
        avg_competitor_price = sum(v.price for v in self.competitors.values()) / len(self.competitors)
        price_advantage = avg_competitor_price - self.r2.price
        
        # Base market share starts at 2% and grows with price advantage and capacity
        base_share = 0.