"""Pfandbon: the refund as a text receipt, 32 characters wide."""
from .money import format_eur
from .rates import LABELS, normalize_kind, rate_for
from .receipt import refund

WIDTH = 32


def _line(left, right):
    """Left text and right text on one line of exactly WIDTH characters."""
    gap = WIDTH - len(left) - len(right)
    return left + " " * max(gap, 1) + right


def format_bon(items):
    """Return the Pfandbon for a list of (kind, count) pairs as one text."""
    count_width = max((len(str(count)) for _, count in items), default=1)
    lines = ["=" * WIDTH, "PFAND-BON".center(WIDTH), "=" * WIDTH]
    for kind, count in items:
        label = LABELS[normalize_kind(kind)]
        lines.append(_line(f"{count:>{count_width}} x {label}", format_eur(rate_for(kind) * count)))
    lines.append("-" * WIDTH)
    lines.append(_line("Summe", format_eur(refund(items))))
    lines.append("=" * WIDTH)
    return "\n".join(lines)
