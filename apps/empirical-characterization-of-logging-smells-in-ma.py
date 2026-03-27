```python
#!/usr/bin/env python3
"""
Detects common logging smells in machine learning code.
Based on: Empirical Characterization of Logging Smells in ML Code (arXiv:2603.23769v1)
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict

class LoggingSmellDetector(ast.NodeVisitor):
    """AST visitor to detect logging code smells."""
    
    def __init__(self):
        self.smells = []
        self.in_loop = False
        self.loop_depth = 0
    
    def visit_For(self, node):
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
    
    def visit_While(self, node):
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
    
    def visit_Call(self, node):
        # Check for print() usage instead of logging
        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            self.smells.append({
                'type': 'PrintInsteadOfLogging',
                'line': node.lineno,
                'msg': 'Uses print() instead of structured logging'
            })
        
        # Check for logging calls
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == 'logging':
                # Check for missing level specification
                if not node.args and not node.keywords:
                    self.smells.append({
                        'type': 'EmptyLogCall',
                        'line': node.lineno,
                        'msg': 'Empty logging call (no message or context)'
                    })
                
                # Check for logging inside tight loops
                if self.loop_depth > 0 and node.func.attr in ['debug', 'info', 'warning', 'error']:
                    self.smells.append({
                        'type': 'LoopLogging',
                        'line': node.lineno,
                        'msg': f'Logging inside loop (depth {self.loop_depth})'
                    })
        
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        # Detect hardcoded log paths
        if isinstance(node.value, ast.Str):
            if any(kw in node.value.s.lower() for kw in ['log', '/var/log', 'logs/', '.log']):
                self.smells.append({
                    'type': 'HardcodedLogPath',
                    'line': node.lineno,
                    'msg': f'Hardcoded log path: {node.value.s[:40]}...'
                })
        self.generic_visit(node)
    
    def visit_With(self, node):
        # Check for open() without rotation
        for item in node.items:
            if isinstance(item.context_expr, ast.Call):
                if isinstance(item.context_expr.func, ast.Name) and item.context_expr.func.id == 'open':
                    # Look for mode='a' or 'w' without rotation
                    mode = None
                    for kw in item.context_expr.keywords:
                        if kw.arg == 'mode':
                            if isinstance(kw.value, ast.Str):
                                mode = kw.value.s
                    if mode and mode.startswith('a'):
                        self.smells.append({
                            'type': 'UnboundedLogAppend',
                            'line': node.lineno,
                            'msg': 'Appending to log file without rotation consideration'
                        })
        self.generic_visit(node)

def detect_smells(code: str) -> List[Dict]:
    """Parse code and detect logging smells."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [{'type': 'SyntaxError', 'line': e.lineno, 'msg': str(e)}]
    
    detector = LoggingSmellDetector()
    detector.visit(tree)
    return detector.smells

def sample_ml_code() -> str:
    """Sample ML code with introduced logging smells for demonstration."""
    return '''
import logging
import time
from pathlib import Path

# Smell 1: Hardcoded log path
LOG_FILE = "/var/log/ml_training.log"

def train_model(data, epochs=10):
    # Smell 2: Using print instead of logging
    print("Starting training...")
    
    # Smell 3: Empty log call (no args)
    logging.info()
    
    # Smell 4: Logging inside a tight loop
    for epoch in range(epochs):
        loss = 0.5  # dummy
        logging.debug(f"Epoch {epoch}, loss={loss}")  # Could flood logs
        
        # Smell 5: Unbounded log append
        with open(LOG_FILE, 'a') as f:
            f.write(f"Epoch {epoch}\\n")
            
    print("Training complete")

def evaluate(model):
    try:
        result = model.predict()
    except:
        # Smell 6: Bare except without logging
        pass
    logging.warning("Evaluation done")  # Missing context

if __name__ == "__main__":
    train_model(None)
'''

def main():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"File not found: {path}")
            sys.exit(1)
        code = path.read_text()
        print(f"Analyzing: {path}")
    else:
        code = sample_ml_code()
        print("Analyzing sample ML code with logging smells...")
    
    smells = detect_smells(code)
    
    print(f"\nFound {len(smells)} logging smell(s):")
    print("-" * 50)
    
    by_type = {}
    for smell in smells:
        by_type.setdefault(smell['type'], []).append(smell)
    
    for smell_type, instances in sorted(by_type.items()):
        print(f"\n{smell_type} ({len(instances)} occurrence(s)):")
        for inst in instances:
            print(f"  Line {inst['line']}: {inst['msg']}")
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    total = len(smells)
    if total == 0:
        print("✓ No logging smells detected!")
    else:
        print(f"! {total} smell(s) require attention")
        print("Recommendations: use structured logging, avoid print(), rotate logs, include context.")

if __name__ == "__main__":
    main()
```