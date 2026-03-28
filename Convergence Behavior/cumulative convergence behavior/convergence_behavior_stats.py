#!/usr/bin/env python3
"""Compute the Section 4.3 convergence-behavior summary from the public release package."""

from __future__ import annotations

from collections import Counter
from math import prod
from pathlib import Path
from statistics import mean


REPO_ROOT = Path(__file__).resolve().parents[2]
SCAN_ROOT = REPO_ROOT / "Open-Source Dataset Release" / "604 positive artifacts"


# Convert a fraction to a percentage while guarding against divide-by-zero.
def percent(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else 100.0 * numerator / denominator


# Load all successful final SysML files from the release folder.
def load_successful_models(scan_root: Path) -> list[Path]:
    if not scan_root.exists():
        raise SystemExit(f"Folder not found: {scan_root}")

    sysml_files = sorted(scan_root.rglob("*.sysml"))
    if not sysml_files:
        raise SystemExit(f"No .sysml files found under: {scan_root}")

    return sysml_files


# Count how many cases first conformed at each repair-cycle index k.
def count_cases_by_repair_cycle(sysml_files: list[Path]) -> Counter[int]:
    return Counter(int(path.stem.split("_")[1]) for path in sysml_files)


# Expand a count dictionary into a sorted list of observed repair-cycle values.
def expand_values(counts_by_k: Counter[int]) -> list[int]:
    return sorted(k for k, count in counts_by_k.items() for _ in range(count))


# Compute Tukey quartiles so the printed IQR matches the paper's summary wording.
def tukey_quartiles(values: list[int]) -> tuple[float, float, float]:
    ordered = sorted(values)
    n = len(ordered)
    midpoint = n // 2

    if n % 2 == 0:
        lower_half = ordered[:midpoint]
        upper_half = ordered[midpoint:]
    else:
        lower_half = ordered[:midpoint]
        upper_half = ordered[midpoint + 1 :]

    def median_of_list(items: list[int]) -> float:
        size = len(items)
        if size % 2 == 0:
            return (items[size // 2 - 1] + items[size // 2]) / 2
        return items[size // 2]

    return (
        median_of_list(lower_half),
        median_of_list(ordered),
        median_of_list(upper_half),
    )


# Print the pooled cumulative curve points used for Figure 5.
def print_cumulative_curve(counts_by_k: Counter[int], total_cases: int) -> None:
    print("Figure 5 cumulative acceptance by repair cycle:")
    running_total = 0
    for k in range(max(counts_by_k) + 1):
        running_total += counts_by_k.get(k, 0)
        print(
            f"  k={k}: {running_total}/{total_cases} "
            f"({percent(running_total, total_cases):.2f}%)"
        )
    print()


# Print the grouped distribution table used for Table 1.
def print_grouped_table(counts_by_k: Counter[int], total_cases: int) -> None:
    grouped_rows = [
        ("0", counts_by_k.get(0, 0)),
        ("1", counts_by_k.get(1, 0)),
        ("2", counts_by_k.get(2, 0)),
        ("3", counts_by_k.get(3, 0)),
        ("4", counts_by_k.get(4, 0)),
        ("5-7", sum(counts_by_k.get(k, 0) for k in range(5, 9))),
    ]

    print("Table 1 grouped distribution:")
    cumulative_cases = 0
    for label, cases in grouped_rows:
        cumulative_cases += cases
        print(
            f"  k={label}: {cases} cases, "
            f"{percent(cases, total_cases):.2f}% share, "
            f"{percent(cumulative_cases, total_cases):.2f}% cumulative"
        )
    print()


# Build the cumulative acceptance fraction A_k at each repair-cycle index k.
def cumulative_acceptance_fractions(
    counts_by_k: Counter[int], total_cases: int
) -> dict[int, float]:
    acceptance_by_k: dict[int, float] = {}
    running_total = 0
    for k in range(max(counts_by_k) + 1):
        running_total += counts_by_k.get(k, 0)
        acceptance_by_k[k] = running_total / total_cases
    return acceptance_by_k


# Return the first repair-cycle index whose cumulative acceptance reaches a target.
def first_threshold_k(acceptance_by_k: dict[int, float], target: float) -> int:
    for k in sorted(acceptance_by_k):
        if acceptance_by_k[k] >= target:
            return k
    raise SystemExit(f"No repair cycle reached target acceptance {target:.2f}")


# Print the residual-mass contraction summary and threshold metrics from Section 4.3.
def print_rate_characterization(counts_by_k: Counter[int], total_cases: int) -> None:
    acceptance_by_k = cumulative_acceptance_fractions(counts_by_k, total_cases)
    residual_by_k = {k: 1.0 - acceptance_by_k[k] for k in range(5)}

    early_ratios = [
        residual_by_k[1] / residual_by_k[0],
        residual_by_k[2] / residual_by_k[1],
        residual_by_k[3] / residual_by_k[2],
    ]
    average_contraction = prod(early_ratios) ** (1 / len(early_ratios))

    print("Rate characterization:")
    print(
        "  Residual failure mass: "
        + ", ".join(f"R_{k} = {residual_by_k[k]:.4f}" for k in range(5))
    )
    print(
        "  Early-cycle contraction ratios: "
        f"rho_0 = {early_ratios[0]:.2f}, "
        f"rho_1 = {early_ratios[1]:.2f}, "
        f"rho_2 = {early_ratios[2]:.2f}"
    )
    print(f"  Geometric-mean early-cycle contraction factor: {average_contraction:.2f}")
    print(
        f"  Threshold repair cycles: "
        f"T90 = {first_threshold_k(acceptance_by_k, 0.90)}, "
        f"T95 = {first_threshold_k(acceptance_by_k, 0.95)}, "
        f"T99 = {first_threshold_k(acceptance_by_k, 0.99)}"
    )
    print()


# Print the summary statistics described in the Section 4.3 text.
def print_summary_statistics(counts_by_k: Counter[int]) -> None:
    repair_cycles = expand_values(counts_by_k)
    total_attempts = [value + 1 for value in repair_cycles]

    repair_q1, repair_median, repair_q3 = tukey_quartiles(repair_cycles)
    attempts_q1, attempts_median, attempts_q3 = tukey_quartiles(total_attempts)

    print("Summary statistics:")
    print(
        f"  Repair cycles to first conformance: "
        f"mean {mean(repair_cycles):.3f}, "
        f"median {repair_median:.0f}, "
        f"IQR {repair_q1:.0f}-{repair_q3:.0f}, "
        f"max {max(repair_cycles)}"
    )
    print(
        f"  Total attempts to first conformance: "
        f"mean {mean(total_attempts):.3f}, "
        f"median {attempts_median:.0f}, "
        f"IQR {attempts_q1:.0f}-{attempts_q3:.0f}, "
        f"max {max(total_attempts)}"
    )


# Run the minimal load-and-report flow for the convergence summary.
def main() -> None:
    sysml_files = load_successful_models(SCAN_ROOT)
    counts_by_k = count_cases_by_repair_cycle(sysml_files)
    total_cases = len(sysml_files)

    print(f"Scanning: {SCAN_ROOT.name}")
    print()
    print_cumulative_curve(counts_by_k, total_cases)
    print_grouped_table(counts_by_k, total_cases)
    print_rate_characterization(counts_by_k, total_cases)
    print_summary_statistics(counts_by_k)


if __name__ == "__main__":
    main()
