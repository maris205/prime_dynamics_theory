# TPC-291 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T291.1 | exact two-prime Schur projection identity | `PROVED_EXACT` | every nonzero vector pair |
| T291.2 | Schur residual is nonnegative | `PROVED_EXACT_FROM_CAUCHY` | every Gram pair |
| T291.3 | signed two-vector Rayleigh minimum | `PROVED_EXACT` | two-dimensional span |
| T291.4 | complete finite coherence-to-cancellation atlas | `NUMERICALLY_CERTIFIED_FINITE` | 1,380 pairs |
| T291.5 | low-residual counts `1074/852/477` | `NUMERICALLY_CERTIFIED_FINITE` | declared grid |
| T291.6 | sign-cost census `1377/3` | `NUMERICALLY_CERTIFIED_FINITE` | positive/negative pairs |
| T291.7 | multi-prime signed reassembly | `OPEN` | no theorem |

```text
STRONGEST_POSITIVE_RESULT = EXACT_SCHUR_RESIDUAL_AND_SIGNED_RAYLEIGH_COMPILER
STRONGEST_OBSTRUCTION = PAIRWISE_CANCELLATION_DOES_NOT_ASSEMBLE_ITSELF_INTO_FULL_SHELL
OPEN_THEOREM = MULTI_PRIME_SIGNED_REASSEMBLY_WITH_SOURCE_ARITHMETIC_L2
REUSABLE_STRUCTURE = COHERENCE -> SCHUR RESIDUAL -> COEFFICIENT SIGN COST -> REASSEMBLY TEST
ROUND2_CLUE = TEST_SOURCE_RESTRICTED_DIFFUSE_WEIGHTS_OR_MULTI_PRIME_SIGNED_NULL_DIRECTIONS
```
