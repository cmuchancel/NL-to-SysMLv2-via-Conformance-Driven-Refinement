#!/usr/bin/env python3
"""Compute the Section 4.1 primary outcome from the public release package."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOT = REPO_ROOT / "Open-Source Dataset Release" / "604 positive artifacts"


# Convert a fraction to a percentage while guarding against divide-by-zero.
def percent(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else 100.0 * numerator / denominator


# Load all final successful SysML files from the configured release folder.
def load_successful_models(scan_root: Path) -> list[Path]:
    if not scan_root.exists():
        raise SystemExit(f"Folder not found: {scan_root}")

    sysml_files = sorted(scan_root.rglob("*.sysml"))
    if not sysml_files:
        raise SystemExit(f"No .sysml files found under: {scan_root}")

    return sysml_files


# Count how many cases succeeded on the very first attempt.
def count_single_shot_successes(sysml_files: list[Path]) -> int:
    return sum(path.name == "iteration_00.sysml" for path in sysml_files)


# Print only the two headline Figure 3 rates.
def print_primary_outcome_summary(scan_root: Path, sysml_files: list[Path]) -> None:
    total_cases = len(sysml_files)
    single_shot_cases = count_single_shot_successes(sysml_files)

    print(f"Scanning: {scan_root.name}")
    print()
    print(f"Total prompt-level cases: {total_cases}")
    print(
        f"Single-shot production conformance: "
        f"{single_shot_cases}/{total_cases} "
        f"({percent(single_shot_cases, total_cases):.2f}%)"
    )
    print(
        f"Final pipeline production conformance: "
        f"{total_cases}/{total_cases} "
        f"({percent(total_cases, total_cases):.2f}%)"
    )


# Run the minimal load-and-report flow for the primary outcome summary.
def main() -> None:
    sysml_files = load_successful_models(SCAN_ROOT)
    print_primary_outcome_summary(SCAN_ROOT, sysml_files)


if __name__ == "__main__":
    main()
