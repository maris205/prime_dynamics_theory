# TPC-292 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T292.1 | triangle sign parity criterion | `PROVED_EXACT_CONDITIONAL` | three nonzero real Gram edges |
| T292.2 | three-vector Schur projection identity | `PROVED_EXACT_FINITE` | positive two-vector minor |
| T292.3 | normalized Gram volume is nonnegative | `PROVED_EXACT_FROM_GRAM_PSD` | every Gram triple |
| T292.4 | complete three-prime atlas | `NUMERICALLY_CERTIFIED_FINITE` | 5,727 declared triples |
| T292.5 | frustration census 5,718/5,727 | `NUMERICALLY_CERTIFIED_FINITE` | frozen 18-row grid |
| T292.6 | growing-shell sign compatibility | `OPEN` | no asymptotic theorem |
| T292.7 | source-native signed reassembly and arithmetic L2 | `OPEN` | no certificate |

```text
STRONGEST_POSITIVE_RESULT = EXACT_TRIANGLE_PARITY_PLUS_THREE_VECTOR_SCHUR_COMPILER
STRONGEST_OBSTRUCTION = PAIRWISE SIGNED CANCELLATION IS GENERICALLY FRUSTRATED ON TRIANGLES
OPEN_THEOREM = GROWING_PRIME-SHELL COMPATIBILITY WITH SOURCE-NATIVE COEFFICIENTS
REUSABLE_STRUCTURE = SIGNED_GRAM_GRAPH -> CYCLE PARITY -> SCHUR RESIDUAL -> SOURCE TEST
ROUND2_CLUE = TEST_SIGNED_GRAPH_MAXCUT_AND_MULTI_PRIME_RAYLEIGH_COMPATIBILITY
```
