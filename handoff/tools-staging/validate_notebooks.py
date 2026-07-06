#!/usr/bin/env python3
"""Validate every file in notebooks/ as a Jupyter notebook.

Checks, per file:
  1. parses as JSON
  2. nbformat == 4
  3. has a non-empty "cells" list
  4. filename ends in .ipynb

Also reports exact-duplicate cell content across files (normalized source hash),
so unreconciled copies are visible instead of silently coexisting.

Exit code 0 = all checks pass AND no duplicates. Exit code 1 otherwise.
Read-only: never modifies any file.
"""
import hashlib
import json
import sys
from pathlib import Path

NB_DIR = Path(__file__).resolve().parent.parent / "notebooks"


def source_fingerprint(nb: dict) -> str:
    """Hash of all code-cell source, whitespace-normalized."""
    chunks = []
    for cell in nb.get("cells", []):
        src = "".join(cell.get("source", []))
        chunks.append(" ".join(src.split()))
    return hashlib.sha256("\n".join(chunks).encode()).hexdigest()[:12]


def main() -> int:
    files = sorted(p for p in NB_DIR.iterdir() if p.is_file() and p.name != "INDEX.md")
    failures = []
    fingerprints: dict[str, list[str]] = {}
    n_json = n_nb4 = n_cells = n_ext = 0

    for p in files:
        try:
            nb = json.loads(p.read_text())
            n_json += 1
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            failures.append(f"NOT JSON: {p.name}: {e}")
            continue
        if nb.get("nbformat") == 4:
            n_nb4 += 1
        else:
            failures.append(f"BAD NBFORMAT ({nb.get('nbformat')!r}): {p.name}")
        if nb.get("cells"):
            n_cells += 1
        else:
            failures.append(f"NO CELLS: {p.name}")
        if p.suffix == ".ipynb":
            n_ext += 1
        else:
            failures.append(f"MISSING .ipynb EXTENSION: {p.name}")
        fingerprints.setdefault(source_fingerprint(nb), []).append(p.name)

    dupes = {h: names for h, names in fingerprints.items() if len(names) > 1}

    print(f"files={len(files)} json_ok={n_json} nbformat4_ok={n_nb4} "
          f"has_cells={n_cells} ext_ok={n_ext} dupe_groups={len(dupes)}")
    for msg in failures:
        print(f"FAIL {msg}")
    for h, names in sorted(dupes.items()):
        print(f"DUPLICATE {h}: " + " | ".join(sorted(names)))

    return 1 if (failures or dupes) else 0


if __name__ == "__main__":
    sys.exit(main())
