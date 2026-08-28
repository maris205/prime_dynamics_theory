# TPC-290 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T290.1 | weighted Gram/Rayleigh identity | `PROVED_EXACT` | every finite vector family |
| T290.2 | nonnegative weights plus nonnegative cross terms imply `R>=1` | `PROVED_EXACT` | finite Gram |
| T290.3 | coherence and diagonal balance imply effective-support lower bound | `PROVED_EXACT_CONDITIONAL` | positive coherence block |
| T290.4 | 54 declared full-support policy rows are amplified | `NUMERICALLY_CERTIFIED_FINITE` | TPC-289 grid |
| T290.5 | three equal-pair subunit witnesses | `NUMERICALLY_CERTIFIED_FINITE_OBSTRUCTION` | one early row |
| T290.6 | leave-one-out uniform supports remain amplified | `NUMERICALLY_CERTIFIED_FINITE` | 18 rows |
| T290.7 | growing diffuse weighted theorem | `OPEN` | no asymptotic source theorem |

```text
STRONGEST_POSITIVE_RESULT = EXACT_EFFECTIVE_SUPPORT_COHERENCE_ENVELOPE
STRONGEST_OBSTRUCTION = SPARSE_NONNEGATIVE_SIGN_FLIP_ESCAPE
OPEN_THEOREM = GROWING_DIFFUSE_WEIGHTED_COHERENCE_OR_SOURCE_RESTRICTION
REUSABLE_STRUCTURE = WEIGHTED_GRAM -> EFFECTIVE_SUPPORT -> POSITIVE BLOCK / SPARSE ESCAPE
ROUND2_CLUE = TEST_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_OR_SOURCE_RESTRICTED_DIFFUSE_WEIGHTS
```
