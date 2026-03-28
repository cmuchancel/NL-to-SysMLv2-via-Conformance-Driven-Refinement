# Auxiliary Demonstration Summary

- Total examples: 10
- ANTLR parse pass: 10/10
- SysIDE production conformance pass: 0/10
- Mismatch count (ANTLR pass, SysIDE fail): 10/10
- Failure family breakdown: 9 reference, 1 invocation

## Concrete Example
- Example: `07_missing_feature_in_expression.sysml`
- ANTLR: Pass
- SysIDE: Fail (reference)
- Diagnostic: examples/mismatch_10_distinct/07_missing_feature_in_expression.sysml:13:68: error (reference-error): No Feature named 'height' found.