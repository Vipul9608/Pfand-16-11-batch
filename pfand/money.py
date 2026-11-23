"""Money helpers. Money is always an integer number of cents."""
import re

_GERMAN_MONEY = re.compile(r"^(-?)(\d+)(?:,(\d{1,2}))?$")


def format_eur(cents):
    """Show cents in the German format.

    125 -> '1,25 €'     1234567 -> '12.345,67 €'     -125 -> '-1,25 €'
    """
    if isinstance(cents, bool) or not isinstance(cents, int):
        raise TypeError(f"Money must be a whole number of cents, not {cents!r}")
    sign = "-" if cents < 0 else ""
    euros, rest = divmod(abs(cents), 100)
    euros_text = f"{euros:,}".replace(",", ".")
    return f"{sign}{euros_text},{rest:02d} €"


def parse_eur(text):
    """Read a German money text and return cents.

    '1,25 €' -> 125     '0,5' -> 50     '12' -> 1200     '1.234,50 €' -> 123450     '-1,50 €' -> -150
    """
    cleaned = text.replace("€", "").strip().replace(".", "")
    match = _GERMAN_MONEY.match(cleaned)
    if not match:
        raise ValueError(f"Kein gültiger Geldbetrag: {text!r}")
    sign, euros, cents = match.groups()
    total = int(euros) * 100 + int((cents or "0").ljust(2, "0"))
    return -total if sign else total
