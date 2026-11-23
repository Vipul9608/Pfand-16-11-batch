# Pfand-Profi

Python CLI that calculates the Pfand (bottle deposit) refund from German CSV lists.
Standard library only. Entry point: `python3 -m pfand` (see `pfand/cli.py`).

## Commands
- Run tests: `python3 -m unittest`
- Check a mission: `python3 scripts/check.py m1` (m1 ... m6, or all)

## Rules
- Money is always a whole number of cents (int). Never use float for money.
- Show money in German format via `format_eur`: `1.234,50 €`. Read it with `parse_eur`.
- CSV files use `;`, German numbers, and UTF-8 with BOM (`encoding="utf-8-sig"`).
- Never edit the original tests (test_money, test_rates, test_receipt, test_cli): fix the code.
- New features go in a new module with a new test file, and a CLI subcommand in `cli.py`.
- Every bug fix needs a new test.
- Commit messages: imperative, one line.
