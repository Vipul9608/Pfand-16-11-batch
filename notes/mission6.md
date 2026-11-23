# Mission 6: Boss mission

C1: What did I ask Claude? (my best prompt) Build feature E from docs/FEATURES.md: write the tests first from the spec, including a test that the shares add up to the total for many totals and group sizes, then the code, then one commit.
C2: What did Claude do? It wrote tests/test_share.py first, then pfand/share.py with split_cents using divmod and parse_names, and added the teilen subcommand that prints a clear Fehler message for an empty --wg list.
C3: What did I check, and what was the proof? I ran python3 -m unittest (41 tests OK), ran python3 -m pfand teilen data/bon_party.csv --wg Anna,Ben,Cem and saw 3,82 / 3,81 / 3,81, and ran python3 scripts/check.py all.
C4: My one new line in CLAUDE.md: Splitting money must add up to the total exactly: use divmod and hand out the rest cents, never round.
