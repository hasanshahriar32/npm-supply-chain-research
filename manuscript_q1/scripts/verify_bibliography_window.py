#!/usr/bin/env python3
"""Check the journal manuscript's compiled bibliography against verified publications."""
import json
from pathlib import Path
import re

JOURNAL = Path(__file__).resolve().parents[1]
BIB = JOURNAL / "bibliography/references_q1.bib"
AUDIT = JOURNAL / "results/bibliography_audit.json"


def verify():
    entries = dict(re.findall(r"(?ms)^@\w+\{([-\w]+),\s*(.*?)^\}", BIB.read_text()))
    audit = json.loads(AUDIT.read_text())
    publications = audit["publications"]
    for name in ("main_q1", "main_q1_anonymous"):
        bbl = (JOURNAL / "build" / f"{name}.bbl").read_text()
        keys = re.findall(r"\\bibitem\{([^}]+)\}", bbl)
        assert len(keys) == len(set(keys)) and set(keys) == set(publications)
        for key in keys:
            text, record = entries[key], publications[key]
            year = int(re.search(r"\byear\s*=\s*\{(\d{4})\}", text)[1])
            assert audit["year_start"] <= year <= audit["year_end"]
            assert audit["year_start"] <= record["publication_date"][0] <= audit["year_end"]
            doi = re.search(r"\bdoi\s*=\s*\{([^}]+)\}", text)[1]
            assert doi.casefold() == record["doi"].casefold()
        journal_count = sum(publications[k]["kind"] == "journal" for k in keys)
        conference_count = len(keys) - journal_count
        assert 0 < conference_count <= 2 and journal_count > conference_count
        print(f"{name}: {journal_count} journals and {conference_count} conference papers, "
              f"{audit['year_start']}–{audit['year_end']}")


if __name__ == "__main__":
    verify()
