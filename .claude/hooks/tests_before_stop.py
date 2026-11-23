#!/usr/bin/env python3
"""Stop hook: Claude may not finish while the tests are red.

Exit code 2 sends our message to Claude, and Claude keeps working.
We check stop_hook_active, so that we never block in an endless loop.
"""
import json
import os
import subprocess
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

if data.get("stop_hook_active"):
    sys.exit(0)

os.chdir(os.environ.get("CLAUDE_PROJECT_DIR", "."))
result = subprocess.run([sys.executable, "-m", "unittest", "-q"], capture_output=True, text=True)

if result.returncode != 0:
    report = (result.stderr or result.stdout)[-1500:]
    print("The tests are not green yet. Fix the code, then finish.\n" + report, file=sys.stderr)
    sys.exit(2)

sys.exit(0)
