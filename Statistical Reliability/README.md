# Statistical Reliability

This folder supports Section 4.4 of the paper. It contains the script and saved output used to verify the statistical reliability calculations for the all-success pipeline result.

## Files

- `statistical_reliability_stats.py`
- `statistical_reliability_stats_output.txt`

## Data Source

The script reads:

- `../Open-Source Dataset Release/604 positive artifacts/`

That folder provides the final successful cases used to determine the sample size and single-shot count reported in the section.

## Output

The script reports:

- total prompt-model cases
- single-shot production conformance
- final pipeline production conformance
- the exact one-sided lower bound on convergence probability
- the exact one-sided upper bound on failure probability
- the large-sample approximation reported in the paper

## Run

From the repository root:

```bash
python3 'Statistical Reliability/statistical_reliability_stats.py'
```
