# Appendix A: Auxiliary Demonstration: Grammar Parsability vs. Production Conformance

This folder supports Appendix A of the paper. It contains the ten curated examples, the ANTLR and SysIDE checks, and the saved outputs for the auxiliary demonstration.

## Files

- `auxiliary_demonstration.tex`
- `examples/mismatch_10_distinct/`
- `antlr_check.py`
- `syside_check.py`
- `run_experiment.py`
- `results/table_2.csv`
- `results/summary.md`

## Runtime Assets

- `generated/hamr_java_classes/`
- `tools/antlr-4.13.2-complete.jar`

## Reported Result

For the ten curated examples:

- `10/10` pass ANTLR parsing
- `0/10` pass production conformance

## Prerequisites

- Python 3.10+
- Java 17+
- SysIDE available as `syside check` or through a Python module entry point

## Run

From the repository root:

```bash
python3 'Appendix A - Auxiliary Demonstration - Grammar Parsability vs. Production Conformance/run_experiment.py'
```
