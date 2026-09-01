# TPC-322 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T322.1 | direct-sum norm identity | `PROVED_EXACT_FINITE` | every finite block family |
| T322.2 | sign-labelled diagonal isometry/projector identity | `PROVED_EXACT_FINITE` | every finite shell |
| T322.3 | cross-block Gram formula for `rho_e` | `PROVED_EXACT_FINITE` | every finite shell |
| T322.4 | projected fraction `0<=phi_e<=1` | `PROVED_EXACT_FINITE` | every finite shell |
| T322.5 | global sign gauge | `PROVED_EXACT_FINITE` | every finite sign vector |
| T322.6 | signed extrema exist on every declared row | `NUMERICALLY_CERTIFIED` | 24-row panel |
| T322.7 | all-plus / alternating counts | `NUMERICAL_OBSERVATION` | declared panel |
| T322.8 | universal all-plus or alternating law | `REFUTED_FINITE_PANEL` | declared panel only |
| T322.9 | growing canonical sign theorem | `OPEN` | no source theorem |
| T322.10 | arithmetic `L2`, Gate B, twin primes | `NONE / OPEN` | unchanged |

```text
STRONGEST_POSITIVE_RESULT = EXACT_OPERATOR_LEVEL_SIGNED_PROJECTOR_INTERFACE_PLUS_24_ROW_EXTREMA_ATLAS
STRONGEST_OBSTRUCTION = BOTH_CONTRACTION_AND_AMPLIFICATION_SIGNS_COEXIST_AND_NAMED_LAWS_REVERSE
OPEN_THEOREM = CANONICAL_SIGN_LAW_WITH_GROWING_SOURCE_IMAGE_AND_ARITHMETIC_L2
REUSABLE_STRUCTURE = DIRECT_SUM -> SIGNED_DIAGONAL_PROJECTOR -> CROSS_BLOCK GRAM -> SIGN ATLAS
ROUND2_CLUE = TEST_CANONICAL_SIGN_LAWS_AGAINST_OPERATOR_SPECTRAL_PROFILES_AND_SOURCE_NATIVE_ARITHMETIC_L2
```
