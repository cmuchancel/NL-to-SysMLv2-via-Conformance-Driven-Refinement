#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
EXAMPLES_DIR = SCRIPT_DIR / "examples" / "mismatch_10_distinct"
RESULTS_DIR = SCRIPT_DIR / "results"
TABLE_2_CSV = RESULTS_DIR / "table_2.csv"
SUMMARY_MD = RESULTS_DIR / "summary.md"
ANTLR_CHECK = SCRIPT_DIR / "antlr_check.py"
SYSIDE_CHECK = SCRIPT_DIR / "syside_check.py"

EXAMPLES = [
    ("01", "01_missing_import_namespace.sysml", "Missing imported namespace"),
    ("02", "02_missing_port_type.sysml", "Missing port type"),
    ("03", "03_missing_attribute_type.sysml", "Missing attribute type"),
    ("04", "04_missing_specialization_base.sysml", "Missing specialization base"),
    ("05", "05_attribute_definition_nonreferential_feature.sysml", "Action typed by undefined behavior type"),
    ("06", "06_invocation_not_behavior.sysml", "Invocation target is not a behavior"),
    ("07", "07_missing_feature_in_expression.sysml", "Missing referenced feature in expression"),
    ("08", "08_missing_root_qualified_namespace.sysml", "Missing root-qualified namespace"),
    ("09", "09_redefine_missing_feature.sysml", "Redefinition of missing feature"),
    ("10", "10_missing_namespace_in_type_use.sysml", "Missing namespace in type use"),
]


# Run a subprocess and capture its text output.
def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True)


# Strip ANSI noise and local absolute paths out of checker output.
def clean_output(text: str, example: Path) -> list[str]:
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    cleaned = ansi_escape.sub("", text)
    cleaned = cleaned.replace(str(example), f"examples/mismatch_10_distinct/{example.name}")
    cleaned = cleaned.replace(f"{WORKSPACE_ROOT}/", "")
    return [line.rstrip() for line in cleaned.splitlines() if line.strip()]


# Pull the first concrete SysIDE error line from checker output.
def first_error_line(lines: list[str]) -> str:
    for line in lines:
        if "error (" in line:
            return line.strip()
    return ""


# Map the raw SysIDE error family to the paper's shorter table wording.
def short_failure_label(error_line: str) -> str:
    match = re.search(r"error \(([^)]+)\):", error_line)
    if not match:
        return "Fail"

    family = match.group(1)
    if family == "reference-error":
        return "Fail (reference)"
    if family == "invocation-expression-instantiated-type":
        return "Fail (invocation)"
    return f"Fail ({family})"


# Run both checkers for one appendix example and store the paper-facing result.
def run_one(example_id: str, filename: str, condition: str) -> dict[str, str]:
    example = EXAMPLES_DIR / filename
    if not example.exists():
        raise SystemExit(f"Missing example file: {example}")

    antlr_cp = run_cmd([sys.executable, str(ANTLR_CHECK), str(example)])
    syside_cp = run_cmd([sys.executable, str(SYSIDE_CHECK), str(example)])

    antlr = "Pass" if antlr_cp.returncode == 0 else "Fail"
    syside = "Pass" if syside_cp.returncode == 0 else "Fail"

    syside_text = (syside_cp.stdout or "") + (("\n" + syside_cp.stderr) if syside_cp.stderr else "")
    syside_lines = clean_output(syside_text, example)
    error_line = first_error_line(syside_lines)

    if syside == "Fail":
        syside = short_failure_label(error_line)

    return {
        "ID": example_id,
        "Injected Condition": condition,
        "ANTLR": antlr,
        "SysIDE": syside,
        "Example": filename,
        "Diagnostic": error_line,
    }


# Write the exact table data behind Table 2.
def write_table_2(rows: list[dict[str, str]]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with TABLE_2_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Injected Condition", "ANTLR", "SysIDE"])
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in writer.fieldnames})


# Write a short human-readable summary of the auxiliary demonstration.
def write_summary(rows: list[dict[str, str]]) -> None:
    antlr_pass = sum(row["ANTLR"] == "Pass" for row in rows)
    syside_pass = sum(row["SysIDE"] == "Pass" for row in rows)
    mismatches = sum(row["ANTLR"] == "Pass" and row["SysIDE"] != "Pass" for row in rows)
    reference_fails = sum(row["SysIDE"] == "Fail (reference)" for row in rows)
    invocation_fails = sum(row["SysIDE"] == "Fail (invocation)" for row in rows)
    concrete_example = next(row for row in rows if row["ID"] == "07")

    lines = [
        "# Auxiliary Demonstration Summary",
        "",
        f"- Total examples: {len(rows)}",
        f"- ANTLR parse pass: {antlr_pass}/{len(rows)}",
        f"- SysIDE production conformance pass: {syside_pass}/{len(rows)}",
        f"- Mismatch count (ANTLR pass, SysIDE fail): {mismatches}/{len(rows)}",
        f"- Failure family breakdown: {reference_fails} reference, {invocation_fails} invocation",
        "",
        "## Concrete Example",
        f"- Example: `{concrete_example['Example']}`",
        f"- ANTLR: {concrete_example['ANTLR']}",
        f"- SysIDE: {concrete_example['SysIDE']}",
        f"- Diagnostic: {concrete_example['Diagnostic']}",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


# Run the fixed ten-case appendix demonstration and refresh the two result files.
def main() -> None:
    rows = [run_one(example_id, filename, condition) for example_id, filename, condition in EXAMPLES]
    write_table_2(rows)
    write_summary(rows)
    print(f"Wrote: {TABLE_2_CSV}")
    print(f"Wrote: {SUMMARY_MD}")


if __name__ == "__main__":
    main()
