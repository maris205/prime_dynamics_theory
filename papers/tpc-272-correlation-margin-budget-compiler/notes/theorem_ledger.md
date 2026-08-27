# TPC-272 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T272.1 | `m^6=Xi_C/Xi` and `Xi/Xi_C=m^(-6)` | PROVED_EXACT_FINITE | positive finite rows |
| T272.2 | scalar saving `sigma` plus margin loss `eta` gives endpoint saving `sigma-eta` | PROVED_CONDITIONAL | growing quantities satisfying stated hypotheses |
| T272.3 | strict target payment is `sigma-eta>1/400` | PROVED_CONDITIONAL | `E0=5/3`, `E*=1997/1200` |
| T272.4 | negative phase sign alone permits every `0<m<=1` | PROVED_EXACT | two-dimensional witness |
| T272.5 | nine finite margin intervals and four dyadic ratios | NUMERICALLY_CERTIFIED | TPC-271 parent registry |
| T272.6 | `96->192` margin sixth-power ratio `<(1/32)^6` with phase preserved | NUMERICALLY_CERTIFIED | one finite pair |
| T272.7 | source-level margin lower bound for literal V59 | OPEN | no asymptotic estimate |

```text
STRONGEST_POSITIVE_RESULT = CONDITIONAL_SIGMA_MINUS_ETA_ENDPOINT_COMPILER
STRONGEST_OBSTRUCTION = SIGN_ONLY_PHASE_DOES_NOT_LOWER_BOUND_MARGIN
OPEN_THEOREM = SOURCE_LEVEL_MARGIN_LOWER_BOUND_COUPLED_TO_SIGNED_SCALAR
REUSABLE_STRUCTURE = Xi_C/Xi -> m^6 -> MARGIN_LOSS -> ENDPOINT_BUDGET
ROUND2_CLUE = AUDIT_SOURCE_LEVEL_MARGIN_LOWER_BOUND_BEFORE_ANY_PHASE_PROMOTION
```
