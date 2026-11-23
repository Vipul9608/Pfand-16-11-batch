"""Read a list of bottles from a CSV file, and calculate the refund."""
import csv

from .rates import rate_for


def read_bon(path):
    """Read a Pfand list from a CSV file.

    Columns: Art;Anzahl;Bemerkung    Returns a list like [("einweg", 24), ("kasten_bier", 1)].
    """
    items = []
    # Excel in Germany saves CSV with semicolons and a UTF-8 BOM.
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            items.append((row["Art"], int(row["Anzahl"])))
    return items


def refund(items):
    """Total Pfand in cents for a list of (kind, count) pairs."""
    total = 0
    for kind, count in items:
        if count < 0:
            raise ValueError(f"Anzahl darf nicht negativ sein: {kind} {count}")
        total += rate_for(kind) * count
    return total
