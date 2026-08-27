# TPC-282 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T282.1 | `C=<w_perp,S>` is the actual projected source attachment | `PROVED_EXACT_FINITE` | declared finite projection and source model |
| T282.2 | `C` is sign-separated on every registered row | `NUMERICALLY_CERTIFIED` | 12 rows: 11 negative, 1 positive |
| T282.3 | `W,Y>0` and `0<C^2/(WY)<1` | `NUMERICALLY_CERTIFIED` | same 12 rows |
| T282.4 | uniform asymptotic source nondegeneracy | `OPEN` | no growing theorem supplied |
| T282.5 | literal arithmetic `L2` estimate | `OPEN` | independent missing gate |

```text
STRONGEST_POSITIVE_RESULT = ACTUAL_LITERAL_SOURCE_ATTACHMENT_LOCKED_AND_NONZERO_ON_12_ROWS
STRONGEST_OBSTRUCTION = WEAKEST_RHO_SQUARED_IS_ABOUT_3.36E-5_AND_SIGN_FLIPS
OPEN_THEOREM = UNIFORM_ASYMPTOTIC_SOURCE_ATTACHMENT_NONDEGENERACY
REUSABLE_STRUCTURE = PROJECT_SOURCE_AND_OUTPUT -> C,W,Y -> NORMALIZED_ATTACHMENT
ROUND2_CLUE = QUANTIFY_SOURCE_ATTACHMENT_STABILITY_RADIUS_AND_SIGN_FLIPS
```
