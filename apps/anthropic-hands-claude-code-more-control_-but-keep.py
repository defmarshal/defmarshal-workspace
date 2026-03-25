```python
#!/usr/bin/env python3
"""
Claude Code Auto Mode Simulator
Demonstrates balanced autonomy: speed with safety checks.
"""

import time
from enum import Enum
from typing import List, Callable

class RiskLevel(Enum):
    SAFE = "safe"          # Read-only, no side effects
    LOW = "low"            # Minor changes, reversible
    MEDIUM = "medium"      # Affects external systems
    HIGH = "high"          # Destructive or irreversible

class Task:
    def __init__(self, name: str, risk: RiskLevel, action: Callable):
        self.name = name
        self.risk = risk
        self.action = action
        self.approved = False
        self.executed = False

class SafetyController:
    """The 'leash' - decides what needs human approval vs auto-execute."""
    
    def __init__(self, auto_mode: bool = False):
        self.auto_mode = auto_mode
        self.approved_tasks = set()
        self.blocked_tasks = set()
    
    def can_execute(self, task: Task) -> bool:
        """Check if task can run based on mode and risk level."""
        if task.name in self.blocked_tasks:
            return False
            
        if self.auto_mode:
            # Auto mode: safe/low tasks auto-approved, medium+ need approval
            if task.risk in (RiskLevel.SAFE, RiskLevel.LOW):
                return True
            else:
                return task.approved
        else:
            # Manual mode: everything needs approval
            return task.approved
    
    def request_approval(self, task: Task) -> bool:
        """Simulate human approval process."""
        print(f"⚠️  Approval needed: {task.name} (risk: {task.risk.value})")
        print("   Analyzing impact...")
        time.sleep(0.5)  # Simulate review time
        # Simulate: 80% approval rate for medium, 50% for high
        import random
        if task.risk == RiskLevel.MEDIUM:
            approved = random.random() < 0.8
        elif task.risk == RiskLevel.HIGH:
            approved = random.random() < 0.5
        else:
            approved = True
            
        if approved:
            print(f"   ✓ Approved by human operator")
            task.approved = True
            self.approved_tasks.add(task.name)
        else:
            print(f"   ✗ Rejected by human operator")
            self.blocked_tasks.add(task.name)
        return approved

class ClaudeCodeAuto:
    """Simulates Claude Code with auto mode toggle."""
    
    def __init__(self, controller: SafetyController):
        self.controller = controller
        self.execution_log = []
    
    def execute_task(self, task: Task) -> bool:
        """Execute a task with safety checks."""
        if not self.controller.can_execute(task):
            if not task.approved and task.name not in self.controller.blocked_tasks:
                self.controller.request_approval(task)
            
            if not self.controller.can_execute(task):
                print(f"❌ Task '{task.name}' blocked or rejected")
                self.execution_log.append((task.name, "BLOCKED"))
                return False
        
        # Execute with simulated time cost
        print(f"▶️  Executing: {task.name}...")
        start = time.time()
        try:
            task.action()
            elapsed = time.time() - start
            print(f"   ✅ Completed in {elapsed:.2f}s")
            task.executed = True
            self.execution_log.append((task.name, "SUCCESS"))
            return True
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            self.execution_log.append((task.name, f"ERROR: {e}"))
            return False

def make_dummy_action(duration: float = 0.3):
    """Create a dummy task action that sleeps."""
    def action():
        time.sleep(duration)
    return action

def main():
    print("=" * 60)
    print("Anthropic Claude Code: Auto Mode vs Manual Mode")
    print("Balancing autonomy with safety via built-in leash mechanisms")
    print("=" * 60)
    print()
    
    # Define a set of tasks with varying risk levels
    tasks = [
        Task("list_files", RiskLevel.SAFE, make_dummy_action(0.2)),
        Task("read_config", RiskLevel.SAFE, make_dummy_action(0.3)),
        Task("write_log", RiskLevel.LOW, make_dummy_action(0.4)),
        Task("update_cache", RiskLevel.LOW, make_dummy_action(0.5)),
        Task("restart_service", RiskLevel.MEDIUM, make_dummy_action(0.8)),
        Task("deploy_config", RiskLevel.MEDIUM, make_dummy_action(1.0)),
        Task("delete_old_logs", RiskLevel.MEDIUM, make_dummy_action(0.7)),
        Task("database_migration", RiskLevel.HIGH, make_dummy_action(1.5)),
        Task("rotate_secrets", RiskLevel.HIGH, make_dummy_action(2.0)),
        Task("emergency_shutdown", RiskLevel.HIGH, make_dummy_action(0.5)),
    ]
    
    print("SCENARIO 1: Manual Mode (Everything needs approval)")
    print("-" * 60)
    manual_controller = SafetyController(auto_mode=False)
    manual_claude = ClaudeCodeAuto(manual_controller)
    
    manual_success = 0
    for task in tasks:
        if manual_claude.execute_task(task):
            manual_success += 1
        print()
    
    print(f"Manual mode: {manual_success}/{len(tasks)} tasks completed")
    print(f"Approvals required: {len(manual_controller.approved_tasks)}")
    print()
    
    print("SCENARIO 2: Auto Mode (Safe/Low auto, Medium/High need approval)")
    print("-" * 60)
    auto_controller = SafetyController(auto_mode=True)
    auto_claude = ClaudeCodeAuto(auto_controller)
    
    auto_success = 0
    for task in tasks:
        if auto_claude.execute_task(task):
            auto_success += 1
        print()
    
    print(f"Auto mode: {auto_success}/{len(tasks)} tasks completed")
    print(f"Auto-executed (no approval): {sum(1 for t in tasks if t.risk in (RiskLevel.SAFE, RiskLevel.LOW) and t.executed)}")
    print(f"Required approval + executed: {len(auto_controller.approved_tasks)}")
    print(f"Blocked/rejected: {len(auto_controller.blocked_tasks)}")
    print()
    
    # Summary comparison
    print("=" * 60)
    print("SUMMARY: Auto Mode Wins on Speed, Keeps Safety")
    print("-" * 60)
    print(f"Time saved (estimated): ~{(manual_success - auto_success) * 0.5:.1f}s per batch")
    print(f"Safety preserved: High-risk tasks still require human sign-off")
    print(f"Risk profile: {len([t for t in tasks if t.risk in (RiskLevel.MEDIUM, RiskLevel.HIGH) and t.executed])} medium/high tasks executed")
    print()
    print("KEY INSIGHT:")
    print("  Auto mode doesn't mean 'run everything'. It means:")
    print("  - Trust the AI with repetitive, low-risk work")
    print("  - Keep humans in the loop for consequential decisions")
    print("  - Adjustable leash: modify RiskLevel thresholds per deployment")
    print()
    print("This balances developer velocity with operational safety,")
    print("reflecting Anthropic's approach: more autonomy, but never")
    print("without guardrails.")
    print("=" * 60)

if __name__ == "__main__":
    main()
```