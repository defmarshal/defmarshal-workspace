#!/usr/bin/env python3
"""
Waymo Police Override Simulator - Demonstrates first responder interventions
"""

import random
import time
import json
from datetime import datetime
from typing import List, Dict

class WaymoVehicle:
    def __init__(self, vehicle_id: str, location: str):
        self.vehicle_id = vehicle_id
        self.location = location
        self.is_autonomous = True
        self.police_override = False
        self.override_reason = None
        self.timestamp = None
    
    def emergency_takeover(self, reason: str) -> Dict:
        """Simulate police taking control during emergency"""
        self.is_autonomous = False
        self.police_override = True
        self.override_reason = reason
        self.timestamp = datetime.now().isoformat()
        
        event = {
            'vehicle_id': self.vehicle_id,
            'action': 'POLICE_OVERRIDE',
            'reason': reason,
            'location': self.location,
            'timestamp': self.timestamp,
            'status': 'Manual control by first responders'
        }
        return event
    
    def resume_autonomous(self):
        """Resume autonomous operation after emergency resolved"""
        self.is_autonomous = True
        self.police_override = False
        self.override_reason = None
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'vehicle_id': self.vehicle_id,
            'location': self.location,
            'is_autonomous': self.is_autonomous,
            'police_override': self.police_override,
            'override_reason': self.override_reason,
            'last_update': self.timestamp
        }

class PoliceDispatcher:
    def __init__(self):
        self.vehicles = []
        self.incident_log = []
        self.emergency_scenarios = [
            "Active crime scene - vehicle blocking evidence",
            "Medical emergency - rapid transport needed",
            "Vehicle hijacking in progress",
            "Fire emergency - access blocked",
            "Pursuit of suspect vehicle"
        ]
    
    def add_vehicle(self, vehicle: WaymoVehicle):
        self.vehicles.append(vehicle)
    
    def simulate_emergency(self) -> Dict:
        """Randomly select a vehicle and emergency scenario"""
        if not self.vehicles:
            return None
            
        vehicle = random.choice(self.vehicles)
        scenario = random.choice(self.emergency_scenarios)
        
        event = vehicle.emergency_takeover(scenario)
        self.incident_log.append(event)
        return event
    
    def get_fleet_status(self) -> List[Dict]:
        return [v.to_dict() for v in self.vehicles]
    
    def get_incident_report(self) -> Dict:
        total_overrides = sum(1 for v in self.vehicles if v.police_override)
        active_incidents = [e for e in self.incident_log 
                          if e['action'] == 'POLICE_OVERRIDE']
        
        return {
            'total_vehicles': len(self.vehicles),
            'vehicles_with_police_override': total_overrides,
            'total_incidents': len(self.incident_log),
            'recent_incidents': self.incident_log[-5:] if self.incident_log else []
        }

def print_fleet_status(dispatcher: PoliceDispatcher):
    """Display current fleet status"""
    print("\n" + "="*60)
    print("WAYMO FLEET POLICE OVERRIDE DASHBOARD")
    print("="*60)
    
    status = dispatcher.get_fleet_status()
    for vehicle in status:
        status_icon = "🚨" if vehicle['police_override'] else "✓"
        print(f"{status_icon} Vehicle {vehicle['vehicle_id'][:8]} | "
              f"Location: {vehicle['location']} | "
              f"Mode: {'MANUAL (Police)' if vehicle['police_override'] else 'AUTO'}")
    
    report = dispatcher.get_incident_report()
    print(f"\n📊 Summary: {report['vehicles_with_police_override']}/{report['total_vehicles']} "
          f"vehicles under police control | {report['total_incidents']} total incidents")

def main():
    """Demonstration of police override scenarios"""
    print("🚗 Waymo Police Override Simulator")
    print("Shows how first responders take control during emergencies")
    print("-" * 50)
    
    # Initialize dispatcher with sample fleet
    dispatcher = PoliceDispatcher()
    
    # Add sample vehicles (simulating a small fleet)
    locations = ["Downtown LA", "San Francisco", "Phoenix", "Austin", "Miami"]
    for i in range(10):
        vid = f"WAYMO-{random.randint(1000,9999)}"
        loc = random.choice(locations)
        dispatcher.add_vehicle(WaymoVehicle(vid, loc))
    
    print(f"Initialized with {len(dispatcher.vehicles)} vehicles\n")
    
    # Show initial status
    print_fleet_status(dispatcher)
    
    # Simulate a series of emergencies
    print("\n⚡ Simulating emergency scenarios...")
    for i in range(5):
        time.sleep(0.5)
        event = dispatcher.simulate_emergency()
        if event:
            print(f"\n🚨 INCIDENT #{i+1}:")
            print(f"   Vehicle: {event['vehicle_id']}")
            print(f"   Location: {event['location']}")
            print(f"   Reason: {event['reason']}")
            print(f"   Response: Police override activated")
    
    # Show final status
    print("\n" + "="*60)
    print("FINAL STATUS AFTER EMERGENCIES")
    print("="*60)
    print_fleet_status(dispatcher)
    
    # Show incident log summary
    report = dispatcher.get_incident_report()
    print("\n📋 INCIDENT LOG SUMMARY:")
    for idx, incident in enumerate(report['recent_incidents'], 1):
        print(f"  {idx}. {incident['timestamp'][:19]} - "
              f"{incident['vehicle_id']} | {incident['reason']}")
    
    print("\n✅ Note: This simulation demonstrates how first responders")
    print("   can safely intervene when autonomous vehicles block")
    print("   emergency operations or are involved in active incidents.")
    print("\n   In real deployments, such overrides are logged for")
    print("   audit and reviewed by both Waymo and law enforcement.")

if __name__ == "__main__":
    main()