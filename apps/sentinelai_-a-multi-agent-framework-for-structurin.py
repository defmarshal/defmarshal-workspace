```python
#!/usr/bin/env python3
"""
SentinelAI: Multi-agent framework for structuring and linking NG9-1-1 emergency data.
Demonstrates ingestion, normalization, correlation, and update coordination.
"""

import json
import hashlib
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional
from collections import defaultdict

@dataclass
class RawIncident:
    """Raw incident data from an external source."""
    source_id: str
    incident_type: str
    description: str
    location: str
    timestamp: str
    raw_data: Dict
    confidence: float = 1.0

@dataclass
class StructuredIncident:
    """Normalized, structured incident."""
    incident_id: str
    canonical_type: str
    descriptions: List[str]
    locations: List[str]
    timestamps: List[str]
    sources: List[str]
    confidence: float
    related_incidents: List[str]
    last_updated: str

class IngestionAgent:
    """Receives raw incident data from various sources."""
    
    def __init__(self):
        self.raw_incidents: List[RawIncident] = []
    
    def ingest(self, source_id: str, data: Dict) -> RawIncident:
        """Ingest a raw incident."""
        incident = RawIncident(
            source_id=source_id,
            incident_type=data.get('type', 'unknown'),
            description=data.get('description', ''),
            location=data.get('location', ''),
            timestamp=data.get('timestamp', datetime.now().isoformat()),
            raw_data=data,
            confidence=data.get('confidence', 1.0)
        )
        self.raw_incidents.append(incident)
        return incident

class StructuringAgent:
    """Normalizes incidents into canonical schema."""
    
    TYPE_MAPPING = {
        'traffic accident': 'traffic',
        'car crash': 'traffic',
        'vehicle collision': 'traffic',
        'fire': 'fire',
        'structure fire': 'fire',
        'wildfire': 'fire',
        'medical emergency': 'medical',
        'heart attack': 'medical',
        'injury': 'medical',
        'crime': 'crime',
        'burglary': 'crime',
        ' assault': 'crime',
        'natural disaster': 'disaster',
        'flood': 'disaster',
        'earthquake': 'disaster'
    }
    
    def normalize_type(self, raw_type: str) -> str:
        """Map raw incident types to canonical categories."""
        raw_lower = raw_type.lower()
        for key, canonical in self.TYPE_MAPPING.items():
            if key in raw_lower:
                return canonical
        return 'other'
    
    def structure(self, raw: RawIncident) -> StructuredIncident:
        """Convert raw incident to structured format."""
        incident_id = hashlib.sha256(
            f"{raw.source_id}:{raw.timestamp}:{raw.location}".encode()
        ).hexdigest()[:16]
        
        return StructuredIncident(
            incident_id=incident_id,
            canonical_type=self.normalize_type(raw.incident_type),
            descriptions=[raw.description],
            locations=[raw.location],
            timestamps=[raw.timestamp],
            sources=[raw.source_id],
            confidence=raw.confidence,
            related_incidents=[],
            last_updated=datetime.now().isoformat()
        )

class CorrelationAgent:
    """Links related incidents across sources."""
    
    def __init__(self, time_threshold_minutes: int = 30, distance_km: int = 5):
        self.time_threshold = time_threshold_minutes * 60  # seconds
        self.distance_threshold = distance_km  # simplified: same location string
    
    def are_related(self, inc1: StructuredIncident, inc2: StructuredIncident) -> bool:
        """Check if two incidents are likely the same event."""
        # Same location (string match for demo)
        loc_match = inc1.locations[0] == inc2.locations[0]
        
        # Time proximity
        t1 = datetime.fromisoformat(inc1.timestamps[0])
        t2 = datetime.fromisoformat(inc2.timestamps[0])
        time_diff = abs((t1 - t2).total_seconds())
        time_match = time_diff <= self.time_threshold
        
        # Type compatibility (same or related types)
        type_match = inc1.canonical_type == inc2.canonical_type
        
        return loc_match and time_match and type_match
    
    def correlate(self, incidents: List[StructuredIncident]) -> List[StructuredIncident]:
        """Group related incidents and merge them."""
        # Build correlation graph
        n = len(incidents)
        groups = []
        assigned = set()
        
        for i in range(n):
            if i in assigned:
                continue
            group = [i]
            assigned.add(i)
            
            for j in range(i + 1, n):
                if j not in assigned and self.are_related(incidents[i], incidents[j]):
                    group.append(j)
                    assigned.add(j)
            
            groups.append(group)
        
        # Merge incidents in each group
        merged = []
        for group_indices in groups:
            if len(group_indices) == 1:
                merged.append(incidents[group_indices[0]])
            else:
                merged_incident = self._merge_group([incidents[i] for i in group_indices])
                merged.append(merged_incident)
        
        return merged
    
    def _merge_group(self, group: List[StructuredIncident]) -> StructuredIncident:
        """Merge multiple incident reports into one canonical incident."""
        # Use highest confidence as base
        base = max(group, key=lambda x: x.confidence)
        
        # Collect all data
        all_descriptions = []
        all_locations = []
        all_timestamps = []
        all_sources = []
        
        for inc in group:
            all_descriptions.extend(inc.descriptions)
            all_locations.extend(inc.locations)
            all_timestamps.extend(inc.timestamps)
            all_sources.extend(inc.sources)
        
        deduplicate = lambda items: list(set(items))
        
        return StructuredIncident(
            incident_id=base.incident_id,
            canonical_type=base.canonical_type,
            descriptions=deduplicate(all_descriptions),
            locations=deduplicate(all_locations),
            timestamps=deduplicate(all_timestamps),
            sources=deduplicate(all_sources),
            confidence=min(1.0, sum(inc.confidence for inc in group) / len(group)),
            related_incidents=[],
            last_updated=datetime.now().isoformat()
        )

class UpdateAgent:
    """Handles conflicting information and updates incident records."""
    
    def resolve_conflicts(self, existing: StructuredIncident, new: StructuredIncident) -> StructuredIncident:
        """Merge new information into existing incident, resolving conflicts."""
        # For simplicity: append new data, keep all sources
        merged = StructuredIncident(
            incident_id=existing.incident_id,
            canonical_type=existing.canonical_type,  # assume same after correlation
            descriptions=list(set(existing.descriptions + new.descriptions)),
            locations=list(set(existing.locations + new.locations)),
            timestamps=list(set(existing.timestamps + new.timestamps)),
            sources=list(set(existing.sources + new.sources)),
            confidence=min(1.0, (existing.confidence + new.confidence) / 2),
            related_incidents=list(set(existing.related_incidents + new.related_incidents)),
            last_updated=datetime.now().isoformat()
        )
        return merged

class OutputAgent:
    """Produces final structured incident data."""
    
    def emit(self, incidents: List[StructuredIncident]) -> Dict:
        """Format incidents for downstream systems."""
        output = {
            'system': 'SentinelAI',
            'generated_at': datetime.now().isoformat(),
            'total_incidents': len(incidents),
            'incidents': [asdict(inc) for inc in incidents]
        }
        return output

class SentinelAIFramework:
    """Main orchestrator for multi-agent emergency data processing."""
    
    def __init__(self):
        self.ingestion = IngestionAgent()
        self.structuring = StructuringAgent()
        self.correlation = CorrelationAgent()
        self.updater = UpdateAgent()
        self.output = OutputAgent()
        self.incident_store: Dict[str, StructuredIncident] = {}
    
    def process_raw_source(self, source_id: str, raw_incidents: List[Dict]):
        """Process a batch of raw incidents from one source."""
        print(f"[*] Ingesting {len(raw_incidents)} incidents from {source_id}")
        
        # Ingest
        structured_raw = []
        for raw_data in raw_incidents:
            raw_inc = self.ingestion.ingest(source_id, raw_data)
            structured = self.structuring.structure(raw_inc)
            structured_raw.append(structured)
        
        # Correlate within this batch
        correlated = self.correlation.correlate(structured_raw)
        print(f"[+] Correlated into {len(correlated)} incident groups")
        
        # Merge with existing store
        for inc in correlated:
            if inc.incident_id in self.incident_store:
                existing = self.incident_store[inc.incident_id]
                merged = self.updater.resolve_conflicts(existing, inc)
                self.incident_store[inc.incident_id] = merged
            else:
                self.incident_store[inc.incident_id] = inc
        
        print(f"[*] Incident store now contains {len(self.incident_store)} unique incidents")
    
    def get_incidents_by_type(self, incident_type: str) -> List[StructuredIncident]:
        """Query incidents by canonical type."""
        return [inc for inc in self.incident_store.values() if inc.canonical_type == incident_type]
    
    def finalize(self) -> Dict:
        """Produce final output."""
        all_incidents = list(self.incident_store.values())
        return self.output.emit(all_incidents)

def simulate_emergency_data():
    """
    Demonstrate SentinelAI with sample emergency data from multiple sources.
    Simulates 911 calls, sensor networks, and social media feeds.
    """
    print("="*70)
    print("SENTINELAI: MULTI-AGENT EMERGENCY DATA INTEGRATION")
    print("="*70)
    print()
    
    framework = SentinelAIFramework()
    
    # Simulate multiple data sources
    sources = {
        'CAD_Phoenix': [
            {
                'type': 'traffic accident',
                'description': 'Multi-vehicle collision on I-10 near 7th Ave',
                'location': 'Phoenix, I-10',
                'timestamp': '2026-03-28T14:20:00',
                'confidence': 0.9
            },
            {
                'type': 'fire',
                'description': 'Structure fire reported at residential address',
                'location': 'Phoenix, Main St',
                'timestamp': '2026-03-28T14:25:00',
                'confidence': 0.85
            },
            {
                'type': 'medical emergency',
                'description': 'Person unconscious at shopping mall',
                'location': 'Phoenix, Mall',
                'timestamp': '2026-03-28T14:30:00',
                'confidence': 0.95
            }
        ],
        'SocialMedia_Twitter': [
            {
                'type': 'traffic accident',
                'description': 'Big wreck on I-10, traffic backed up for miles',
                'location': 'Phoenix, I-10',
                'timestamp': '2026-03-28T14:21:00',
                'confidence': 0.7
            },
            {
                'type': 'fire',
                'description': 'House on fire near Main St, smoke visible',
                'location': 'Phoenix, Main St',
                'timestamp': '2026-03-28T14:26:00',
                'confidence': 0.65
            }
        ],
        'SensorNetwork_Weather': [
            {
                'type': 'natural disaster',
                'description': 'Flash flood warning for Phoenix metro area',
                'location': 'Phoenix',
                'timestamp': '2026-03-28T14:15:00',
                'confidence': 0.8
            }
        ],
        'Hospital_ER': [
            {
                'type': 'medical emergency',
                'description': 'Mass casualty incident: multiple patients from traffic collision',
                'location': 'Phoenix, I-10',
                'timestamp': '2026-03-28T14:35:00',
                'confidence': 0.9
            }
        ]
    }
    
    # Process each source
    for source_id, incidents in sources.items():
        framework.process_raw_source(source_id, incidents)
    
    print()
    print("[*] FINAL INTEGRATED INCIDENT DATABASE")
    print("-"*70)
    
    # Show summaries by type
    for incident_type in ['traffic', 'fire', 'medical', 'disaster']:
        matches = framework.get_incidents_by_type(incident_type)
        if matches:
            print(f"\n{incident_type.upper()} INCIDENTS ({len(matches)}):")
            for inc in matches:
                print(f"  ID: {inc.incident_id}")
                print(f"    Locations: {', '.join(inc.locations)}")
                print(f"    Sources: {', '.join(inc.sources)}")
                print(f"    Confidence: {inc.confidence:.2f}")
                print(f"    Descriptions: {len(inc.descriptions)} reports")
                if inc.related_incidents:
                    print(f"    Related: {len(inc.related_incidents)} linked incidents")
    
    # Final output
    print()
    final_output = framework.finalize()
    print(f"[+] Generated final output with {final_output['total_incidents']} unique incidents")
    print("[+] SentinelAI processing complete. Data ready for emergency dispatch, analytics, and public alert systems.")
    print()
    print("="*70)
    print("KEY CONCEPTS DEMONSTRATED:")
    print("  • Multi-agent architecture: Ingestion, Structuring, Correlation, Update, Output")
    print("  • Data normalization across heterogeneous sources")
    print("  • Correlation by location, time, and type")
    print("  • Conflict resolution and source aggregation")
    print("  • Unified canonical incident representation")
    print("  • Scalable to real NG9-1-1 deployments")
    print("="*70)

if __name__ == "__main__":
    simulate_emergency_data()
```