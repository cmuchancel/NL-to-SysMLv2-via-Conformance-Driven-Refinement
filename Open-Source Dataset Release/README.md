# Open-Source Dataset Release

This folder provides the public dataset release referenced in Section 4.7 of the paper.

## Contents

- `151 SysMBench natural language prompts/`
  The released prompt set used in the evaluation campaign.

- `604 positive artifacts/`
  The final production-conforming artifacts, grouped by provider and prompt ID.

- `439 negative artifacts/`
  The failed intermediate artifacts, grouped by provider and prompt ID.

- `trajectory level corpus/`
  The full stored iteration corpus, with generated SysMLv2 text and paired diagnostics for each step.

## Counts

- positive artifacts: 604
- negative artifacts: 439
- total trajectory iterations: 1043

Iteration labels in this release are zero-based, so the first attempt is `iteration_00`.
