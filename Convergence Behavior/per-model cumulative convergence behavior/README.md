# Per-Model Cumulative Convergence Behavior

This folder supports the per-model cumulative convergence analysis in Section 4.3 of the paper. It contains the script and saved output used for Figure 6.

## Files

- `per_model_cumulative_convergence_stats.py`
- `per_model_cumulative_convergence_stats_output.txt`

## Data Source

The script reads:

- `../../Open-Source Dataset Release/604 positive artifacts/`

Each provider subfolder contains the final successful cases for one model, and the final filename indicates the repair cycle at which first production conformance was reached.

## Output

The script reports:

- per-model cumulative acceptance by repair cycle

## Run

From the repository root:

```bash
python3 'Convergence Behavior/per-model cumulative convergence behavior/per_model_cumulative_convergence_stats.py'
```
