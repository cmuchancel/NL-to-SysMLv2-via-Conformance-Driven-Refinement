# Natural-Language to SysMLv2 Translation via Conformance-Driven Iterative Refinement

This repository is the paper companion repo. It contains the final paper PDF, the public dataset release, and the standalone folders used to verify the paper's reported results.

## Start Here

- `final_paper.pdf`
  The final paper PDF.

- `Open-Source Dataset Release/`
  The released dataset package, including positive artifacts, negative artifacts, the full trajectory-level corpus, and run-level token-usage records.

- `Open-Source Dataset Release/token_usage_by_run.csv`
  Provider-reported token usage for all 604 prompt--model runs. Token metadata are available for 603 runs; the unavailable Mistral prompt 107 record is retained with blank token fields and an explicit availability flag.

- Main results folders:
  - `Primary Outcome: Production Conformance/`
  - `Per-Model Reliability/`
  - `Convergence Behavior/`
  - `Statistical Reliability/`
  - `Grammar Validity vs. Production Conformance/`

- Appendix folders:
  - `Appendix A - Auxiliary Demonstration - Grammar Parsability vs. Production Conformance/`
  - `Appendix B - Extended Analysis - Difficulty and Output-Length Signals/`
  - `Appendix C - Extended Analysis - Classifying Repair Attempts on Persistent Errors/`

## How To Use It

- Read `final_paper.pdf` for the paper itself.
- Open the folder for the section or appendix you want to inspect.
- Each section folder includes its own README, local inputs, scripts, and saved outputs.
- The saved `.txt` and `.csv` files are included so the reported numbers can be checked directly.

## Repository Structure

The top-level folders are the intended entry points. The repo is organized by paper section so that each result area can be inspected on its own.
