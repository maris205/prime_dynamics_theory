# TPC-301 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T301.1 | Budget feasible sets are nested in tolerance | PROVED_EXACT_FINITE | fixed finite prefix |
| T301.2 | Relative budget is homogeneous of degree two in the target | PROVED_EXACT_FINITE | nonzero scalar target |
| T301.3 | First feasible prefix is nonincreasing under relaxed tolerance | PROVED_EXACT_FINITE | nested literal prefixes |
| T301.4 | A target-independent common-prefix normalizer cancels from the gap | PROVED_EXACT_FINITE | positive scalar normalizer |
| T301.5 | 324 frontier cases replay within published intervals | NUMERICALLY_CERTIFIED_FINITE | 18 rows, 3 tolerances, 3 contexts, 2 targets |
| T301.6 | Common weighted/positive gap exceeds 10 in every row and tolerance | NUMERICALLY_CERTIFIED_FINITE | 54 cases |
| T301.7 | Common weighted budget exceeds 3e-5 under each normalizer in 54/54 cases | NUMERICALLY_CERTIFIED_FINITE | three declared normalizers |
| T301.8 | Full-prefix budgets are monotone over the tolerance ladder | NUMERICALLY_CERTIFIED_FINITE | 36 target-row checks |
| T301.9 | Growing budget and arithmetic L2 remain open | OPEN | outside finite audit |
