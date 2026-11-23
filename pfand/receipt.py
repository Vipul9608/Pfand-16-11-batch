"""Read a list of bottles from a CSV file, and calculate the refund."""
import csv

from .rates import rate_for


def read_bon(path):
    """Read a Pfand list from a CSV file.

    Columns: Art;Anzahl;Bemerkung    Returns a list like [("einweg", 24), ("kasten_bier", 1)].
    """
    items = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            items.append((row["Art"], int(row["Anzahl"])))
    return items


def refund(items):
    """Total Pfand in cents for a list of (kind, count) pairs."""
    total = 0
    for kind, count in items:
        total += rate_for(kind) * count
    return total
