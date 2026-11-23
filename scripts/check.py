#!/usr/bin/env python3
"""check.py: checks your missions. Run it in the project folder:

    python scripts/check.py m1        (one mission: m1 ... m6)
    python scripts/check.py all

It only READS your project. It never changes anything.
(On a Mac you may need python3 instead of python.)
"""
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASS = FAIL = 0


def ok(text):
    global PASS
    PASS += 1
    print(f"  PASS  {text}")


def bad(text, hint=None):
    global FAIL
    FAIL += 1
    print(f"  FAIL  {text}")
    if hint:
        print(f"        hint: {hint}")


def info(text):
    print(f"  INFO  {text}")


def run(args, timeout=120):
    return subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)


def path(*parts):
    return os.path.join(ROOT, *parts)


def baseline():
    with open(path("scripts", "baseline.json"), encoding="utf-8") as f:
        return json.load(f)


def test_summary():
    """(number of tests, all green?)"""
    r = run(["-m", "unittest"])
    text = r.stderr + r.stdout
    m = re.search(r"Ran (\d+) test", text)
    return (int(m.group(1)) if m else 0), r.returncode == 0


def answers(filename, prefix, count):
    """How many lines A1:/B1:/C1: ... are really answered (not the template text)."""
    p = path("notes", filename)
    if not os.path.exists(p):
        return None
    done = 0
    with open(p, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for i in range(1, count + 1):
        for line in lines:
            if line.startswith(f"{prefix}{i}:"):
                text = line.split(":", 1)[1].strip()
                if "(write your answer here)" not in text and len(text) >= 8:
                    done += 1
    return done


def git(*args):
    try:
        return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, text=True, timeout=30)
    except Exception:
        return None


def m1():
    print("Mission 1: First contact")
    n = answers("mission1.md", "A", 3)
    if n is None:
        bad("notes/mission1.md is missing")
    elif n == 3:
        ok("you answered the three questions in your own words")
    else:
        bad(f"{n} of 3 answers are written in notes/mission1.md", "replace the text (write your answer here) with your own sentence")
    r = run(["-m", "pfand", "raten"])
    ok("python -m pfand raten works") if r.returncode == 0 else bad("python -m pfand raten does not work")


def m2():
    print("Mission 2: Fix it, with proof")
    base = baseline()
    changed = []
    for name, digest in base["hashes"].items():
        p = path(*name.split("/"))
        if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != digest:
            changed.append(name)
    if changed:
        bad("an original test file was changed: " + ", ".join(changed), "fix the code, not the test. (Run this check right after mission 2, before you add new tests to old files.)")
    else:
        ok("the original tests are untouched")
    n, green = test_summary()
    ok(f"all {n} tests pass") if green else bad("some tests still fail", "python -m unittest")
    r = run(["-m", "pfand", "refund", os.path.join("data", "bon_party.csv")])
    ok("python -m pfand refund data/bon_party.csv works") if r.returncode == 0 and "11,44" in r.stdout else bad("python -m pfand refund data/bon_party.csv does not print Summe: 11,44 €")


def m3():
    print("Mission 3: Plan it, build it, commit it")
    base = baseline()["baseline_tests"]
    n, green = test_summary()
    ok("all tests pass") if green else bad("some tests fail")
    ok(f"you added tests: {n - base} new") if n >= base + 3 else bad(f"you need at least 3 new tests (now {n - base})", "ask Claude to write the tests first")
    a = run(["-m", "pfand", "bon", os.path.join("data", "bon_party.csv")])
    e = run(["-m", "pfand", "teilen", os.path.join("data", "bon_party.csv"), "--wg", "Anna,Ben,Cem"])
    bon_ok = a.returncode == 0 and "11,44" in a.stdout
    wg_ok = e.returncode == 0 and "3,82" in e.stdout and e.stdout.count("3,81") >= 2
    if bon_ok or wg_ok:
        ok("your feature works: " + ("Pfandbon (A)" if bon_ok else "WG teilen (E)"))
    else:
        bad("no feature found: try python -m pfand bon data/bon_party.csv  (A) or teilen (E)", "see docs/FEATURES.md for the exact output")
    g = git("log", "--oneline")
    if g is None or g.returncode != 0:
        info("this folder is not a git repository: no commit check")
    else:
        count = len([l for l in g.stdout.splitlines() if l.strip()])
        ok(f"git log has {count} commits") if count >= 3 else bad(f"git log has {count} commits: you need at least 3 (start, fix, feature)")
        s = git("status", "--porcelain")
        ok("everything is committed") if s is not None and not s.stdout.strip() else bad("you have changes that are not committed")


