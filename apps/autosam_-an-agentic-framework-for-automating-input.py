```python
#!/usr/bin/env python3
"""
AutoSAM Demo: Multi-modal RAG for automated SAM input generation
Simplified demonstration of the concept.
"""

import re
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Component:
    name: str
    type: str
    parameters: Dict[str, float]

class DocumentStore:
    """Simulated document store with P&IDs and specs."""
    def __init__(self):
        self.documents = {
            "p&id_main_coolant": """
                P-101A: Reactor Coolant Pump
                Flow rate: 15000 gpm
                Head: 300 ft
                
                V-101: Pressurizer
                Volume: 1500 ft3
                Design pressure: 2250 psia
                
                SG-101: Steam Generator
                Heat transfer area: 30000 ft2
                Tube material: Inconel-600
            """,
            "specs_materials": """
                Pipe schedule: STD for 8" and larger
                Stainless steel SA-312 TP304 for reactor coolant
                Inconel-600 for steam generator tubes
                Design temperature: 650°F (reactor coolant)
            """,
            "system_description": """
                The RCS consists of two loops. Each loop has:
                - 1 reactor coolant pump
                - 1 steam generator
                - 1 hot leg
                - 1 cold leg
                - 1 pressurizer connected to hot leg
            """
        }
    
    def search(self, query: str) -> List[str]:
        """Simple keyword search across documents."""
        results = []
        for doc_name, content in self.documents.items():
            if any(word in content.lower() for word in query.lower().split()):
                results.append(f"[{doc_name}] {content[:200]}...")
        return results

class SAMInputGenerator:
    """Generates SAM input files from extracted parameters."""
    
    def __init__(self):
        self.components: List[Component] = []
    
    def add_component(self, comp: Component):
        self.components.append(comp)
    
    def generate_input_file(self) -> str:
        """Generate SAM input file in standard format."""
        lines = [
            "*** SAM INPUT FILE - AutoSAM Generated ***",
            "* Components",
        ]
        
        for comp in self.components:
            if comp.type == "pump":
                lines.append(f"PUMP {comp.name}")
                lines.append(f"  FLOW_RATE = {comp.parameters.get('flow_rate', 0)}")
                lines.append(f"  HEAD = {comp.parameters.get('head', 0)}")
                lines.append("  /")
            elif comp.type == "volume":
                lines.append(f"VOLUME {comp.name}")
                lines.append(f"  VOL = {comp.parameters.get('volume', 0)}")
                lines.append(f"  PRES = {comp.parameters.get('pressure', 0)}")
                lines.append("  /")
            elif comp.type == "heat_structure":
                lines.append(f"HEAT_STRUCTURE {comp.name}")
                lines.append(f"  AREA = {comp.parameters.get('area', 0)}")
                lines.append(f"  MATERIAL = {comp.parameters.get('material', 'STEEL')}")
                lines.append("  /")
        
        lines.extend([
            "",
            "* End of AutoSAM generated input",
            "***"
        ])
        return "\n".join(lines)

def extract_parameters(text: str) -> Dict[str, float]:
    """Extract numerical parameters from text."""
    params = {}
    flow_match = re.search(r'flow\s+rate[:\s]+([\d.]+)\s*(gpm|gallon)', text, re.IGNORECASE)
    if flow_match:
        params['flow_rate'] = float(flow_match.group(1))
    
    head_match = re.search(r'head[:\s]+([\d.]+)\s*(ft|feet)', text, re.IGNORECASE)
    if head_match:
        params['head'] = float(head_match.group(1))
    
    vol_match = re.search(r'volume[:\s]+([\d.]+)\s*(ft3|ft\^3|cubic)', text, re.IGNORECASE)
    if vol_match:
        params['volume'] = float(vol_match.group(1))
    
    press_match = re.search(r'pressure[:\s]+([\d.]+)\s*(psia|psi)', text, re.IGNORECASE)
    if press_match:
        params['pressure'] = float(press_match.group(1))
    
    area_match = re.search(r'area[:\s]+([\d.]+)\s*(ft2|ft\^2)', text, re.IGNORECASE)
    if area_match:
        params['area'] = float(area_match.group(1))
    
    return params

def main():
    print("=" * 60)
    print("AutoSAM: RAG-based SAM Input Generation Demo")
    print("=" * 60)
    
    store = DocumentStore()
    print("\n📚 Document Store contains:")
    for doc in store.documents:
        print(f"  - {doc}")
    
    queries = [
        ("reactor coolant pump", "pump"),
        ("pressurizer", "volume"),
        ("steam generator", "heat_structure")
    ]
    
    generator = SAMInputGenerator()
    
    print("\n🔍 Searching documents and extracting parameters...")
    for query, comp_type in queries:
        results = store.search(query)
        if results:
            print(f"\n  Found {comp_type} in: {results[0].split(']')[0][1:]}")
            params = extract_parameters(results[0])
            if params:
                comp = Component(
                    name=f"{comp_type.upper()}_{len(generator.components)+1}",
                    type=comp_type,
                    parameters=params
                )
                generator.add_component(comp)
                print(f"    Extracted: {params}")
            else:
                print(f"    Warning: No parameters found")
    
    print(f"\n📦 Total components extracted: {len(generator.components)}")
    
    sam_input = generator.generate_input_file()
    
    print("\n" + "=" * 60)
    print("GENERATED SAM INPUT FILE:")
    print("=" * 60)
    print(sam_input)
    
    output_file = "auto_sam_input.i"
    with open(output_file, 'w') as f:
        f.write(sam_input)
    print(f"\n💾 Saved to: {output_file}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("Next steps in full AutoSAM:")
    print("  - Multi-modal extraction from P&ID images (OCR + diagram parsing)")
    print("  - Cross-document constraint resolution")
    print("  - SAM syntax validation")
    print("  - Integration with NUREG/CR-xxxx specifications")

if __name__ == "__main__":
    main()
```