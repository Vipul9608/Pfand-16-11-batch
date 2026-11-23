"""Pfand rates. All money in this project is a WHOLE NUMBER of cents."""

RATES = {
    "einweg": 25,          # cans and disposable plastic bottles
    "mehrweg_bier": 8,     # reusable beer bottle
    "mehrweg_wasser": 15,  # many reusable water and soft-drink bottles
    "kasten_wasser": 150,  # crate for water bottles
    "kasten_bier": 310,    # beer crate
}

LABELS = {
    "einweg": "Einweg (Dose/PET)",
    "mehrweg_bier": "Mehrweg Bier",
    "mehrweg_wasser": "Mehrweg Wasser",
    "kasten_wasser": "Kasten Wasser",
    "kasten_bier": "Kasten Bier",
}


def rate_for(kind):
    """Pfand for one item of this kind, in cents. Capital letters and spaces do not matter."""
    key = str(kind).strip().lower()
    if key not in RATES:
        raise ValueError(f"Unbekannte Pfandart: {kind!r}")
    return RATES[key]
