# TPC-378 theorem ledger

| ID | Statement | Status |
|---|---|---|
| T378-T1 | The declared affine-grid selection is finite, literal, and response-blind. | `PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND` |
| T378-T2 | The current six endpoint intervals are disjoint from the inherited largest finite intervals. | `PROVED_EXACT_FINITE` |
| T378-T3 | Full-window square-energy geometry is nonnegative and the exact anchor is positive and symmetric. | `PROVED_EXACT_FINITE` |
| T378-T4 | The inherited c=1 band and tail satisfy the entrywise and selected-mode Rayleigh identities. | `PROVED_EXACT_FINITE` / `NUMERICALLY_CERTIFIED_FINITE_SCOPED` |
| T378-T5 | The complete 18-row panel has profile `(0,3,3)` at both counts. | `NUMERICALLY_CERTIFIED_FINITE_SCOPED` |
| T378-T6 | The parent profile transfers to this finite fresh-origin panel. | `NUMERICALLY_CERTIFIED_FINITE_SCOPED` |
| T378-T7 | The profile is uniform over all origins or all growing windows. | `OPEN` |
| T378-T8 | The normalization is a source-valid physical normalization for the arithmetic target. | `MODELING_CHOICE_OPEN` |
| T378-T9 | A growing c=1 operator bound or source-uniform arithmetic L2 estimate follows. | `OPEN` |
| T378-T10 | Any arithmetic power saving, Route-B reassembly, or twin-prime conclusion follows. | `NO` / `NONE` |

## Reusable structure

The response-blind affine-grid selector, exact coordinate-disjointness audit,
inherited c=1 mask, nested endpoint relation, and full-mode band/tail
certificate form a reusable finite cross-holdout template.

## ROUND2_CLUE

`TEST_C1_CROSSHOLDOUT_LAW_CONTROL`.
