"""WG teilen: split the Pfand fairly, so that the shares add up to the total exactly."""


def split_cents(total_cents, people):
    """Split cents into `people` shares. The first people get one extra cent if it does not divide."""
    if people < 1:
        raise ValueError("Mindestens eine Person wird gebraucht.")
    base, extra = divmod(total_cents, people)
    return [base + 1 if index < extra else base for index in range(people)]


def parse_names(text):
    """Read 'Anna,Ben,Cem' into a list of names. An empty list is an error."""
    names = [name.strip() for name in text.split(",") if name.strip()]
    if not names:
        raise ValueError("Die WG-Liste ist leer: gib Namen an, zum Beispiel --wg Anna,Ben,Cem")
    return names
