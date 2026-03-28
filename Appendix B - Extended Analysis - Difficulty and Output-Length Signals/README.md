# Appendix B: Extended Analysis: Difficulty and Output-Length Signals

This folder supports Appendix B of the paper. It contains the local data, script, and saved outputs used to verify the difficulty and generated-output-length analyses.

## Files

- `data/prompt_difficulty_levels.csv`
- `data/difficulty_iterations.csv`
- `data/generated_output_length_vs_iterations.csv`
- `appendix_b_extended_analysis.py`
- `appendix_b_stats_output.txt`
- `results/figure_8_difficulty_by_model.csv`
- `results/figure_8_pooled_by_difficulty.csv`
- `results/figure_9_fit.csv`
- `results/figure_9_output_length_by_model.csv`

## Coverage

- B.1 SysMBench difficulty versus iterations-to-success
- B.2 Generated output length versus iterations-to-converge

## Prerequisites

- Python 3.10+
- `pandas`
- `numpy`

## Run

From the repository root:

```bash
python3 'Appendix B - Extended Analysis - Difficulty and Output-Length Signals/appendix_b_extended_analysis.py' > 'Appendix B - Extended Analysis - Difficulty and Output-Length Signals/appendix_b_stats_output.txt'
```
