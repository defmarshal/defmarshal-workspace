```python
#!/usr/bin/env python3
"""
Session Risk Memory (SRM): Temporal Authorization for Deterministic Pre-Execution Safety Gates
Demonstrates cumulative risk tracking for agent action authorization.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set
from datetime import datetime, timedelta

@dataclass
class Action:
    """Represents an action an agent might attempt."""
    name: str
    action_type: str
    risk_score: float  # 0.0 (safe) to 1.0 (high risk)
    required_role: str

@dataclass
class Role:
    """Defines an agent role with permissions and risk tolerance."""
    name: str
    allowed_action_types: Set[str]
    max_cumulative_risk: float  # Threshold for session risk
    max_risk_per_action: float   # Individual action risk limit

class SessionRiskMemory:
    """Tracks risk accumulation over a session for temporal authorization."""
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size  # Number of recent actions to track
        self.action_history: List[Action] = []
        self.cumulative_risk: float = 0.0
        self.session_start: datetime = datetime.now()
    
    def record_action(self, action: Action) -> None:
        """Record an executed action and update cumulative risk."""
        self.action_history.append(action)
        self.cumulative_risk += action.risk_score
        
        # Maintain sliding window
        if len(self.action_history) > self.window_size:
            removed = self.action_history.pop(0)
            self.cumulative_risk -= removed.risk_score
    
    def get_cumulative_risk(self) -> float:
        """Return cumulative risk over the session window."""
        return round(self.cumulative_risk, 3)
    
    def get_recent_actions(self) -> List[Action]:
        """Return recent actions within the window."""
        return self.action_history.copy()
    
    def reset(self) -> None:
        """Clear session memory."""
        self.action_history.clear()
        self.cumulative_risk = 0.0
        self.session_start = datetime.now()

class SafetyGate:
    """Deterministic pre-execution safety gate with SRM."""
    
    def __init__(self, role: Role):
        self.role = role
        self.srm = SessionRiskMemory()
    
    def authorize(self, action: Action) -> Dict:
        """Check if action is authorized based on role and cumulative risk."""
        result = {
            "action": action.name,
            "authorized": False,
            "reason": "",
            "cumulative_risk_before": self.srm.get_cumulative_risk()
        }
        
        # 1. Role-based check: Is this action type allowed for this role?
        if action.action_type not in self.role.allowed_action_types:
            result["reason"] = f"Action type '{action.action_type}' not permitted for role '{self.role.name}'"
            return result
        
        # 2. Individual risk check: Is this single action too risky?
        if action.risk_score > self.role.max_risk_per_action:
            result["reason"] = f"Action risk {action.risk_score:.2f} exceeds per-action limit {self.role.max_risk_per_action:.2f}"
            return result
        
        # 3. SRM temporal check: Would this push cumulative risk over threshold?
        projected_cumulative = self.srm.get_cumulative_risk() + action.risk_score
        if projected_cumulative > self.role.max_cumulative_risk:
            result["reason"] = f"Projected cumulative risk {projected_cumulative:.3f} would exceed session limit {self.role.max_cumulative_risk:.3f}"
            return result
        
        # All checks passed
        result["authorized"] = True
        result["reason"] = "Authorized"
        result["cumulative_risk_after"] = projected_cumulative
        return result
    
    def execute_action(self, action: Action) -> Dict:
        """Attempt to execute an action through the safety gate."""
        auth = self.authorize(action)
        if auth["authorized"]:
            self.srm.record_action(action)
            auth["status"] = "EXECUTED"
        else:
            auth["status"] = "BLOCKED"
        return auth

def demonstrate_srm() -> None:
    """Demonstrate SRM with example roles and actions."""
    print("=" * 70)
    print("SESSION RISK MEMORY (SRM) DEMONSTRATION")
    print("Temporal authorization for deterministic safety gates")
    print("=" * 70)
    
    # Define roles
    analyst_role = Role(
        name="data_analyst",
        allowed_action_types={"read", "query", "export_summary"},
        max_cumulative_risk=0.5,
        max_risk_per_action=0.2
    )
    
    admin_role = Role(
        name="system_admin",
        allowed_action_types={"read", "query", "export_full", "delete", "modify_config"},
        max_cumulative_risk=1.0,
        max_risk_per_action=0.4
    )
    
    # Define actions
    actions = [
        Action("read_user_data", "read", 0.05, "data_analyst"),
        Action("query_sensitive_logs", "query", 0.15, "data_analyst"),
        Action("export_full_database", "export_full", 0.5, "data_analyst"),  # Not even allowed type
        Action("export_summary_report", "export_summary", 0.1, "data_analyst"),
        Action("delete_log_file", "delete", 0.3, "data_analyst"),  # Allowed? No, type mismatch
        Action("modify_system_config", "modify_config", 0.35, "system_admin"),
        Action("run_diagnostic", "query", 0.08, "system_admin"),
    ]
    
    print("\n📋 ROLES:")
    for role in [analyst_role, admin_role]:
        print(f"\n  {role.name}:")
        print(f"    Allowed actions: {', '.join(sorted(role.allowed_action_types))}")
        print(f"    Max cumulative risk: {role.max_cumulative_risk}")
        print(f"    Max per-action risk: {role.max_risk_per_action}")
    
    print("\n🎯 SIMULATING SESSION FOR DATA_ANALYST:")
    print("-" * 70)
    
    gate = SafetyGate(analyst_role)
    
    for action in actions:
        if action.required_role != "data_analyst":
            continue  # Skip admin actions for this demo
        
        result = gate.execute_action(action)
        status_icon = "✅" if result["authorized"] else "🚫"
        print(f"{status_icon} {action.name:25} (risk={action.risk_score:.2f})")
        print(f"   Cumulative before: {result['cumulative_risk_before']:.3f}", end="")
        if result["authorized"]:
            print(f" → after: {result['cumulative_risk_after']:.3f}")
        else:
            print(f" → BLOCKED: {result['reason']}")
    
    print("\n📊 FINAL SESSION STATE:")
    print(f"  Total actions attempted: {len([a for a in actions if a.required_role == 'data_analyst'])}")
    print(f"  Cumulative risk: {gate.srm.get_cumulative_risk():.3f}")
    print(f"  Session duration: {datetime.now() - gate.srm.session_start}")
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT:")
    print("SRM prevents 'death by a thousand cuts'—many small-risk actions")
    print("accumulating to dangerous levels. Without temporal memory, each")
    print("action looks safe in isolation, but session-level risk goes unnoticed.")
    print("=" * 70)

def main():
    """Run SRM demonstration."""
    print("🧠 Session Risk Memory (SRM): Temporal Authorization Demo\n")
    demonstrate_srm()

if __name__ == "__main__":
    main()
```