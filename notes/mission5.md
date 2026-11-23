# Mission 5: Second opinion

Run /code-review on your changes. Read every finding. Treat the findings as questions, not orders.

B1: One finding that was real: format_eur(-125) printed -2,75 € because divmod rounds toward minus infinity, so negative amounts were wrong by almost a euro.
B2: One finding that was noise, and why: a suspected bug that blank lines in the CSV would crash read_bon turned out to be noise, because csv.DictReader already skips empty rows.
B3: What I changed because of the review: negative money now formats and parses correctly, parse_eur rejects texts like 1,234 or 1,2,3, format_eur rejects floats, and refund rejects negative counts, with 11 new tests.
