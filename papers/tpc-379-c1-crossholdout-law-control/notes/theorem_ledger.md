# TPC-379 theorem ledger

| ID | Statement | Status |
|---|---|---|
| T379-T1 | The affine-grid selection and four-law panel are finite, literal, and response-blind. | `PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND` |
| T379-T2 | Current intervals are disjoint from the largest declared TPC-376--378 intervals. | `PROVED_EXACT_FINITE` |
| T379-T3 | The square-energy geometry is common to all laws and the q=8 rational anchor is positive and symmetric. | `PROVED_EXACT_FINITE_LAW_INDEPENDENT` |
| T379-T4 | The four sign vectors and common c=1 band/tail mask are fixed before metric readout. | `PROVED_EXACT_FINITE_PREDECLARED` |
| T379-T5 | The complete 36-row panel has profiles `(0,3,3)`, `(0,0,0)`, `(0,0,0)`, `(0,0,0)` in the declared law order. | `NUMERICALLY_CERTIFIED_FINITE_SCOPED` |
| T379-T6 | The all-plus high-Q failure profile is invariant across the three signed controls. | `REFUTED_SCOPED` |
| T379-T7 | Any sign law is uniformly controlled over origins or growing windows. | `OPEN` |
| T379-T8 | The common finite normalization is source-valid for the arithmetic target. | `MODELING_CHOICE_OPEN` |
| T379-T9 | A growing c=1 operator bound or source-uniform arithmetic L2 estimate follows. | `OPEN` |
| T379-T10 | An arithmetic power saving, Route-B reassembly, or twin-prime conclusion follows. | `NO` / `NONE` |

## Reusable structure

The common-geometry, common-mask law-control panel, exact rational anchor,
reverse-shell replay, and full-mode band/tail Rayleigh certificate form a
reusable finite obstruction template.

## ROUND2_CLUE

`TEST_C1_LAW_CONTROL_COUNT_REPLAY`.
