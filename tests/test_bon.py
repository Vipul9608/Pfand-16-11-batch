import contextlib
import io
import os
import unittest

from pfand.bon import WIDTH, format_bon
from pfand.cli import main

DATA = os.path.join(os.path.dirname(__file__), "..", "data")

# The title line ends in spaces (it is 32 wide), so it is written with explicit padding.
TITLE = " " * 11 + "PFAND-BON" + " " * 12

PARTY_BON = """\
================================
""" + TITLE + """
================================
24 x Einweg (Dose/PET)    6,00 €
18 x Mehrweg Bier         1,44 €
 6 x Mehrweg Wasser       0,90 €
 1 x Kasten Bier          3,10 €
--------------------------------
Summe                    11,44 €
================================"""

PARTY_ITEMS = [("einweg", 24), ("mehrweg_bier", 18), ("mehrweg_wasser", 6), ("kasten_bier", 1)]


class FormatBonTest(unittest.TestCase):
    def test_party_list_matches_the_spec(self):
        self.assertEqual(format_bon(PARTY_ITEMS), PARTY_BON)

    def test_every_line_is_32_characters_wide(self):
        for line in format_bon(PARTY_ITEMS).splitlines():
            self.assertEqual(len(line), WIDTH, repr(line))

    def test_empty_list_does_not_crash(self):
        text = format_bon([])
        self.assertIn("Summe", text)
        self.assertIn("0,00 €", text)
        for line in text.splitlines():
            self.assertEqual(len(line), WIDTH, repr(line))

    def test_label_ignores_capital_letters(self):
        text = format_bon([("Einweg", 5)])
        self.assertIn("5 x Einweg (Dose/PET)", text)

    def test_cli_prints_the_bon(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(["bon", os.path.join(DATA, "bon_party.csv")])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().rstrip("\n"), PARTY_BON)


if __name__ == "__main__":
    unittest.main()
