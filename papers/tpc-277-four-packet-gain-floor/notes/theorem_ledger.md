# TPC-277 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T277.1 | `G<=4D`, hence `D/G>=1/4` | `PROVED_EXACT` | four-packet Hilbert geometry |
| T277.2 | `E<=0` implies `G<=D`, hence `D/G>=1` | `PROVED_EXACT_CONDITIONAL` | signed cross-term condition |
| T277.3 | `r=(1-kappa)^(-1)` | `PROVED_EXACT` | `G>0` |
| T277.4 | geometry alone gives no `x^gamma`, `gamma>0` | `PROVED_EXACT_OBSTRUCTION` | orthogonal adversary |
| T277.5 | eight literal rows replay with `r>1` | `NUMERICALLY_CERTIFIED` | registered/extended finite rows |
| T277.6 | `r>=101/100` fails on the finite scan | `REFUTED_SCOPED` | no asymptotic promotion |
| T277.7 | uniform source-level power gain | `OPEN` | literal growing source |

```text
STRONGEST_POSITIVE_RESULT = SHARP_UNIVERSAL_FOUR_PACKET_FLOOR_PLUS_EXACT_SOURCE_SCAN
STRONGEST_OBSTRUCTION = GEOMETRY_ALONE_CANNOT_PAY_A_POSITIVE_POWER_AND_ONE_PERCENT_FAILS_FINITE
OPEN_THEOREM = UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND
REUSABLE_STRUCTURE = D,G,E -> kappa -> r=(1-kappa)^(-1)
ROUND2_CLUE = TEST_CROSS_SCALE_SIGNED_GAIN_STABILITY_AND_SHELL_SENSITIVITY
```
