import contextlib
import io
import os
import unittest

from pfand.cli import main
from pfand.share import parse_names, split_cents

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


class SplitCentsTest(unittest.TestCase):
    def test_spec_example(self):
        self.assertEqual(split_cents(1144, 3), [382, 381, 381])

    def test_even_split(self):
        self.assertEqual(split_cents(900, 3), [300, 300, 300])

    def test_one_person_gets_everything(self):
        self.assertEqual(split_cents(1144, 1), [1144])

    def test_more_people_than_cents(self):
        self.assertEqual(split_cents(2, 4), [1, 1, 0, 0])

    def test_shares_always_add_up_to_the_total(self):
        for total in list(range(0, 300)) + [1144, 99999, 123457]:
            for people in range(1, 12):
                with self.subTest(total=total, people=people):
                    shares = split_cents(total, people)
                    self.assertEqual(sum(shares), total)
                    self.assertEqual(len(shares), people)
                    self.assertLessEqual(max(shares) - min(shares), 1)
                    self.assertEqual(shares, sorted(shares, reverse=True))

    def test_no_people_is_an_error(self):
        with self.assertRaises(ValueError):
            split_cents(1144, 0)


class ParseNamesTest(unittest.TestCase):
    def test_names_are_trimmed(self):
        self.assertEqual(parse_names(" Anna, Ben ,Cem"), ["Anna", "Ben", "Cem"])

    def test_empty_list_is_an_error(self):
        for text in ["", " ", ",", " , ,"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_names(text)


class TeilenCliTest(unittest.TestCase):
    def run_cli(self, args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(args)
        return code, out.getvalue(), err.getvalue()

    def test_spec_output(self):
        code, text, _ = self.run_cli(["teilen", os.path.join(DATA, "bon_party.csv"), "--wg", "Anna,Ben,Cem"])
        self.assertEqual(code, 0)
        self.assertEqual(text, "Gesamt-Pfand: 11,44 €\nAnna: 3,82 €\nBen: 3,81 €\nCem: 3,81 €\n")

    def test_no_people_gives_a_clear_error(self):
        code, text, err = self.run_cli(["teilen", os.path.join(DATA, "bon_party.csv"), "--wg", ""])
        self.assertEqual(code, 1)
        self.assertEqual(text, "")
        self.assertIn("Fehler", err)


if __name__ == "__main__":
    unittest.main()
