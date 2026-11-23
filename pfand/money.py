"""Money helpers. Money is always an integer number of cents."""


def format_eur(cents):
    """Show cents in the German format.

    125 -> '1,25 €'     1234567 -> '12.345,67 €'
    """
    euros, rest = divmod(cents, 100)
    euros_text = f"{euros:,}".replace(",", ".")
    return f"{euros_text},{rest:02d} €"


def parse_eur(text):
    """Read a German money text and return cents.

    '1,25 €' -> 125     '0,5' -> 50     '12' -> 1200     '1.234,50 €' -> 123450
    """
    t = text.replace("€", "").strip().replace(".", "")
    if "," in t:
        euros, cents = t.split(",")
        return int(euros) * 100 + int(cents.ljust(2, "0"))
    return int(t) * 100
