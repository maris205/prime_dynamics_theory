# TPC-299 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T299.1 | `B_{k,tau}(b)=min{c^T M_kc:||V_kc-b||<=tau||b||}` has the KKT/ridge frontier | `PROVED_EXACT_FINITE` | positive-definite finite source Gram |
| T299.2 | budget feasibility is equivalent to `B >= B_{k,tau}(b)` | `PROVED_EXACT_FINITE` | same finite profile prefix |
| T299.3 | nested source prefixes have nonincreasing budget frontiers | `PROVED_EXACT_FINITE` | finite nested literal ladder |
| T299.4 | weighted half-RMS budget exceeds `9e-5||beta||^2` on 18/18 rows | `NUMERICALLY_CERTIFIED_FINITE` | 18 rows, 1,380 shell edges |
| T299.5 | weighted half-RMS budget exceeds `1e-3||beta||^2` on 14/18 threshold prefixes | `NUMERICALLY_CERTIFIED_FINITE` | declared finite normalization |
| T299.6 | even the full available prefix exceeds `1e-3||beta||^2` on 11/18 rows | `NUMERICALLY_CERTIFIED_FINITE` | same 17-profile ladder |
| T299.7 | positive half-RMS budget is below `1e-4||beta||^2` on 18/18 rows | `NUMERICALLY_CERTIFIED_FINITE` | positive control |
| T299.8 | weighted/positive threshold-budget ratio exceeds 20 on 18/18 rows | `NUMERICALLY_CERTIFIED_FINITE` | comparative finite diagnostic |
| T299.9 | arithmetic `L2`, moving-shell budget bounds, Gate B, and twin-prime endpoint | `OPEN/NONE` | outside finite audit |
