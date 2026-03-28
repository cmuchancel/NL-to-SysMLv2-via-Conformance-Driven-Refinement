# Primary Outcome: Production Conformance

This folder supports Section 4.1 of the paper. It contains the script and saved output used to verify the overall single-shot and final pipeline production-conformance rates.

## Files

- `primary_outcome_stats.py`
- `primary_outcome_stats_output.txt`

## Data Source

The script reads:

- `../Open-Source Dataset Release/604 positive artifacts/`

Each `.sysml` file in that folder is a final successful case. Files named `iteration_00.sysml` correspond to cases that succeeded on the initial generation.

## Output

The script reports:

- total prompt-model cases
- single-shot production conformance
- final pipeline production conformance

## Run

From the repository root:

```bash
python3 'Primary Outcome: Production Conformance/primary_outcome_stats.py'
```
