import contextlib
import io
import os
import unittest

from pfand.cli import main

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


def run(args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = main(args)
    return code, out.getvalue()


class CliTest(unittest.TestCase):
    def test_raten_lists_every_kind(self):
        code, text = run(["raten"])
        self.assertEqual(code, 0)
        self.assertIn("Einweg (Dose/PET)", text)
        self.assertIn("3,10 €", text)

    def test_refund_prints_the_sum(self):
        code, text = run(["refund", os.path.join(DATA, "bon_party.csv")])
        self.assertEqual(code, 0)
        self.assertIn("Summe: 11,44 €", text)


if __name__ == "__main__":
    unittest.main()
