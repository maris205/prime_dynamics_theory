# TPC-283 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T283.1 | nearest zero-attachment point is `w-(C/Y)S` | `PROVED_EXACT` | nonzero Hilbert-space signal |
| T283.2 | relative squared distance is `C^2/(WY)` | `PROVED_EXACT` | `W,Y>0` |
| T283.3 | all 12 parent rows have radius `<3/10` | `NUMERICALLY_CERTIFIED` | finite source-lock transfer |
| T283.4 | six parent rows have radius `<1/10` | `NUMERICALLY_CERTIFIED` | finite source-lock transfer |
| T283.5 | unrestricted zeroing perturbation is physically admissible | `OPEN` | literal source class not characterized |

```text
STRONGEST_POSITIVE_RESULT = EXACT_ZEROING_RADIUS_FORMULA_AND_12_ROW_TRANSFER
STRONGEST_OBSTRUCTION = EVERY_ROW_IS_ZEROABLE_WITHIN_30_PERCENT_SOURCE_NORM
OPEN_THEOREM = ADMISSIBLE_LITERAL_SOURCE_STABILITY_CLASS
REUSABLE_STRUCTURE = ATTACHMENT_C -> HYPERPLANE_DISTANCE -> RADIUS_BUDGET
ROUND2_CLUE = TEST_ADMISSIBLE_LITERAL_SOURCE_CONTROLS_AFTER_UNRESTRICTED_ZEROING_OBSTRUCTION
```
