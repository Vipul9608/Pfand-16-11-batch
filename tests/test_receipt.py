import os
import unittest

from pfand.receipt import read_bon, refund

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


class RefundTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(refund([("einweg", 4)]), 100)

    def test_empty_list(self):
        self.assertEqual(refund([]), 0)


class ReadBonTest(unittest.TestCase):
    def test_reads_the_party_list(self):
        items = read_bon(os.path.join(DATA, "bon_party.csv"))
        self.assertEqual(items[0], ("einweg", 24))
        self.assertEqual(len(items), 4)


if __name__ == "__main__":
    unittest.main()
