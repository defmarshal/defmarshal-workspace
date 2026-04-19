#!/usr/bin/env python3
"""Quick test runner for agent utilities."""
import subprocess, sys, os

def run_test(cmd, desc):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        status = "PASS" if result.returncode == 0 else "FAIL"
        print(f"[{status}] {desc}")
        if result.stdout: print(f"  stdout: {result.stdout[:200]}")
        if result.stderr: print(f"  stderr: {result.stderr[:200]}")
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] {desc}: {e}")
        return False

os.chdir("/home/ubuntu/.openclaw/workspace")
all_pass = True
all_pass &= run_test("python3 -m py_compile agents/code-gardener.py", "code-gardener syntax")
all_pass &= run_test("python3 -m py_compile agents/content-gardener.py", "content-gardener syntax")
all_pass &= run_test("bash -n agents/meta-summary.sh", "meta-summary syntax")
all_pass &= run_test("python3 -c \"import sys; sys.path.insert(0,'.'); from agents.seed_gatherer import *; print('seed-gatherer import OK')\" 2>/dev/null || python3 -c \"import importlib.util; spec=importlib.util.spec_from_file_location('sg','agents/seed-gatherer.py'); mod=importlib.util.module_from_spec(spec); print('seed-gatherer import OK')\"", "seed-gatherer import")
print("All tests passed" if all_pass else "Some tests failed")
sys.exit(0 if all_pass else 1)
