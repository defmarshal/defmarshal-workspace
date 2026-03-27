```python
#!/usr/bin/env python3
"""
Demonstrates generating penetration test cases from software architecture using LLMs.
Based on: arXiv:2603.23698v1 "Towards Leveraging LLMs to Generate Abstract Penetration Test Cases from Software Architecture"
"""

from typing import List, Dict
import json

# Example architecture: Component-Connector model
ARCHITECTURE = {
    "systems": ["E-Commerce Platform"],
    "components": [
        {"id": "C1", "name": "Web UI", "type": "Presentation", "exposed": True},
        {"id": "C2", "name": "API Gateway", "type": "Integration", "exposed": True},
        {"id": "C3", "name": "Order Service", "type": "Business", "exposed": False},
        {"id": "C4", "name": "Payment Service", "type": "Business", "exposed": False},
        {"id": "C5", "name": "User DB", "type": "Persistence", "exposed": False},
        {"id": "C6", "name": "Order DB", "type": "Persistence", "exposed": False}
    ],
    "connections": [
        {"source": "C1", "target": "C2", "protocol": "HTTPS", "data": "user_input"},
        {"source": "C2", "target": "C3", "protocol": "REST/JSON", "data": "order_request"},
        {"source": "C2", "target": "C4", "protocol": "REST/JSON", "data": "payment_info"},
        {"source": "C3", "target": "C5", "protocol": "SQL", "data": "user_lookup"},
        {"source": "C3", "target": "C6", "protocol": "SQL", "data": "order_data"},
        {"source": "C4", "target": "C6", "protocol": "SQL", "data": "payment_record"}
    ]
}

def query_llm(architecture: Dict) -> List[Dict]:
    """Simulate LLM generating penetration test cases from architecture."""
    exposed_components = [c for c in architecture["components"] if c["exposed"]]
    data_flows = [(conn["source"], conn["target"], conn["data"]) 
                  for conn in architecture["connections"]]
    
    test_cases = []
    
    # 1. Injection: flows with user-controlled data
    for src, tgt, data in data_flows:
        if "input" in data.lower() or "request" in data.lower():
            test_cases.append({
                "type": "Injection",
                "title": f"{data.title()} Injection",
                "target": f"{src} → {tgt}",
                "description": f"Inject malicious {data} via {src} to exploit {tgt}",
                "severity": "High"
            })
    
    # 2. Authentication: exposed entry points
    for comp in exposed_components:
        if any(conn["source"] == comp["id"] and any(p in conn["protocol"] for p in ["REST", "HTTPS"]):
            test_cases.append({
                "type": "Broken Authentication",
                "title": f"Authentication Bypass on {comp['name']}",
                "target": comp["name"],
                "description": "Test weak session management, token validation, or privilege escalation",
                "severity": "Critical"
            })
    
    # 3. Data exposure: sensitive data flows
    sensitive = ["payment", "credit", "card", "personal", "pii"]
    for src, tgt, data in data_flows:
        if any(kw in data.lower() for kw in sensitive):
            test_cases.append({
                "type": "Data Exposure",
                "title": f"{data.title()} Exposure",
                "target": f"{src} → {tgt}",
                "description": f"Verify {data} encryption in transit/at rest and proper access controls",
                "severity": "High"
            })
    
    return test_cases

def main():
    print("Penetration Test Case Generation from Architecture")
    print("=" * 55)
    print("\nArchitecture Model:")
    print(json.dumps(ARCHITECTURE, indent=2))
    
    tests = query_llm(ARCHITECTURE)
    print(f"\nGenerated {len(tests)} Test Cases:")
    for i, test in enumerate(tests, 1):
        print(f"\n{i}. [{test['severity']}] {test['title']}")
        print(f"   Target: {test['target']}")
        print(f"   Description: {test['description']}")
    
    output = {
        "architecture": ARCHITECTURE,
        "test_cases": tests,
        "metadata": {"source": "LLM simulation", "count": len(tests)}
    }
    with open("pen_test_cases.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nSaved to pen_test_cases.json")

if __name__ == "__main__":
    main()
```