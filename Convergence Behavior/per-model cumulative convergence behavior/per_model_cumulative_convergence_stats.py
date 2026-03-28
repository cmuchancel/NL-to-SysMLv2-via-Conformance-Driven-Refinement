#!/usr/bin/env python3
"""Compute the Section 4.3 per-model cumulative convergence summary from the public release package."""

from __future__ import annotations

from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCAN_ROOT = REPO_ROOT / "Open-Source Dataset Release" / "604 positive artifacts"
MODEL_ORDER = [
    ("anthropic", "Anthropic Sonnet 4.6"),
    ("openai", "OpenAI Codex 5.2"),
    ("deepseek_reasoner", "DeepSeek Reasoner"),
    ("mistral_large", "Mistral Large"),
]
MAX_K = 7


# Convert a fraction to a percentage while guarding against divide-by-zero.
def percent(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else 100.0 * numerator / denominator


# Build the path to one model's folder and make sure it exists.
def get_model_folder(scan_root: Path, provider_name: str) -> Path:
    model_folder = scan_root / provider_name
    if not model_folder.exists():
        raise SystemExit(f"Folder not found: {model_folder}")
    return model_folder


# Load all successful final SysML files for one model.
def load_successful_models(model_folder: Path) -> list[Path]:
    sysml_files = sorted(model_folder.rglob("*.sysml"))
    if not sysml_files:
        raise SystemExit(f"No .sysml files found under: {model_folder}")
    return sysml_files


# Count how many cases for one model first conformed at each repair-cycle index k.
def count_cases_by_repair_cycle(sysml_files: list[Path]) -> Counter[int]:
    return Counter(int(path.stem.split("_")[1]) for path in sysml_files)


# Print the Figure 6 cumulative acceptance curve points for each model.
def print_per_model_cumulative_summary(scan_root: Path) -> None:
    print(f"Scanning: {scan_root.name}")
    print()

    for provider_name, model_label in MODEL_ORDER:
        model_folder = get_model_folder(scan_root, provider_name)
        sysml_files = load_successful_models(model_folder)
        counts_by_k = count_cases_by_repair_cycle(sysml_files)
        total_cases = len(sysml_files)

        print(f"{model_label}:")
        running_total = 0
        for k in range(MAX_K + 1):
            running_total += counts_by_k.get(k, 0)
            print(
                f"  k={k}: {running_total}/{total_cases} "
                f"({percent(running_total, total_cases):.2f}%)"
            )
        print()


# Run the minimal load-and-report flow for the Figure 6 summary.
def main() -> None:
    print_per_model_cumulative_summary(SCAN_ROOT)


if __name__ == "__main__":
    main()
