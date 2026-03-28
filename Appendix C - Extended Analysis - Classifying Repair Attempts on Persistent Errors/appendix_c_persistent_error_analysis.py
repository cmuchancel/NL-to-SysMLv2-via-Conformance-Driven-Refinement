#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR / "data" / "exact_signature_transition_analysis.csv"
RESULTS_DIR = SCRIPT_DIR / "results"

STATE_SUMMARY_FILE = RESULTS_DIR / "summary_transition_states.csv"
PERSISTENT_OUTCOME_FILE = RESULTS_DIR / "summary_persistent_transition_outcomes.csv"


# Convert the CSV boolean strings into Python booleans.
def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


# Compute percentages safely for summary printing and CSV output.
def percent(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else 100.0 * numerator / denominator


# Load the local Appendix C event-level transition dataset.
def load_transition_rows() -> list[dict[str, object]]:
    if not DATA_FILE.exists():
        raise SystemExit(f"Data file not found: {DATA_FILE}")

    with DATA_FILE.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    if not rows:
        raise SystemExit(f"No transition rows found in: {DATA_FILE}")

    parsed_rows: list[dict[str, object]] = []
    for row in rows:
        parsed_rows.append(
            {
                "persists_next": parse_bool(row["persists_next"]),
                "resolved_next": parse_bool(row["resolved_next"]),
                "same_snippet_when_persist": parse_bool(row["same_snippet_when_persist"]),
                "changed_snippet_when_persist": parse_bool(row["changed_snippet_when_persist"]),
            }
        )

    return parsed_rows


# Count the deterministic transition states used in the Appendix C analysis.
def count_transition_states(rows: list[dict[str, object]]) -> Counter[str]:
    counts: Counter[str] = Counter()

    for row in rows:
        if row["resolved_next"]:
            counts["resolved_next"] += 1
        elif row["same_snippet_when_persist"]:
            counts["persistent_same_snippet"] += 1
        elif row["changed_snippet_when_persist"]:
            counts["persistent_changed_snippet"] += 1
        else:
            counts["persistent_no_comparable_snippet"] += 1

    return counts


# Collapse the persistent cases into the two paper-facing outcome categories.
def count_persistent_outcomes(state_counts: Counter[str]) -> Counter[str]:
    return Counter(
        {
            "unaddressed_and_not_fixed": state_counts["persistent_same_snippet"],
            "addressed_but_not_fixed": (
                state_counts["persistent_changed_snippet"]
                + state_counts["persistent_no_comparable_snippet"]
            ),
        }
    )


# Save the deterministic state counts to a local CSV.
def write_state_summary(state_counts: Counter[str], total_transitions: int) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        ("resolved_next", state_counts["resolved_next"]),
        ("persistent_same_snippet", state_counts["persistent_same_snippet"]),
        ("persistent_changed_snippet", state_counts["persistent_changed_snippet"]),
        ("persistent_no_comparable_snippet", state_counts["persistent_no_comparable_snippet"]),
    ]

    with STATE_SUMMARY_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["deterministic_state", "count", "share_pct_of_total"])
        for label, count in rows:
            writer.writerow([label, count, f"{percent(count, total_transitions):.12f}"])


# Save the paper-facing persistent split to a local CSV.
def write_persistent_outcomes(
    persistent_outcomes: Counter[str], persistent_total: int
) -> None:
    rows = [
        ("unaddressed_and_not_fixed", persistent_outcomes["unaddressed_and_not_fixed"]),
        ("addressed_but_not_fixed", persistent_outcomes["addressed_but_not_fixed"]),
    ]

    with PERSISTENT_OUTCOME_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["grouped_outcome", "count", "share_pct_of_persistent"])
        for label, count in rows:
            writer.writerow([label, count, f"{percent(count, persistent_total):.12f}"])


# Print the Appendix C counts in the same form used in the paper text.
def print_summary(state_counts: Counter[str], persistent_outcomes: Counter[str]) -> None:
    total_transitions = sum(state_counts.values())
    resolved_next = state_counts["resolved_next"]
    persistent_total = total_transitions - resolved_next

    print("Scanning: exact_signature_transition_analysis.csv")
    print()
    print("C.1 Persistent exact-error transition counts")
    print(f"Total exact-error transitions: {total_transitions}")
    print(
        f"Resolved by the next iteration: "
        f"{resolved_next}/{total_transitions} "
        f"({percent(resolved_next, total_transitions):.2f}%)"
    )
    print(
        f"Persistent through the next iteration: "
        f"{persistent_total}/{total_transitions} "
        f"({percent(persistent_total, total_transitions):.2f}%)"
    )
    print()
    print("Persistent deterministic states:")
    print(
        f"persistent_same_snippet: {state_counts['persistent_same_snippet']}/{persistent_total} "
        f"({percent(state_counts['persistent_same_snippet'], persistent_total):.2f}%)"
    )
    print(
        f"persistent_changed_snippet: {state_counts['persistent_changed_snippet']}/{persistent_total} "
        f"({percent(state_counts['persistent_changed_snippet'], persistent_total):.2f}%)"
    )
    print(
        "persistent_no_comparable_snippet: "
        f"{state_counts['persistent_no_comparable_snippet']}/{persistent_total} "
        f"({percent(state_counts['persistent_no_comparable_snippet'], persistent_total):.2f}%)"
    )
    print()
    print("C.2 Persistent outcome split")
    print(
        "Unaddressed and not fixed: "
        f"{persistent_outcomes['unaddressed_and_not_fixed']}/{persistent_total} "
        f"({percent(persistent_outcomes['unaddressed_and_not_fixed'], persistent_total):.2f}%)"
    )
    print(
        "Addressed but not fixed: "
        f"{persistent_outcomes['addressed_but_not_fixed']}/{persistent_total} "
        f"({percent(persistent_outcomes['addressed_but_not_fixed'], persistent_total):.2f}%)"
    )


def main() -> None:
    rows = load_transition_rows()
    state_counts = count_transition_states(rows)
    persistent_outcomes = count_persistent_outcomes(state_counts)

    total_transitions = sum(state_counts.values())
    persistent_total = total_transitions - state_counts["resolved_next"]

    write_state_summary(state_counts, total_transitions)
    write_persistent_outcomes(persistent_outcomes, persistent_total)
    print_summary(state_counts, persistent_outcomes)


if __name__ == "__main__":
    main()
