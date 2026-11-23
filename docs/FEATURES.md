# Feature menu

Pick a feature for mission 3 (A or E) and for the boss mission 6 (B, C, D, or your own idea).
The examples show what the finished feature prints. They are the **specification**: write your tests from them.
Every feature needs: a plan first, tests, and one clear commit.

All examples use the list `data/bon_party.csv`: 24 x einweg, 18 x mehrweg_bier, 6 x mehrweg_wasser, 1 x kasten_bier = 11,44 €.

---

## A. Pfandbon (a receipt as text)

    python -m pfand bon data/bon_party.csv

prints:

```
================================
           PFAND-BON            
================================
24 x Einweg (Dose/PET)    6,00 €
18 x Mehrweg Bier         1,44 €
 6 x Mehrweg Wasser       0,90 €
 1 x Kasten Bier          3,10 €
--------------------------------
Summe                    11,44 €
================================
```

Rules:
- Every line is exactly 32 characters wide.
- The counts are right-aligned, the money is right-aligned.
- The labels come from `LABELS` in `pfand/rates.py`.
- An empty list must not crash.

---

## B. Sparziel (how many bottles for my goal?)

    python -m pfand ziel 30,00 --art einweg --schon 5,00

prints:

```
Ziel: 30,00 €
Schon gespart: 5,00 €
Es fehlen noch 25,00 €: das sind 100 x Einweg (Dose/PET).
```

Rules:
- The goal and the saved amount are German money texts: use `parse_eur`.
- Round **up**: a bottle is not divisible. 30,01 € needs one bottle more than 30,00 €.
- If the goal is reached, print `Ziel erreicht!` instead of the last line.
- A goal of 0 or less is an error with a clear message.

---

## C. Statistik (many lists at once)

    python -m pfand statistik "data/bon_*.csv"

prints:

```
Statistik für 4 Listen
  Einweg (Dose/PET)      52 Stück    13,00 €
  Mehrweg Bier           40 Stück     3,20 €
  Mehrweg Wasser         19 Stück     2,85 €
  Kasten Wasser           1 Stück     1,50 €
  Kasten Bier             1 Stück     3,10 €
Gesamt: 23,65 €
Beste Liste: bon_party.csv (11,44 €)
Durchschnitt pro Liste: 5,91 €
```

Rules:
- Windows shells do not expand `*`. Your code must expand patterns with `glob` itself.
- The average is rounded to the nearest cent, halves up. (Not Python's `round`: it rounds halves to the even number.)

---

## D. Bericht (an HTML report)

    python -m pfand report "data/bon_*.csv" --html report.html

prints `Bericht geschrieben: report.html` and writes a web page with a title, the total in German format,
and one bar for each list (the bar length is the total, compared with the biggest list).

Rules: no libraries; escape file names with `html.escape`; open the file in your browser and look at it.

---

## E. WG teilen (share the Pfand fairly)

    python -m pfand teilen data/bon_party.csv --wg Anna,Ben,Cem

prints:

```
Gesamt-Pfand: 11,44 €
Anna: 3,82 €
Ben: 3,81 €
Cem: 3,81 €
```

Rules:
- The shares must add up to the total, exactly. 11,44 € cannot be split into three equal amounts: the first people get one extra cent.
- A list with no people is an error with a clear message.
- Write a test that checks "the shares add up to the total" for many totals and many numbers of people.

---

## Your own idea

Small and testable. Ask Claude to **interview you** about the hard parts and edge cases, and to write a short spec to `SPEC.md`. Then clear the context and build from the spec.
