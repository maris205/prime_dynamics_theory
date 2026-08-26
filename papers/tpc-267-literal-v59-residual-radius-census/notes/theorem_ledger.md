# TPC-267 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T267.1 | finite prime-shell/unit-mask operator is assembled with the literal signed centered kernel | `PROVED_EXACT_FINITE` | selected (N,H,Q,s) |
| T267.2 | four-block projection gives (C=C_3+C_\perp) with residual retained | `PROVED_EXACT_FINITE` | rank-three Haar span |
| T267.3 | Euler-product and logarithm interval enclosure is reproducible | `NUMERICALLY_CERTIFIED` | (P=50000), stated guards |
| T267.4 | twelve natural-clock rows satisfy (|C_\perp|/R<1/4) | `NUMERICALLY_CERTIFIED` | finite rows only |
| T267.5 | asymptotic V59 residual radius or uniform phase sector | `OPEN` | not supplied |
| T267.6 | arithmetic `L2`, full Gate B, twin-prime conclusion | `NONE / OPEN` | outside finite certificate |

```text
STRONGEST_POSITIVE_RESULT = FINITE_LITERAL_PRIME_SHELL_RESIDUAL_PHASE_CONTRACTION
STRONGEST_OBSTRUCTION = FINITE_PHASE_CONTRACTION_DOES_NOT_BOUND_THE_ASYMPTOTIC_RADIUS
OPEN_THEOREM = UNIFORM_LITERAL_V59_RADIUS_OR_SIGNED_PHASE_BOUND_WITH_EFFECTIVE_SAVING_GT_1_OVER_400
REUSABLE_STRUCTURE = EXACT_A_OPERATOR -> P3_PROJECTION -> RADIUS_SQUARED_INTERVAL -> SIGNED_PHASE_RATIO
ROUND2_CLUE = REPEAT_THE_CENSUS_WITH_GROWING_LOCAL_CUTOFF_AND_SMOOTH_PROFILE
```
