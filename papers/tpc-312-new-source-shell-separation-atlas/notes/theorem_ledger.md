# TPC-312 theorem ledger

| ID | Statement | Status |
|---|---|---|
| T312-T1 | The source interval is exactly `{321,...,640}` and the four declared prime shells are disjoint finite sets | `PROVED_EXACT_FINITE` |
| T312-T2 | The physical output Gram identity implies positive semidefiniteness | `PROVED_EXACT_FINITE` |
| T312-T3 | Fixing the first sign to `+1` removes only the global-sign duplication | `PROVED_EXACT_FINITE` |
| T312-T4 | Reflected Gray traversal covers every sign class exactly once | `PROVED_EXACT_FINITE` |
| T312-T5 | All eight rational Grams have full rank certified modulo `1000000007` | `NUMERICALLY_CERTIFIED_FINITE` |
| T312-T6 | Every row has a unique minimum modulo global sign and a unique all-positive maximum | `NUMERICALLY_CERTIFIED_FINITE` |
| T312-T7 | Every row has minimum ratio `<1` and positive ratio `>1` | `NUMERICALLY_CERTIFIED_FINITE` |
| T312-T8 | Minimum ratios strictly descend and positive ratios strictly ascend along each Q spine | `PROVED_EXACT_FINITE` |
| T312-T9 | Exponent two strengthens both finite inequalities at every Q | `PROVED_EXACT_FINITE` |
| T312-T10 | The new panel establishes an external holdout, uniform budget, arithmetic L2, Gate B, or a twin-prime theorem | `OPEN` / `NONE` |

The exact-order labels refer only to the eight locked finite rows.  They do not
claim monotonicity for other shells or for a growing family.
