```python
#!/usr/bin/env python3
"""SpaceTime Programming Demo: Live code + execution exploration

Based on arXiv:2603.18735v1 - unifies static code structure with dynamic execution.
"""

import ast
import sys
import traceback
from typing import Any, Dict

class SpaceTimeExplorer:
    """Fuses static AST analysis with runtime execution tracking."""
    
    def __init__(self, code: str):
        self.code = code
        self.ast_tree = ast.parse(code)
        self.exec_globals = {}
        self.exec_locals = {}
        self.execution_log = []
        
    def analyze_static(self) -> Dict[str, Any]:
        """Extract static structure: functions, vars, calls."""
        info = {"functions": [], "variables": [], "calls": []}
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                info["functions"].append({
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "lineno": node.lineno
                })
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        info["variables"].append(target.id)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    info["calls"].append(node.func.id)
        return info
    
    def execute_with_tracing(self):
        """Run code while capturing variable state changes."""
        # Tracer to log assignments and function calls
        def trace_lines(frame, event, arg):
            if event == 'line':
                code_line = frame.f_code.co_filename
                if frame.f_code.co_name == '<module>':
                    # Capture local variable snapshot
                    snapshot = dict(frame.f_locals)
                    self.execution_log.append({
                        'type': 'line',
                        'line_no': frame.f_lineno,
                        'variables': snapshot
                    })
            return trace_lines
        
        sys.settrace(trace_lines)
        try:
            exec(self.code, self.exec_globals, self.exec_locals)
        finally:
            sys.settrace(None)
    
    def show_spacetime_view(self):
        """Display unified static + dynamic view."""
        print("=== SPACETIME PROGRAMMING VIEW ===\n")
        
        print("STATIC CODE STRUCTURE:")
        static = self.analyze_static()
        print(f"  Functions: {[f['name'] for f in static['functions']]}")
        print(f"  Variables: {static['variables']}")
        print(f"  Function calls: {static['calls']}")
        
        print("\nDYNAMIC EXECUTION TRACE:")
        if not self.execution_log:
            print("  (No traced steps)")
        else:
            for i, step in enumerate(self.execution_log[:10]):  # limit output
                print(f"  Line {step['line_no']}: {step['variables']}")
        
        print("\nFINAL STATE:")
        print(f"  Global vars: {list(self.exec_globals.keys())}")
        print(f"  Local vars: {list(self.exec_locals.keys())}")
        if 'result' in self.exec_locals:
            print(f"  Result value: {self.exec_locals['result']}")

def main():
    # Sample code to explore - mixes computation and state changes
    sample_code = """
x = 5
y = 10

def add(a, b):
    return a + b

result = add(x, y)
z = result * 2
"""
    
    print("SpaceTime Programming Explorer")
    print("Analyzing code + execution in unified view...\n")
    print("CODE:")
    print(sample_code)
    print("\n")
    
    explorer = SpaceTimeExplorer(sample_code)
    
    # Static analysis only
    static = explorer.analyze_static()
    print("Static analysis detected:")
    print(f"  Functions: {[f['name'] for f in static['functions']]}")
    print(f"  Variables: {static['variables']}")
    
    # Execute with tracing
    print("\nExecuting with runtime tracing...")
    explorer.execute_with_tracing()
    
    # Show combined spacetime view
    explorer.show_spacetime_view()
    
    print("\n=== CONCEPT DEMONSTRATION ===")
    print("Developers can see both code structure (static) and")
    print("execution state (dynamic) in one unified view.")
    print("This bridges the gap between 'reading code' and 'running code'.")

if __name__ == "__main__":
    main()
```