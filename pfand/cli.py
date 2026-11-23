"""The command line of Pfand-Profi.   python -m pfand --help"""
import argparse

from .money import format_eur
from .rates import LABELS, RATES
from .receipt import read_bon, refund


def cmd_raten(args):
    print("Pfand-Sätze")
    for kind, cents in RATES.items():
        print(f"  {LABELS[kind]:<20} {format_eur(cents):>8}")
    return 0


def cmd_refund(args):
    items = read_bon(args.datei)
    print(f"Summe: {format_eur(refund(items))}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="pfand", description="Pfand-Profi: dein Flaschen-Assistent")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("raten", help="zeige die Pfand-Sätze").set_defaults(func=cmd_raten)
    p = sub.add_parser("refund", help="berechne die Summe für eine CSV-Liste")
    p.add_argument("datei", help="CSV-Datei mit Art;Anzahl;Bemerkung")
    p.set_defaults(func=cmd_refund)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)
