# Mission 1: First contact

Ask Claude three questions about the project. Then write the answers here, in your own words,
one sentence each. Do not copy Claude's text.

A1: What does this project do? It reads German bottle lists from CSV files and tells me how much Pfand money I get back, in cents shown as euros.
A2: Where does the program start? In pfand/__main__.py, which calls main() in pfand/cli.py, and argparse sends each subcommand (raten, refund, bon, teilen) to its own function.
A3: How do I run the tests, and how many tests are there? With python3 -m unittest; the starter had 15 tests (4 failing on purpose), and now there are 41, all green.
