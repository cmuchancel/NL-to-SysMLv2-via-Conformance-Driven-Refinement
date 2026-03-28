# Grammar Validity vs. Production Conformance

This folder supports Section 4.5 of the paper. It contains the summary script, the local Figure 7 confusion-matrix data, and the checker assets needed to rebuild that data from the released trajectory corpus.

## Files

- `grammar_validity_vs_production_conformance_stats.py`
- `grammar_validity_vs_production_conformance_stats_output.txt`
- `build_figure_7_confusion_matrix.py`
- `data/figure_7_confusion_matrix.csv`
- `data/figure_7_first_iteration_audit.csv`

## Checker Assets

- `checkers/antlr_check.py`
- `checkers/syside_check.py`
- `checkers/generated/hamr_java_classes/`
- `checkers/tools/antlr-4.13.2-complete.jar`

## Data Sources

The summary script reads:

- `data/figure_7_confusion_matrix.csv`

The rebuild script reads:

- `../Open-Source Dataset Release/trajectory level corpus/`

## Output

The summary script reports:

- total initial candidates
- ANTLR grammar-pass count and percentage
- production-conformance pass count and percentage
- the four Figure 7 confusion-matrix cells
- the operational-gap percentages discussed in the paper

## Run

To regenerate the summary from the saved confusion matrix:

```bash
python3 'Grammar Validity vs. Production Conformance/grammar_validity_vs_production_conformance_stats.py'
```

To rebuild the confusion matrix from the released trajectory corpus:

```bash
python3 'Grammar Validity vs. Production Conformance/build_figure_7_confusion_matrix.py'
```
