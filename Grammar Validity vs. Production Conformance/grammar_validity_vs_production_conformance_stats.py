#!/usr/bin/env python3
"""Compute the Section 4.5 grammar-validity versus production-conformance summary."""

from __future__ import annotations

import csv
from pathlib import Path


SECTION_ROOT = Path(__file__).resolve().parent
COUNTS_PATH = SECTION_ROOT / "data" / "figure_7_confusion_matrix.csv"


# Convert a fraction to a percentage while guarding against divide-by-zero.
def percent(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else 100.0 * numerator / denominator


# Load the four Figure 7 confusion-matrix cells from the local CSV.
def load_confusion_matrix(counts_path: Path) -> dict[str, int]:
    if not counts_path.exists():
        raise SystemExit(f"File not found: {counts_path}")

    counts = {
        "antlr_fail_syside_fail": 0,
        "antlr_fail_syside_pass": 0,
        "antlr_pass_syside_fail": 0,
        "antlr_pass_syside_pass": 0,
    }

    with counts_path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            key = f"antlr_{row['antlr'].lower()}_syside_{row['syside'].lower()}"
            counts[key] = int(row["cases"])

    return counts


# Print the Section 4.5 totals, confusion matrix, and gap percentages.
def print_grammar_vs_production_summary(
    counts_path: Path, counts: dict[str, int]
) -> None:
    total_cases = sum(counts.values())
    antlr_passes = counts["antlr_pass_syside_fail"] + counts["antlr_pass_syside_pass"]
    syside_passes = counts["antlr_fail_syside_pass"] + counts["antlr_pass_syside_pass"]
    operational_gap = counts["antlr_pass_syside_fail"]

    print(f"Scanning: {counts_path.name}")
    print()
    print(f"Total initial candidates: {total_cases}")
    print(
        f"ANTLR grammar pass: "
        f"{antlr_passes}/{total_cases} "
        f"({percent(antlr_passes, total_cases):.2f}%)"
    )
    print(
        f"SysIDE production conformance pass: "
        f"{syside_passes}/{total_cases} "
        f"({percent(syside_passes, total_cases):.2f}%)"
    )
    print()
    print("Figure 7 confusion matrix:")
    print(f"  ANTLR fail, SysIDE fail: {counts['antlr_fail_syside_fail']}")
    print(f"  ANTLR fail, SysIDE pass: {counts['antlr_fail_syside_pass']}")
    print(f"  ANTLR pass, SysIDE fail: {counts['antlr_pass_syside_fail']}")
    print(f"  ANTLR pass, SysIDE pass: {counts['antlr_pass_syside_pass']}")
    print()
    print(
        f"Grammar-valid but production-failing cases: "
        f"{operational_gap}/{antlr_passes} "
        f"({percent(operational_gap, antlr_passes):.2f}% of grammar-valid artifacts)"
    )
    print(
        f"Grammar-valid but production-failing cases: "
        f"{operational_gap}/{total_cases} "
        f"({percent(operational_gap, total_cases):.2f}% of all initial outputs)"
    )
    print(
        f"Production-pass while grammar-fail: "
        f"{counts['antlr_fail_syside_pass']}/{total_cases} "
        f"({percent(counts['antlr_fail_syside_pass'], total_cases):.2f}%)"
    )


# Run the minimal load-and-report flow for the Section 4.5 summary.
def main() -> None:
    counts = load_confusion_matrix(COUNTS_PATH)
    print_grammar_vs_production_summary(COUNTS_PATH, counts)


if __name__ == "__main__":
    main()
