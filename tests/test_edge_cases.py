"""Edge cases found in the mission 5 review of money.py and receipt.py."""
import unittest

from pfand.money import format_eur, parse_eur
from pfand.receipt import refund


class NegativeMoneyTest(unittest.TestCase):
    def test_format_negative_cents(self):
        self.assertEqual(format_eur(-125), "-1,25 €")

    def test_format_small_negative_cents(self):
        self.assertEqual(format_eur(-5), "-0,05 €")

    def test_format_negative_thousands(self):
        self.assertEqual(format_eur(-123450), "-1.234,50 €")

    def test_parse_negative_amount(self):
        self.assertEqual(parse_eur("-1,50 €"), -150)

    def test_parse_negative_below_one_euro(self):
        self.assertEqual(parse_eur("-0,50"), -50)


class InvalidMoneyTest(unittest.TestCase):
    def test_format_rejects_float(self):
        with self.assertRaises(TypeError):
            format_eur(1.5)

    def test_parse_rejects_three_cent_digits(self):
        with self.assertRaises(ValueError):
            parse_eur("1,234")

    def test_parse_rejects_two_commas(self):
        with self.assertRaises(ValueError):
            parse_eur("1,2,3")

    def test_parse_rejects_empty_text(self):
        with self.assertRaises(ValueError):
            parse_eur(" € ")


class RefundCountTest(unittest.TestCase):
    def test_negative_count_is_an_error(self):
        with self.assertRaises(ValueError):
            refund([("einweg", -1)])

    def test_zero_count_is_allowed(self):
        self.assertEqual(refund([("einweg", 0)]), 0)


if __name__ == "__main__":
    unittest.main()
