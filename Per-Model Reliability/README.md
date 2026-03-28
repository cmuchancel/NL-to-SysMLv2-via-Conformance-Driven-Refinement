# Per-Model Reliability

This folder supports Section 4.2 of the paper. It contains the script and saved output used to verify the per-model single-shot and final pipeline production-conformance rates.

## Files

- `per_model_reliability_stats.py`
- `per_model_reliability_stats_output.txt`

## Data Source

The script reads:

- `../Open-Source Dataset Release/604 positive artifacts/`

Each provider subfolder contains the final successful cases for one model. Files named `iteration_00.sysml` correspond to cases that succeeded on the initial generation.

## Output

The script reports, for each model:

- total prompt-model cases
- single-shot production conformance
- final pipeline production conformance

## Run

From the repository root:

```bash
python3 'Per-Model Reliability/per_model_reliability_stats.py'
```
