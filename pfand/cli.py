"""The command line of Pfand-Profi.   python -m pfand --help"""
import argparse
import sys

from .bon import format_bon
from .money import format_eur
from .rates import LABELS, RATES
from .receipt import read_bon, refund
from .share import parse_names, split_cents


def cmd_raten(args):
    print("Pfand-Sätze")
    for kind, cents in RATES.items():
        print(f"  {LABELS[kind]:<20} {format_eur(cents):>8}")
    return 0


def cmd_refund(args):
    items = read_bon(args.datei)
    print(f"Summe: {format_eur(refund(items))}")
    return 0


def cmd_bon(args):
    print(format_bon(read_bon(args.datei)))
    return 0


def cmd_teilen(args):
    try:
        names = parse_names(args.wg)
    except ValueError as error:
        print(f"Fehler: {error}", file=sys.stderr)
        return 1
    total = refund(read_bon(args.datei))
    print(f"Gesamt-Pfand: {format_eur(total)}")
    for name, share in zip(names, split_cents(total, len(names))):
        print(f"{name}: {format_eur(share)}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="pfand", description="Pfand-Profi: dein Flaschen-Assistent")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("raten", help="zeige die Pfand-Sätze").set_defaults(func=cmd_raten)
    p = sub.add_parser("refund", help="berechne die Summe für eine CSV-Liste")
    p.add_argument("datei", help="CSV-Datei mit Art;Anzahl;Bemerkung")
    p.set_defaults(func=cmd_refund)
    p = sub.add_parser("bon", help="drucke einen Pfandbon für eine CSV-Liste")
    p.add_argument("datei", help="CSV-Datei mit Art;Anzahl;Bemerkung")
    p.set_defaults(func=cmd_bon)
    p = sub.add_parser("teilen", help="teile das Pfand fair in der WG")
    p.add_argument("datei", help="CSV-Datei mit Art;Anzahl;Bemerkung")
    p.add_argument("--wg", required=True, help="Namen mit Komma, zum Beispiel Anna,Ben,Cem")
    p.set_defaults(func=cmd_teilen)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)
