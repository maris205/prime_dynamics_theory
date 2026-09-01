# TPC-323 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T323.1 | direct/coherent trace decomposition | `PROVED_EXACT_FINITE` | every finite block family |
| T323.2 | positive-scalar invariance of the normalized profile | `PROVED_EXACT_FINITE` | every finite PSD Gram |
| T323.3 | profile majorization label protocol | `PROVED_EXACT_FINITE_DEFINITION` | declared finite vectors |
| T323.4 | all-plus profile majorizes direct profile | `NUMERICALLY_CERTIFIED_FINITE` | 24-row panel |
| T323.5 | alternative law profile census | `NUMERICALLY_CERTIFIED_FINITE` | 24-row panel |
| T323.6 | all-plus unique uniform named law | `NUMERICAL_OBSERVATION` | four laws, declared panel |
| T323.7 | all-plus energy/profile decoupling | `NUMERICALLY_CERTIFIED_FINITE` | 3 below / 21 above energy rows |
| T323.8 | universal asymptotic profile law | `OPEN` | no growing theorem |
| T323.9 | source-native arithmetic `L2` and Gate B | `OPEN` | unchanged |

```text
STRONGEST_POSITIVE_RESULT = ALL_PLUS_SIGNED_PROFILE_MAJORISATION_24_OF_24
STRONGEST_OBSTRUCTION = ENERGY_CROSSING_DOES_NOT_SELECT_PROFILE_AND_ALTERNATIVES_MIX
OPEN_THEOREM = FRESH_PROFILE_HOLDOUT_OR_SOURCE_NATIVE_SIGNED_ARITHMETIC_BOUND
REUSABLE_STRUCTURE = TRACE_RATIO_AMPLITUDE_PLUS_NORMALISED_PROFILE_SHAPE
ROUND2_CLUE = TEST_PROFILE_MAJORISATION_HOLDOUT_OR_SOURCE_NATIVE_ARITHMETIC_L2
```
