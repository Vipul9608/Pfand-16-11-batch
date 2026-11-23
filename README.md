# Pfand-Profi

A small Python tool that calculates your **Pfand** (bottle deposit) refund. It reads lists of bottles from CSV files, the way Excel saves them in Germany: semicolons, German number format, UTF-8 with BOM.

You do not write this project alone. **Claude Code is your co-pilot.** The project document (PDF) has six missions: explore, fix, plan and build, manage the context, get a second opinion, and ship a feature.

## Start

    python -m unittest              # run the tests (on a Mac: python3)
    python -m pfand raten           # show the Pfand rates
    python -m pfand --help          # all commands

The tests do not all pass yet. That is on purpose: mission 2.

## Check your missions

    python scripts/check.py m1      # m1 ... m6, or: all

## Folders

| Folder | What is in it |
| :- | :- |
| `pfand/` | the code (standard library only, no packages to install) |
| `tests/` | the tests (unittest) |
| `data/` | example lists (CSV files) |
| `docs/FEATURES.md` | the feature menu for missions 3 and 6 |
| `notes/` | your answers for missions 1, 5 and 6 |
| `extras/hooks/` | the hooks for the power-up in mission 6 |
| `scripts/check.py` | the mission checker |

## Rules of this project

- Money is always a whole number of **cents**. Never use float for money.
- Money is shown in the German format: `1.234,50 €`.
- Never edit an existing test to make it pass: fix the code.
