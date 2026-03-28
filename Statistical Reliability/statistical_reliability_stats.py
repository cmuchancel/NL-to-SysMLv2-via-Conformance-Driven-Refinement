#!/usr/bin/env python3
"""Compute the Section 4.4 statistical-reliability summary from the public release package."""

from __future__ import annotations

from math import log
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOT = REPO_ROOT / "Open-Source Dataset Release" / "604 positive artifacts"
ALPHA = 0.05


# Convert a fraction to a percentage while guarding against divide-by-zero.
def percent(numerator: float, denominator: float) -> float:
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


# Compute the exact and approximate confidence-bound quantities used in the submitted paper.
def compute_reliability_bounds(total_cases: int) -> tuple[float, float, float]:
    lower_convergence_bound = ALPHA ** (1 / total_cases)
    upper_failure_bound = 1 - lower_convergence_bound
    upper_failure_bound_approx = -log(ALPHA) / total_cases
    return lower_convergence_bound, upper_failure_bound, upper_failure_bound_approx


# Print the Section 4.4 reliability summary and practical interpretation.
def print_statistical_reliability_summary(scan_root: Path, sysml_files: list[Path]) -> None:
    total_cases = len(sysml_files)
    single_shot_cases = count_single_shot_successes(sysml_files)
    lower_convergence_bound, upper_failure_bound, upper_failure_bound_approx = (
        compute_reliability_bounds(total_cases)
    )

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
    print()
    print(
        "Exact one-sided 95% lower confidence bound on convergence probability: "
        f"{lower_convergence_bound:.6f} ({lower_convergence_bound * 100:.2f}%)"
    )
    print(
        "Exact one-sided 95% upper confidence bound on failure probability: "
        f"{upper_failure_bound:.6f} ({upper_failure_bound * 100:.3f}%)"
    )
    print(
        "Large-n approximation for the failure bound: "
        f"{upper_failure_bound_approx:.6f} ({upper_failure_bound_approx * 100:.3f}%)"
    )
    print()
    print(
        "Interpretation: with 95% confidence, the true convergence probability "
        f"is at least {lower_convergence_bound * 100:.2f}%."
    )
    print(
        "Interpretation: with 95% confidence, the true failure rate "
        f"is below about {upper_failure_bound * 100:.1f}%."
    )


# Run the minimal load-and-report flow for the Section 4.4 summary.
def main() -> None:
    sysml_files = load_successful_models(SCAN_ROOT)
    print_statistical_reliability_summary(SCAN_ROOT, sysml_files)


if __name__ == "__main__":
    main()
