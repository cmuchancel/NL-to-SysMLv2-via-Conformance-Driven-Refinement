# Convergence Behavior

This folder supports the pooled convergence analysis in Section 4.3 of the paper. It contains the script and saved output used for Figure 5 and Table 1.

## Files

- `convergence_behavior_stats.py`
- `convergence_behavior_stats_output.txt`

## Data Source

The script reads:

- `../../Open-Source Dataset Release/604 positive artifacts/`

The final filename for each successful artifact, such as `iteration_00.sysml` or `iteration_03.sysml`, indicates the repair cycle at which first production conformance was reached.

## Output

The script reports:

- pooled cumulative acceptance by repair cycle
- grouped counts and shares for Table 1
- residual-mass contraction and threshold metrics
- summary statistics for repair cycles and total attempts to first conformance

## Run

From the repository root:

```bash
python3 'Convergence Behavior/cumulative convergence behavior/convergence_behavior_stats.py'
```
