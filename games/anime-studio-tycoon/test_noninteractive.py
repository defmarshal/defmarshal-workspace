#!/usr/bin/env python3
import subprocess
import sys

# Simulate the game with auto-choices (non-interactive)
# We'll pipe in choices to trigger auto-mode
test_input = "\n".join([
    "",  # Week 0 - force auto-choice
    "",  # Week 1 - auto
    "",  # Week 2 - auto
    "",  # Week 3 - auto (event occurs)
    "",  # Week 4 - auto (upgrades view)
    "",  # Week 5 - auto
    "",  # Week 6 - auto (episode complete)
    "",  # Week 7 - auto
    "",  # Week 8 - auto
    "",  # Week 9 - auto
]) + "\n"

# Run the game and capture output
result = subprocess.run(
    ["python3", "main.py"],
    input=test_input,
    capture_output=True,
    text=True,
    timeout=30
)

print("=== STDOUT ===")
print(result.stdout)
print("\n=== STDERR ===")
print(result.stderr)
print(f"\nReturn code: {result.returncode}")

# Save log for report
with open("test-output.txt", "w") as f:
    f.write(result.stdout)
    f.write(result.stderr)

sys.exit(result.returncode)
