#!/usr/bin/env python3
"""Rebuild the Section 4.5 Figure 7 confusion-matrix data from the released trajectory corpus."""

from __future__ import annotations

import csv
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


SECTION_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SECTION_ROOT.parent
TRAJECTORY_ROOT = REPO_ROOT / "Open-Source Dataset Release" / "trajectory level corpus"
ANTLR_CHECK = SECTION_ROOT / "checkers" / "antlr_check.py"
SYSIDE_CHECK = SECTION_ROOT / "checkers" / "syside_check.py"
AUDIT_CSV = SECTION_ROOT / "data" / "figure_7_first_iteration_audit.csv"
COUNTS_CSV = SECTION_ROOT / "data" / "figure_7_confusion_matrix.csv"
MAX_WORKERS = 6


# Find the initial candidate for every provider/prompt case in the released corpus.
def find_initial_candidates(trajectory_root: Path) -> list[tuple[str, str, Path]]:
    if not trajectory_root.exists():
        raise SystemExit(f"Folder not found: {trajectory_root}")

    items: list[tuple[str, str, Path]] = []
    for provider_dir in sorted(p for p in trajectory_root.iterdir() if p.is_dir()):
        for case_dir in sorted(p for p in provider_dir.iterdir() if p.is_dir()):
            sysml_path = case_dir / "iteration_00.sysml"
            if not sysml_path.exists():
                raise SystemExit(f"Missing initial candidate: {sysml_path}")
            items.append((provider_dir.name, case_dir.name, sysml_path))

    if not items:
        raise SystemExit(f"No initial candidates found under: {trajectory_root}")

    return items


# Run one local checker script against one SysML file.
def run_checker(checker_path: Path, sysml_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(checker_path), str(sysml_path)],
        capture_output=True,
        text=True,
    )


# Audit one initial candidate with both ANTLR and SysIDE.
def audit_one(item: tuple[str, str, Path]) -> dict[str, str]:
    provider, prompt_id, sysml_path = item
    antlr = run_checker(ANTLR_CHECK, sysml_path)
    syside = run_checker(SYSIDE_CHECK, sysml_path)

    antlr_ok = antlr.returncode == 0
    syside_ok = syside.returncode == 0

    if antlr_ok and syside_ok:
        label = "antlr_pass_syside_pass"
    elif antlr_ok and not syside_ok:
        label = "antlr_pass_syside_fail"
    elif not antlr_ok and syside_ok:
        label = "antlr_fail_syside_pass"
    else:
        label = "antlr_fail_syside_fail"

    return {
        "provider": provider,
        "prompt_id": prompt_id,
        "sysml_path": str(sysml_path.relative_to(REPO_ROOT)),
        "antlr_ok": str(antlr_ok),
        "syside_ok": str(syside_ok),
        "label": label,
        "antlr_exit_code": str(antlr.returncode),
        "syside_exit_code": str(syside.returncode),
    }


# Run the paired audit over all 604 initial candidates.
def build_audit_rows(items: list[tuple[str, str, Path]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(audit_one, item) for item in items]
        for future in as_completed(futures):
            rows.append(future.result())
    return sorted(rows, key=lambda row: (row["provider"], int(row["prompt_id"])))


# Count the four Figure 7 confusion-matrix cells from the audit rows.
def count_confusion_matrix(rows: list[dict[str, str]]) -> dict[str, int]:
    counts = {
        "antlr_fail_syside_fail": 0,
        "antlr_fail_syside_pass": 0,
        "antlr_pass_syside_fail": 0,
        "antlr_pass_syside_pass": 0,
    }
    for row in rows:
        counts[row["label"]] += 1
    return counts


# Save the per-case audit CSV for transparent re-checking.
def write_audit_csv(rows: list[dict[str, str]], audit_csv: Path) -> None:
    audit_csv.parent.mkdir(parents=True, exist_ok=True)
    with audit_csv.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "provider",
                "prompt_id",
                "sysml_path",
                "antlr_ok",
                "syside_ok",
                "label",
                "antlr_exit_code",
                "syside_exit_code",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


# Save the four-cell confusion matrix used by the summary script.
def write_counts_csv(counts: dict[str, int], counts_csv: Path) -> None:
    counts_csv.parent.mkdir(parents=True, exist_ok=True)
    with counts_csv.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["antlr", "syside", "cases"])
        writer.writerow(["fail", "fail", counts["antlr_fail_syside_fail"]])
        writer.writerow(["fail", "pass", counts["antlr_fail_syside_pass"]])
        writer.writerow(["pass", "fail", counts["antlr_pass_syside_fail"]])
        writer.writerow(["pass", "pass", counts["antlr_pass_syside_pass"]])


# Print the rebuilt counts so the user can confirm they match Figure 7.
def print_summary(counts: dict[str, int]) -> None:
    total_cases = sum(counts.values())
    print(f"Scanned initial candidates: {total_cases}")
    print(f"ANTLR fail, SysIDE fail: {counts['antlr_fail_syside_fail']}")
    print(f"ANTLR fail, SysIDE pass: {counts['antlr_fail_syside_pass']}")
    print(f"ANTLR pass, SysIDE fail: {counts['antlr_pass_syside_fail']}")
    print(f"ANTLR pass, SysIDE pass: {counts['antlr_pass_syside_pass']}")


# Rebuild the local Figure 7 audit and confusion-matrix CSVs from the release corpus.
def main() -> None:
    items = find_initial_candidates(TRAJECTORY_ROOT)
    rows = build_audit_rows(items)
    counts = count_confusion_matrix(rows)
    write_audit_csv(rows, AUDIT_CSV)
    write_counts_csv(counts, COUNTS_CSV)
    print_summary(counts)


if __name__ == "__main__":
    main()
