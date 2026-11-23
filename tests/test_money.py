import unittest

from pfand.money import format_eur, parse_eur


class FormatEurTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(format_eur(125), "1,25 €")

    def test_zero(self):
        self.assertEqual(format_eur(0), "0,00 €")

    def test_thousands_use_a_dot(self):
        self.assertEqual(format_eur(1234567), "12.345,67 €")


class ParseEurTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(parse_eur("1,25 €"), 125)

    def test_whole_euros(self):
        self.assertEqual(parse_eur("12"), 1200)

    def test_one_digit_after_the_comma(self):
        self.assertEqual(parse_eur("0,5"), 50)

    def test_thousands_dot(self):
        self.assertEqual(parse_eur("1.234,50 €"), 123450)


if __name__ == "__main__":
    unittest.main()
