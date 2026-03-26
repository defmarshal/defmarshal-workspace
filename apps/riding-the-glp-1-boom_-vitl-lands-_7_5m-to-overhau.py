#!/usr/bin/env python3
"""
VITL E-Prescribing Marketplace - GLP-1 Boom Simulator
Demonstrates cash-pay clinic prescribing platform for GLP-1 medications
"""

import random
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Drug:
    name: str
    category: str  # e.g., GLP-1, SGLT2, Insulin
    avg_cash_price: float
    monthly_supply: int = 30

@dataclass
class Clinic:
    id: str
    name: str
    cash_prices: Dict[str, float]  # drug_name -> price
    inventory: Dict[str, int]  # drug_name -> quantity
    rating: float = 4.5
    patients_served: int = 0

@dataclass
class Patient:
    id: str
    name: str
    condition: str  # diabetes, obesity, etc.
    budget: float
    prescribed_drugs: List[str] = field(default_factory=list)
    total_spent: float = 0.0

class VITLMarketplace:
    def __init__(self):
        self.drugs = self._init_drugs()
        self.clinics: List[Clinic] = []
        self.patients: List[Patient] = []
        self.transactions = []
        self.revenue = 0.0
        self.funding_round = 0
        
    def _init_drugs(self) -> List[Drug]:
        return [
            Drug("Ozempic", "GLP-1", 950.0),
            Drug("Wegovy", "GLP-1", 1200.0),
            Drug("Mounjaro", "GLP-1", 1050.0),
            Drug("Zepbound", "GLP-1", 1100.0),
            Drug("Rybelsus", "GLP-1", 850.0),
            Drug("Trulicity", "GLP-1", 900.0),
        ]
    
    def add_clinic(self, clinic: Clinic):
        self.clinics.append(clinic)
        
    def add_patient(self, patient: Patient):
        self.patients.append(patient)
        
    def match_patient(self, patient: Patient) -> Optional[Clinic]:
        """Find best clinic for patient's prescribed drugs within budget"""
        if not patient.prescribed_drugs:
            return None
            
        eligible_clinics = []
        for clinic in self.clinics:
            # Check if clinic has all needed drugs in stock
            has_all = all(drug in clinic.cash_prices for drug in patient.prescribed_drugs)
            if not has_all:
                continue
                
            # Calculate total cost
            total_cost = sum(clinic.cash_prices[drug] for drug in patient.prescribed_drugs)
            if total_cost <= patient.budget:
                eligible_clinics.append((clinic, total_cost))
        
        if not eligible_clinics:
            return None
            
        # Sort by total cost (lowest first), then by rating
        eligible_clinics.sort(key=lambda x: (x[1], -x[0].rating))
        return eligible_clinics[0][0]
    
    def process_transaction(self, patient: Patient, clinic: Clinic) -> bool:
        """Complete a prescription purchase"""
        total_cost = sum(clinic.cash_prices[drug] for drug in patient.prescribed_drugs)
        
        if total_cost > patient.budget:
            return False
            
        # Deduct inventory
        for drug in patient.prescribed_drugs:
            clinic.inventory[drug] -= 1
            
        # Update patient and clinic
        patient.total_spent += total_cost
        clinic.patients_served += 1
        self.revenue += total_cost * 0.05  # VITL takes 5% platform fee
        
        self.transactions.append({
            'timestamp': datetime.now(),
            'patient_id': patient.id,
            'clinic_id': clinic.id,
            'drugs': patient.prescribed_drugs.copy(),
            'total_cost': total_cost,
            'platform_fee': total_cost * 0.05
        })
        return True
    
    def simulate_month(self, new_patients: int = 10):
        """Simulate one month of operations"""
        print(f"\n🗓️  Month {self.funding_round + 1}: Simulating {new_patients} new patients...")
        
        # Generate new patients with GLP-1 needs
        for i in range(new_patients):
            patient = Patient(
                id=f"PAT-{len(self.patients)+1:04d}",
                name=f"Patient {len(self.patients)+1}",
                condition=random.choice(["Type 2 Diabetes", "Obesity", "Weight Management"]),
                budget=random.uniform(800, 1500)
            )
            # Most need one GLP-1 drug, some need combinations
            num_drugs = 1 if random.random() < 0.7 else 2
            patient.prescribed_drugs = random.sample([d.name for d in self.drugs], num_drugs)
            self.patients.append(patient)
            
            # Try to match
            clinic = self.match_patient(patient)
            if clinic:
                success = self.process_transaction(patient, clinic)
                status = "✅ Prescribed" if success else "❌ Failed"
                print(f"  {status}: {patient.name} ({patient.condition}) → {clinic.name} | ${sum(clinic.cash_prices[d] for d in patient.prescribed_drugs):.0f}")
            else:
                print(f"  ⚠️  No clinic found for {patient.name} (budget: ${patient.budget:.0f})")
                
        self.funding_round += 1
        
    def apply_funding(self, amount: float):
        """Simulate receiving $7.5M funding and expanding"""
        print(f"\n💰 Funding Round {self.funding_round + 1}: ${amount/1_000_000:.1f}M raised!")
        print("   Expanding marketplace...")
        
        # Add new clinics
        new_clinics = int(amount / 500_000)  # Roughly 1 clinic per $500k
        for i in range(new_clinics):
            clinic = Clinic(
                id=f"CLINIC-{len(self.clinics)+1:04d}",
                name=f"VITL Partner Clinic #{len(self.clinics)+1}",
                cash_prices={drug.name: drug.avg_cash_price * random.uniform(0.9, 1.1) for drug in self.drugs},
                inventory={drug.name: random.randint(10, 50) for drug in self.drugs},
                rating=random.uniform(3.8, 5.0)
            )
            self.add_clinic(clinic)
            print(f"   + Added {clinic.name} (rating: {clinic.rating:.1f})")
            
    def print_summary(self):
        """Print marketplace summary"""
        print("\n" + "="*60)
        print("📊 VITL MARKETPLACE SUMMARY")
        print("="*60)
        print(f"Total Clinics: {len(self.clinics)}")
        print(f"Total Patients: {len(self.patients)}")
        print(f"Total Transactions: {len(self.transactions)}")
        print(f"Platform Revenue: ${self.revenue:,.2f}")
        print(f"Average Transaction: ${self.revenue/max(1, len(self.transactions)):,.2f}")
        print(f"Patients Served (by clinics): {sum(c.patients_served for c in self.clinics)}")
        print("\nTop 3 Clinics by Volume:")
        top_clinics = sorted(self.clinics, key=lambda c: c.patients_served, reverse=True)[:3]
        for i, clinic in enumerate(top_clinics, 1):
            print(f"  {i}. {clinic.name}: {clinic.patients_served} patients, rating {clinic.rating:.1f}")
            
    def run_simulation(self, months: int = 6):
        """Run full simulation with funding rounds"""
        print("🏥 VITL GLP-1 E-Prescribing Marketplace Simulation")
        print("=" * 60)
        print("\nInitial state: 5 clinics, 0 patients")
        
        # Initial clinics
        for i in range(5):
            clinic = Clinic(
                id=f"CLINIC-{i+1:04d}",
                name=f"Pilot Clinic #{i+1}",
                cash_prices={drug.name: drug.avg_cash_price for drug in self.drugs},
                inventory={drug.name: 20 for drug in self.drugs},
                rating=4.2
            )
            self.add_clinic(clinic)
            
        # Initial funding
        self.apply_funding(7_500_000)
        
        # Monthly simulation
        for month in range(months):
            # Growing patient base each month
            new_patients = 10 + month * 5  # Accelerating growth
            self.simulate_month(new_patients)
            
            if (month + 1) % 2 == 0 and month < months - 1:
                # Additional funding every other month (simulating investor confidence)
                additional_funding = 5_000_000 * (1 + self.funding_round * 0.5)
                self.apply_funding(additional_funding)
                
        self.print_summary()
        
        print("\n" + "="*60)
        print("🎯 Key Insights:")
        print("="*60)
        print("• GLP-1 drugs dominate cash-pay clinic prescriptions")
        print("• Marketplace volume scales with clinic network size")
        print("• Platform fee model (5%) generates predictable revenue")
        print("• Funding enables rapid expansion and inventory buildup")
        print("• Patient matching efficiency is critical for retention")

def main():
    marketplace = VITLMarketplace()
    marketplace.run_simulation(months=6)

if __name__ == "__main__":
    main()