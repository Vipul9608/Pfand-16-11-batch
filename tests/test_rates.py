import unittest

from pfand.rates import rate_for


class RateForTest(unittest.TestCase):
    def test_known_kind(self):
        self.assertEqual(rate_for("einweg"), 25)

    def test_capital_letters_and_spaces_do_not_matter(self):
        self.assertEqual(rate_for("  Einweg "), 25)

    def test_unknown_kind_is_an_error(self):
        with self.assertRaises(ValueError):
            rate_for("glasschrank")


if __name__ == "__main__":
    unittest.main()
