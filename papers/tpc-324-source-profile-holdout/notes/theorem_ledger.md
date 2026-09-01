# TPC-324 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T324.1 | conditional translation covariance under shell-prime divisibility | `PROVED_EXACT_FINITE_CONDITIONAL` | every finite block family |
| T324.2 | direct/coherent Gram positivity and profile typing | `PROVED_EXACT_FINITE` | every nonzero finite row |
| T324.3 | amplitude/profile separation under positive rescaling | `PROVED_EXACT_FINITE` | every PSD Gram |
| T324.4 | all-plus holdout profile majorization | `NUMERICALLY_CERTIFIED_FINITE` | 48 rows, 2 frozen panels |
| T324.5 | per-panel all-plus replication | `NUMERICALLY_CERTIFIED_FINITE` | 24/24 on each panel |
| T324.6 | alternative-law census | `NUMERICALLY_CERTIFIED_FINITE` | 48 rows |
| T324.7 | source-location replication explains no asymptotic law | `OPEN` | no growing theorem |
| T324.8 | source-native arithmetic (L^2) and Gate B | `OPEN` | unchanged |

```text
STRONGEST_POSITIVE_RESULT = TWO_PANEL_ALL_PLUS_PROFILE_REPLICATION_48_OF_48
STRONGEST_OBSTRUCTION = FINITE_REPLICATION_IS_NOT_A_SOURCE_NATIVE_ARITHMETIC_THEOREM
OPEN_THEOREM = HOLDOUT_SCALE_LADDER_OR_SOURCE_NATIVE_SIGNED_ARITHMETIC_BOUND
REUSABLE_STRUCTURE = CONDITIONAL_TRANSLATION_COVARIANCE_PLUS_RESIDUE_SENSITIVE_HOLDOUT
ROUND2_CLUE = TEST_HOLDOUT_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2
```
