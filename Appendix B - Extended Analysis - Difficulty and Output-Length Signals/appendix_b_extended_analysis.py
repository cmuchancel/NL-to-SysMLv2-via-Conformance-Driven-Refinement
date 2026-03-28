#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "data"
RESULTS_DIR = SCRIPT_DIR / "results"

DIFFICULTY_INPUT = DATA_DIR / "difficulty_iterations.csv"
OUTPUT_LENGTH_INPUT = DATA_DIR / "generated_output_length_vs_iterations.csv"

FIGURE_8_MODEL_SUMMARY = RESULTS_DIR / "figure_8_difficulty_by_model.csv"
FIGURE_8_POOLED_SUMMARY = RESULTS_DIR / "figure_8_pooled_by_difficulty.csv"
FIGURE_9_FIT_SUMMARY = RESULTS_DIR / "figure_9_fit.csv"
FIGURE_9_MODEL_SUMMARY = RESULTS_DIR / "figure_9_output_length_by_model.csv"

MODEL_ORDER_FULL = [
    "OpenAI Codex 5.2",
    "Anthropic Claude Sonnet 4.6",
    "DeepSeek Reasoner",
    "Mistral Large",
]

MODEL_ORDER_SHORT = ["OpenAI", "Anthropic", "DeepSeek", "Mistral"]


# Load the local Appendix B difficulty dataset.
def load_difficulty_data() -> pd.DataFrame:
    data = pd.read_csv(DIFFICULTY_INPUT)
    data["prompt_id"] = pd.to_numeric(data["prompt_id"], errors="raise").astype(int)
    data["difficulty"] = pd.to_numeric(data["difficulty"], errors="raise").astype(int)
    data["iterations_to_success"] = pd.to_numeric(data["iterations_to_success"], errors="raise")
    return data


# Load the local Appendix B output-length dataset.
def load_output_length_data() -> pd.DataFrame:
    data = pd.read_csv(OUTPUT_LENGTH_INPUT)
    data["iterations_to_converge"] = pd.to_numeric(data["iterations_to_converge"], errors="raise")
    data["sysml_line_count"] = pd.to_numeric(data["sysml_line_count"], errors="raise")
    return data


# Compute the per-model and pooled summaries used in Figure 8.
def summarize_difficulty(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, float, float, float]:
    by_model = (
        data.groupby(["model_label", "difficulty"], as_index=False)
        .agg(
            n_cases=("iterations_to_success", "size"),
            mean_iterations_to_success=("iterations_to_success", "mean"),
        )
    )

    pooled = (
        data.groupby("difficulty", as_index=False)
        .agg(
            n_prompts=("prompt_id", "nunique"),
            n_cases=("iterations_to_success", "size"),
            mean_iterations_to_success=("iterations_to_success", "mean"),
            std_iterations_to_success=("iterations_to_success", "std"),
        )
    )
    pooled["se_iterations_to_success"] = (
        pooled["std_iterations_to_success"] / np.sqrt(pooled["n_cases"])
    )

    x = pooled["difficulty"].to_numpy(dtype=float)
    y = pooled["mean_iterations_to_success"].to_numpy(dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    y_hat = slope * x + intercept
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - (ss_res / ss_tot)

    return by_model, pooled, float(slope), float(intercept), float(r2)


# Compute the summaries used in Figure 9.
def summarize_output_length(data: pd.DataFrame) -> tuple[pd.DataFrame, float, float, float]:
    x = data["sysml_line_count"].to_numpy(dtype=float)
    y = data["iterations_to_converge"].to_numpy(dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    y_hat = slope * x + intercept
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - (ss_res / ss_tot)

    by_model = (
        data.groupby("model_label", as_index=False)
        .agg(
            mean=("sysml_line_count", "mean"),
            std=("sysml_line_count", "std"),
            count=("sysml_line_count", "size"),
        )
    )
    by_model["se"] = by_model["std"] / np.sqrt(by_model["count"])
    by_model["model_label"] = pd.Categorical(by_model["model_label"], MODEL_ORDER_SHORT, ordered=True)
    by_model = by_model.sort_values("model_label").reset_index(drop=True)

    return by_model, float(slope), float(intercept), float(r2)


# Print the Appendix B statistics in paper-facing form.
def print_summary(
    pooled_difficulty: pd.DataFrame,
    difficulty_slope: float,
    difficulty_intercept: float,
    difficulty_r2: float,
    output_length_by_model: pd.DataFrame,
    output_length_slope: float,
    output_length_intercept: float,
    output_length_r2: float,
) -> None:
    print("Scanning: difficulty_iterations.csv and generated_output_length_vs_iterations.csv")
    print()
    print("B.1 SysMBench difficulty versus iterations-to-success")
    for row in pooled_difficulty.itertuples(index=False):
        print(
            f"Difficulty {int(row.difficulty)}: "
            f"{int(row.n_prompts)} prompts, {int(row.n_cases)} cases, "
            f"pooled mean {row.mean_iterations_to_success:.3f}"
        )
    print(
        f"Pooled linear fit: y = {difficulty_slope:.3f}x + {difficulty_intercept:.3f}, "
        f"R^2 = {difficulty_r2:.3f}"
    )
    print()
    print("B.2 Generated output length versus iterations-to-converge")
    print(
        f"Pooled linear fit: y = {output_length_slope:.5f}x + {output_length_intercept:.3f}, "
        f"R^2 = {output_length_r2:.4f}"
    )
    print("Average generated SysML lines by model:")
    for row in output_length_by_model.itertuples(index=False):
        print(
            f"{row.model_label}: {float(row.mean):.1f} "
            f"(SE {float(row.se):.1f}, n={int(row.count)})"
        )


# Build the local summary tables and paper-facing output for Appendix B.
def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    difficulty_data = load_difficulty_data()
    by_model_difficulty, pooled_difficulty, difficulty_slope, difficulty_intercept, difficulty_r2 = summarize_difficulty(difficulty_data)
    by_model_difficulty.to_csv(FIGURE_8_MODEL_SUMMARY, index=False)
    pooled_difficulty.to_csv(FIGURE_8_POOLED_SUMMARY, index=False)

    output_length_data = load_output_length_data()
    by_model_output_length, output_length_slope, output_length_intercept, output_length_r2 = summarize_output_length(output_length_data)
    by_model_output_length.to_csv(FIGURE_9_MODEL_SUMMARY, index=False)
    pd.DataFrame(
        [
            {
                "n_points": int(len(output_length_data)),
                "linear_slope": output_length_slope,
                "linear_intercept": output_length_intercept,
                "linear_r2": output_length_r2,
            }
        ]
    ).to_csv(FIGURE_9_FIT_SUMMARY, index=False)

    print_summary(
        pooled_difficulty,
        difficulty_slope,
        difficulty_intercept,
        difficulty_r2,
        by_model_output_length,
        output_length_slope,
        output_length_intercept,
        output_length_r2,
    )


if __name__ == "__main__":
    main()
