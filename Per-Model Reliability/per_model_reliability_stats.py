#!/usr/bin/env python3
"""Compute the Section 4.2 per-model reliability summary from the public release package."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOT = REPO_ROOT / "Open-Source Dataset Release" / "604 positive artifacts"
MODEL_ORDER = [
    ("anthropic", "Sonnet"),
    ("openai", "OpenAI"),
    ("deepseek_reasoner", "DeepSeek"),
    ("mistral_large", "Mistral"),
]


# Convert a fraction to a percentage while guarding against divide-by-zero.
def percent(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else 100.0 * numerator / denominator


# Build the path to one model's folder and make sure it exists.
def get_model_folder(scan_root: Path, provider_name: str) -> Path:
    model_folder = scan_root / provider_name
    if not model_folder.exists():
        raise SystemExit(f"Folder not found: {model_folder}")
    return model_folder


# Load all final successful SysML files for one model.
def load_successful_models(model_folder: Path) -> list[Path]:
    sysml_files = sorted(model_folder.rglob("*.sysml"))
    if not sysml_files:
        raise SystemExit(f"No .sysml files found under: {model_folder}")
    return sysml_files


# Count how many cases for one model succeeded on the very first attempt.
def count_single_shot_successes(sysml_files: list[Path]) -> int:
    return sum(path.name == "iteration_00.sysml" for path in sysml_files)


# Print the Figure 4 stats for each model.
def print_per_model_summary(scan_root: Path) -> None:
    print(f"Scanning: {scan_root.name}")
    print()

    for provider_name, model_label in MODEL_ORDER:
        model_folder = get_model_folder(scan_root, provider_name)
        sysml_files = load_successful_models(model_folder)
        total_cases = len(sysml_files)
        single_shot_cases = count_single_shot_successes(sysml_files)

        print(f"{model_label}:")
        print(f"  Total prompt-level cases: {total_cases}")
        print(
            f"  Single-shot production conformance: "
            f"{single_shot_cases}/{total_cases} "
            f"({percent(single_shot_cases, total_cases):.2f}%)"
        )
        print(
            f"  Final pipeline production conformance: "
            f"{total_cases}/{total_cases} "
            f"({percent(total_cases, total_cases):.2f}%)"
        )
        print()


# Run the minimal load-and-report flow for the per-model reliability summary.
def main() -> None:
    print_per_model_summary(SCAN_ROOT)


if __name__ == "__main__":
    main()
