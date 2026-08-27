# TPC-273 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T273.1 | `m^2=rho^2` and `m^6=(rho^2)^3` | PROVED_EXACT_FINITE | positive parent rows |
| T273.2 | 32-row margin classification: 12 low, 11 middle, 9 high | NUMERICALLY_CERTIFIED | declared grid |
| T273.3 | cutoff-only `N64: z=2->5` crosses middle to `m>1/4` | NUMERICALLY_CERTIFIED | finite transition |
| T273.4 | cutoff-only `N128: z=2->3` crosses middle to `m<1/8` | NUMERICALLY_CERTIFIED | finite transition |
| T273.5 | phase census is 30 negative and 2 positive | NUMERICALLY_CERTIFIED | declared grid |
| T273.6 | uniform stability of the declared finite family | REFUTED_SCOPED | not an asymptotic counterexample |
| T273.7 | source-level growing margin uniformity | OPEN | no theorem supplied |

```text
STRONGEST_POSITIVE_RESULT = 32_ROW_OUTWARD_MARGIN_AND_PHASE_MATRIX
STRONGEST_OBSTRUCTION = CUTOFF_ONLY_MARGIN_BAND_FLIPS_AT_FIXED_SCALE
OPEN_THEOREM = GROWING_CUTOFF_MARGIN_UNIFORMITY_FOR_LITERAL_V59
REUSABLE_STRUCTURE = PARENT_RHO2 -> MARGIN2 -> THRESHOLD_MATRIX -> STABILITY_TEST
ROUND2_CLUE = TEST_SOURCE_LEVEL_MARGIN_UNIFORMITY_ON_THE_LITERAL_GROWING_CUTOFF
```