def m4():
    print("Mission 4: Fuel and briefing")
    p = path("CLAUDE.md")
    if not os.path.exists(p):
        bad("CLAUDE.md does not exist", "run /init in Claude Code, then cut it down")
        return
    ok("CLAUDE.md exists")
    with open(p, encoding="utf-8") as f:
        text = f.read()
    lines = [l for l in text.splitlines() if l.strip()]
    ok(f"it is short: {len(lines)} lines") if 5 <= len(lines) <= 30 else bad(f"CLAUDE.md has {len(lines)} lines: aim for about 10 to 20", "which lines would you cut?")
    low = text.lower()
    ok("it says that money is in cents") if "cent" in low else bad("CLAUDE.md does not mention cents", "add the rule: money is a whole number of cents")
    ok("it says how to run the tests") if "unittest" in low else bad("CLAUDE.md does not say how to run the tests", "add: python -m unittest")


def m5():
    print("Mission 5: Second opinion")
    n = answers("mission5.md", "B", 3)
    if n is None:
        bad("notes/mission5.md is missing")
    elif n == 3:
        ok("you answered the three review questions")
    else:
        bad(f"{n} of 3 answers are written in notes/mission5.md")
    snippet = (
        "import json\n"
        "from pfand.money import format_eur, parse_eur\n"
        "from pfand.receipt import refund\n"
        "r = {}\n"
        "r['a'] = format_eur(-125) == '-1,25 €'\n"
        "try:\n    r['b'] = parse_eur('-1,50 €') == -150\nexcept Exception:\n    r['b'] = False\n"
        "try:\n    refund([('einweg', -1)]); r['c'] = False\nexcept ValueError:\n    r['c'] = True\nexcept Exception:\n    r['c'] = False\n"
        "print(json.dumps(r))\n"
    )
    r = run(["-c", snippet])
    try:
        res = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        res = {}
    fixed = sum(1 for v in res.values() if v)
    if fixed >= 2:
        ok(f"the review found real problems, and you fixed them ({fixed} of 3 edge cases)")
    else:
        bad(f"the code still has edge-case problems ({fixed} of 3 fixed)", "ask Claude to review money.py and receipt.py: what happens with negative numbers?")
    n, green = test_summary()
    ok("all tests pass") if green else bad("some tests fail")


def m6():
    print("Mission 6: Boss mission")
    base = baseline()["baseline_tests"]
    n = answers("mission6.md", "C", 4)
    if n is None:
        bad("notes/mission6.md is missing")
    elif n == 4:
        ok("you answered the four showcase questions")
    else:
        bad(f"{n} of 4 answers are written in notes/mission6.md")
    count, green = test_summary()
    ok("all tests pass") if green else bad("some tests fail")
    ok(f"you added {count - base} tests since the start") if count >= base + 6 else bad(f"you need at least 6 new tests in total (now {count - base})")
    settings = path(".claude", "settings.json")
    try:
        with open(settings, encoding="utf-8") as f:
            data = json.load(f)
        ok("the hooks are in .claude/settings.json") if "hooks" in data else bad(".claude/settings.json has no hooks")
    except FileNotFoundError:
        bad(".claude/settings.json is missing", "power-up: copy extras/hooks/settings.example.json (see the project document)")
    except ValueError:
        bad(".claude/settings.json is not valid JSON", "look for a comma or a quote")
    hooks_dir = path(".claude", "hooks")
    scripts = [f for f in os.listdir(hooks_dir) if f.endswith(".py")] if os.path.isdir(hooks_dir) else []
    ok(f"hook scripts found: {', '.join(sorted(scripts))}") if scripts else bad("no hook scripts in .claude/hooks/")
    claude_md = path("CLAUDE.md")
    ok("CLAUDE.md exists") if os.path.exists(claude_md) else bad("CLAUDE.md is missing")


MISSIONS = {"m1": m1, "m2": m2, "m3": m3, "m4": m4, "m5": m5, "m6": m6}


def main(argv):
    if len(argv) != 2 or argv[1] not in list(MISSIONS) + ["all"]:
        print("Usage: python scripts/check.py m1 | m2 | m3 | m4 | m5 | m6 | all")
        return 2
    todo = list(MISSIONS) if argv[1] == "all" else [argv[1]]
    for name in todo:
        MISSIONS[name]()
        print()
    if FAIL == 0:
        print(f"ALL CHECKS PASSED ({PASS}). Great flying, pilot.")
    else:
        print(f"{FAIL} check(s) need your attention, {PASS} passed. Read the hints, fix, and run the check again.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
