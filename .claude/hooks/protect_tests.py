#!/usr/bin/env python3
"""PreToolUse hook: Claude may not edit the ORIGINAL test files.

Claude Code sends the tool call as JSON on standard input. Exit code 2 blocks the call,
and what we write to stderr goes back to Claude as feedback.
"""
import json
import sys

PROTECTED = {"test_money.py", "test_rates.py", "test_receipt.py", "test_cli.py"}

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # not our business

path = ((data.get("tool_input") or {}).get("file_path") or "").replace("\\", "/")
name = path.rsplit("/", 1)[-1]

if "/tests/" in path and name in PROTECTED:
    print(
        f"Blocked: {name} is an original test file. Fix the code, not the test. "
        "New tests go into a NEW file, for example tests/test_my_feature.py.",
        file=sys.stderr,
    )
    sys.exit(2)

sys.exit(0)
