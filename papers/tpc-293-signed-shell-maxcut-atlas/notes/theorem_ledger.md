# TPC-293 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T293.1 | all-positive `K_m` favorable-edge maximum is `floor(m^2/4)` | `PROVED_EXACT_CONDITIONAL` | finite complete graph |
| T293.2 | signed frustration index is edge total minus signed max-cut value | `PROVED_EXACT_FINITE` | every finite signed graph |
| T293.3 | signed-graph switching preserves the objective | `PROVED_EXACT_FINITE` | every finite signed graph |
| T293.4 | complete physical signed-shell atlas | `NUMERICALLY_CERTIFIED_FINITE` | 18 declared rows / 1,380 edges |
| T293.5 | only one row has a positive sign-only gain, of `+3` | `NUMERICALLY_CERTIFIED_FINITE` | frozen literal grid |
| T293.6 | growing-shell signed compatibility theorem | `OPEN` | no asymptotic control |
| T293.7 | magnitude-weighted signed Rayleigh improvement | `OPEN` | edge magnitudes not included |
| T293.8 | source-native feasibility and arithmetic `L2` | `OPEN` | no coefficient-image proof |

```text
STRONGEST_POSITIVE_RESULT = EXACT_ALL_POSITIVE_MAXCUT_AND_SWITCHING_LEMMAS
STRONGEST_OBSTRUCTION = SIGN-ONLY OPTIMIZATION MATCHES ALL-POSITIVE BENCHMARK ON 17/18 ROWS
OPEN_THEOREM = MAGNITUDE-WEIGHTED SIGNED RAYLEIGH BOUND WITH SOURCE-IMAGE CONTROL
REUSABLE_STRUCTURE = PHYSICAL_GRAM -> SIGNED_COMPLETE_GRAPH -> MAXCUT/FRUSTRATION -> WEIGHTED TEST
ROUND2_CLUE = TEST_MAGNITUDE_WEIGHTED_SIGNED_RAYLEIGH_AND_SOURCE_IMAGE
```
